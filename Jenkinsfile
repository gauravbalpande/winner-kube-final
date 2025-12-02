pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_IMAGE_BACKEND = 'gauarvbalpande/uwinner-backend'
        DOCKER_IMAGE_FRONTEND = 'gauarvbalpande/uwinner-frontend'
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials'
       // KUBECONFIG_CREDENTIALS_ID = 'kubeconfig'
        GIT_REPO = 'https://github.com/gauravbalpande/winner.git'
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: "${GIT_REPO}"
            }
        }
        
        stage('Environment Setup') {
            steps {
                script {
                    sh '''
                        echo "Setting up environment..."
                        python3 --version
                        node --version
                        docker --version
                    '''
                }
            }
        }
        
        stage('Backend Tests') {
            steps {
                dir('backend') {
                    sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install -r requirements.txt
                        pip install pytest pytest-cov
                        pytest tests/ --cov=. --cov-report=xml || true
                    '''
                }
            }
        }
        
        stage('Frontend Tests') {
            steps {
                dir('frontend') {
                    sh '''
                        npm install
                        npm run test || true
                        npm run lint || true
                    '''
                }
            }
        }
        
        stage('Build Docker Images') {
            parallel {
                stage('Build Backend') {
                    steps {
                        script {
                            dir('backend') {
                                dockerImageBackend = docker.build("${DOCKER_IMAGE_BACKEND}:${BUILD_NUMBER}")
                                docker.build("${DOCKER_IMAGE_BACKEND}:latest")
                            }
                        }
                    }
                }
                stage('Build Frontend') {
                    steps {
                        script {
                            dir('frontend') {
                                dockerImageFrontend = docker.build("${DOCKER_IMAGE_FRONTEND}:${BUILD_NUMBER}", "--target production .")
                                docker.build("${DOCKER_IMAGE_FRONTEND}:latest", "--target production .")
                            }
                        }
                    }
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                script {
                    sh '''
                        echo "Running Trivy security scan..."
                        docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
                            aquasec/trivy image ${DOCKER_IMAGE_BACKEND}:${BUILD_NUMBER} || true
                        docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
                            aquasec/trivy image ${DOCKER_IMAGE_FRONTEND}:${BUILD_NUMBER} || true
                    '''
                }
            }
        }
        
        stage('Push to Registry') {
            steps {
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", "${DOCKER_CREDENTIALS_ID}") {
                        dockerImageBackend.push("${BUILD_NUMBER}")
                        dockerImageBackend.push("latest")
                        dockerImageFrontend.push("${BUILD_NUMBER}")
                        dockerImageFrontend.push("latest")
                    }
                }
            }
        }
        
    //     stage('Update Kubernetes Manifests') {
    //         steps {
    //             script {
    //                 sh """
    //                     sed -i 's|image: ${DOCKER_IMAGE_BACKEND}:.*|image: ${DOCKER_IMAGE_BACKEND}:${BUILD_NUMBER}|' k8s/backend-deployment.yaml
    //                     sed -i 's|image: ${DOCKER_IMAGE_FRONTEND}:.*|image: ${DOCKER_IMAGE_FRONTEND}:${BUILD_NUMBER}|' k8s/frontend-deployment.yaml
    //                     git config user.email "jenkins@betmasterx.com"
    //                     git config user.name "Jenkins CI"
    //                     git add k8s/
    //                     git commit -m "Update image tags to ${BUILD_NUMBER}" || true
    //                     git push origin main || true
    //                 """
    //             }
    //         }
    //     }
        
    //     stage('Deploy to Kubernetes') {
    //         steps {
    //             script {
    //                 withKubeConfig([credentialsId: "${KUBECONFIG_CREDENTIALS_ID}"]) {
    //                     sh '''
    //                         kubectl apply -f k8s/namespace.yaml
    //                         kubectl apply -f k8s/backend-deployment.yaml
    //                         kubectl apply -f k8s/frontend-deployment.yaml
    //                         kubectl apply -f k8s/ingress.yaml
    //                         kubectl rollout status deployment/betmasterx-backend -n betmasterx
    //                         kubectl rollout status deployment/betmasterx-frontend -n betmasterx
    //                     '''
    //                 }
    //             }
    //         }
    //     }
        
    //     stage('Run Ansible Configuration') {
    //         steps {
    //             ansiblePlaybook(
    //                 playbook: 'ansible/deploy.yml',
    //                 inventory: 'ansible/inventory.ini',
    //                 credentialsId: 'ansible-ssh-key',
    //                 extras: '-e build_number=${BUILD_NUMBER}'
    //             )
    //         }
    //     }
    // }
    
    post {
        success {
            echo 'Deployment successful!'
            slackSend(color: 'good', message: "Deployment successful: ${BUILD_NUMBER}")
        }
        failure {
            echo 'Deployment failed!'
            slackSend(color: 'danger', message: "Deployment failed: ${BUILD_NUMBER}")
        }
        always {
            cleanWs()
        }
    }
}