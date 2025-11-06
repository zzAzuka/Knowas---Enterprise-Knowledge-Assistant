pipeline {
    agent any

    environment {
        AWS_REGION = 'eu-north-1'
        AWS_ACCOUNT_ID = '478261144529'
        ECR_REPO_NAME = 'knowas/sibi'
        IMAGE_TAG = "latest"
        ECR_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-credentials',
                    url: 'https://github.com/zzAzuka/Knowas---Enterprise-Knowledge-Assistant.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${ECR_REPO_NAME}:${IMAGE_TAG}")
                }
            }
        }

        stage('Login to ECR') {
            steps {
                script {
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-credentials']]) {
                        sh '''
                            aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                        '''
                    }
                }
            }
        }

        stage('Tag Docker Image') {
            steps {
                script {
                    sh "docker tag ${ECR_REPO_NAME}:${IMAGE_TAG} ${ECR_REGISTRY}/${ECR_REPO_NAME}:${IMAGE_TAG}"
                }
            }
        }

        stage('Push to ECR') {
            steps {
                script {
                    sh "docker push ${ECR_REGISTRY}/${ECR_REPO_NAME}:${IMAGE_TAG}"
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up local Docker images...'
            sh '''
            docker system prune -af || true
            '''
        }
    }
}
