pipeline {
    agent any

    environment {
        AWS_REGION = 'eu-north-1'
        AWS_ACCOUNT_ID = '478261144529'
        ECR_REPO_NAME = 'knowas/sibi'
        IMAGE_TAG = 'latest'
        ECR_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
        EC2_HOST = 'ec2-13-49-183-249.eu-north-1.compute.amazonaws.com'
        PEM_PATH = 'C:\\ProgramData\\Jenkins\\.ssh\\knowas-key.pem'
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

        stage('Fix SSH Key Permissions') {
            steps {
                script {
                    // Take ownership of the file, then set proper permissions
                    bat """
                    takeown /F "%PEM_PATH%"
                    icacls "%PEM_PATH%" /reset
                    icacls "%PEM_PATH%" /inheritance:r
                    icacls "%PEM_PATH%" /grant:r "SYSTEM:(R)"
                    """
                }
            }
        }
        
        stage('Deploy to EC2') {
            steps {
                script {
                    // Execute remote commands on EC2 - all commands run on Linux EC2 instance
                    bat """
                    ssh -i "%PEM_PATH%" -o StrictHostKeyChecking=no ec2-user@%EC2_HOST% "aws ecr get-login-password --region %AWS_REGION% | docker login --username AWS --password-stdin %ECR_REGISTRY% && docker pull %ECR_REGISTRY%/%ECR_REPO_NAME%:%IMAGE_TAG% && docker stop app 2>/dev/null || true && docker rm app 2>/dev/null || true && docker run -d -p 80:80 --name app %ECR_REGISTRY%/%ECR_REPO_NAME%:%IMAGE_TAG%"
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