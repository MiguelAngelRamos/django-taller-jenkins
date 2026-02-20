pipeline {
    agent any

    environment {
        IMAGE_NAME = "django-clean-api"
        CONTAINER_DEV = "api-staging"
        CONTAINER_PROD = "api-production"
    }

    stages {
        stage('1. Checkout') {
            steps {
                checkout scm
            }
        }

        stage('2. Install & Test') {
            agent {
                docker { 
                    // Usamos la misma imagen base que definimos en el Dockerfile
                    image 'python:3.11-slim' 
                    args '--entrypoint=""' 
                }
            }
            steps {
                echo "Ejecutando suite de pruebas en la rama: ${env.BRANCH_NAME}"
                
                // Instalamos dependencias optimizando con una caché local del workspace
                sh 'pip install --cache-dir .pip-cache -r requirements.txt'
                
                // Ejecutamos las pruebas. Django creará su propia BD SQLite en memoria,
                // la probará y la destruirá sin afectar nada más.
                sh 'python manage.py test'
            }
        }

        stage('3. Build Docker Image') {
            when {
                anyOf { branch 'develop'; branch 'main' }
            }
            steps {
                script {
                    echo "Empaquetando la imagen inmutable de la API..."
                    // Si llegamos aquí, los tests pasaron. Construimos la imagen con total seguridad.
                    sh "docker build -t ${IMAGE_NAME}:${env.BRANCH_NAME} ."
                }
            }
        }

        stage('4. Deploy to Staging') {
            when { branch 'develop' }
            steps {
                script {
                    echo "🚀 Desplegando API en STAGING (Puerto 8081)..."
                    sh "docker stop ${CONTAINER_DEV} || true"
                    sh "docker rm ${CONTAINER_DEV} || true"
                    // Mapeamos el puerto 8081 del servidor al 8000 interno del contenedor Django
                    sh "docker run -d --name ${CONTAINER_DEV} -p 8081:8000 ${IMAGE_NAME}:develop"
                }
            }
        }

        stage('5. Deploy to Production') {
            when { branch 'main' }
            steps {
                script {
                    echo "🚀 Desplegando API en PRODUCCIÓN (Puerto 80)..."
                    sh "docker stop ${CONTAINER_PROD} || true"
                    sh "docker rm ${CONTAINER_PROD} || true"
                    // Mapeamos el puerto 80 estándar HTTP al 8000 interno del contenedor
                    sh "docker run -d --name ${CONTAINER_PROD} -p 80:8000 ${IMAGE_NAME}:main"
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}
