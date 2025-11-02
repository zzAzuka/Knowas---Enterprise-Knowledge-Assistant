pipeline {
    agent any

    environment {
        DOCKER_HUB_REPO = 'sibirassal/sibi-knowas'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/zzAzuka/Knowas---Enterprise-Knowledge-Assistant.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                // Build from root, since Dockerfile is in repo root
                bat 'docker build -t %DOCKER_HUB_REPO%:latest -f Dockerfile .'
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', passwordVariable: 'DOCKER_HUB_PASS', usernameVariable: 'DOCKER_HUB_USER')]) {
                    // Use safer login method via stdin (avoids CLI password warning)
                    bat '''
                    echo %DOCKER_HUB_PASS% | docker login -u %DOCKER_HUB_USER% --password-stdin
                    '''
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                bat 'docker push %DOCKER_HUB_REPO%:latest'
            }
        }
    }
}
