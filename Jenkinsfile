pipeline {
    agent any

    environment {
        DOCKER_HUB_REPO = 'sibirassal/sibi-knowas'   // Docker Hub repo name
        IMAGE_TAG = "latest"                                      // You can change this to a version or build number
    }

    stages {
        // 1️⃣ Step: Pull code from GitHub
        stage('Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-credentials',
                    url: 'https://github.com/zzAzuka/Knowas---Enterprise-Knowledge-Assistant.git'
            }
        }

        // 2️⃣ Step: Build the Docker image
        stage('Build Docker Image') {
            steps {
                script {
                    // This runs 'docker build -t yourdockerhubusername/yourimagename:latest .'
                    dockerImage = docker.build("${DOCKER_HUB_REPO}:${IMAGE_TAG}")
                }
            }
        }

        // 3️⃣ Step: Push image to Docker Hub
        stage('Push to Docker Hub') {
            steps {
                script {
                    // This logs in and pushes the image to your Docker Hub repo
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
                        dockerImage.push()
                    }
                }
            }
        }
    }

    // 4️⃣ Cleanup (Windows version uses bat)
    post {
        always {
            echo 'Cleaning up local Docker images...'
            bat '''
            docker system prune -af || exit 0
            '''
        }
    }
}