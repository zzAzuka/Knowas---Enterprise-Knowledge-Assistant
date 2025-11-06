pipeline {
    agent any

    environment {
        AWS_REGION = 'eu-north-1'
        AWS_ACCOUNT_ID = '478261144529'
        ECR_REPO_NAME = 'knowas/sibi'
        IMAGE_TAG = 'latest'
        ECR_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
        EC2_HOST = 'ec2-13-49-183-249.eu-north-1.compute.amazonaws.com'
        PEM_PATH = 'C:\\EC2\\knowas-key.pem'
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
                        bat """
                        for /f "delims=" %%i in ('aws ecr get-login-password --region %AWS_REGION%') do (
                            echo %%i | docker login --username AWS --password-stdin %ECR_REGISTRY%
                        )
                        """
                    }
                }
            }
        }

        stage('Tag Docker Image') {
            steps {
                bat "docker tag %ECR_REPO_NAME%:%IMAGE_TAG% %ECR_REGISTRY%/%ECR_REPO_NAME%:%IMAGE_TAG%"
            }
        }

        stage('Push to ECR') {
            steps {
                bat "docker push %ECR_REGISTRY%/%ECR_REPO_NAME%:%IMAGE_TAG%"
            }
        }

        stage('Deploy to EC2') {
            steps {
                script {
                    // Clean, single-line SSH command that executes everything remotely on EC2 (Linux)
                    bat """
                    set PATH=%PATH%;C:\\Windows\\System32\\OpenSSH
                    ssh -i "%PEM_PATH%" -o StrictHostKeyChecking=no ec2-user@%EC2_HOST% "bash -c '
                        aws ecr get-login-password --region %AWS_REGION% | docker login --username AWS --password-stdin %ECR_REGISTRY% &&
                        docker pull %ECR_REGISTRY%/%ECR_REPO_NAME%:%IMAGE_TAG% &&
                        docker stop app || true &&
                        docker rm app || true &&
                        docker run -d -p 80:80 --name app %ECR_REGISTRY%/%ECR_REPO_NAME%:%IMAGE_TAG%
                    '"
                    """
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up local Docker images...'
            bat "docker system prune -af || exit 0"
        }
    }
}
