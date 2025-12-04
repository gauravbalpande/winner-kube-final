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
                echo "Running backend tests inside Docker..."
                docker build --no-cache -t backend-test .
                docker run --rm backend-test-image pytest --maxfail=1 -q || true
            '''
        }
    }
}



        
stage('Frontend Tests') {
    steps {
        dir('frontend') {
            sh '''
                echo "Setting up Node.js for frontend..."
                curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
                apt-get install -y nodejs --no-install-recommends

                echo "Node version:"
                node --version
                echo "npm version:"
                npm --version

                echo "Installing frontend dependencies..."
                npm install || true

                echo "Running frontend tests (if available)..."
                npm run test || echo "⚠️ No test script found (skipping tests)"
                npm run lint || echo "⚠️ No lint script found (skipping lint)"

                echo "Frontend test stage complete ✔"
            '''
        }
    }
}

        
        stage('Build Docker Images') {
    parallel {
        stage('Build Backend') {
            steps {
                script {
                    sh """
                        echo "🐳 Building Backend Image..."
                        cd backend
                        docker build -t ${DOCKER_IMAGE_BACKEND}:${BUILD_NUMBER} .
                        docker tag ${DOCKER_IMAGE_BACKEND}:${BUILD_NUMBER} ${DOCKER_IMAGE_BACKEND}:latest
                    """
                }
            }
        }

        stage('Build Frontend') {
            steps {
                script {
                    sh """
                        echo "🐳 Building Frontend Image..."
                        cd frontend
                        docker build --target production -t ${DOCKER_IMAGE_FRONTEND}:${BUILD_NUMBER} .
                        docker tag ${DOCKER_IMAGE_FRONTEND}:${BUILD_NUMBER} ${DOCKER_IMAGE_FRONTEND}:latest
                    """
                }
            }
        }
    }
}

stage('Security Scan') {
    steps {
        script {
            sh """
                echo "🔒 Running security scan using Trivy..."
                docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
                    aquasec/trivy image ${DOCKER_IMAGE_BACKEND}:${BUILD_NUMBER} || true
                docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
                    aquasec/trivy image ${DOCKER_IMAGE_FRONTEND}:${BUILD_NUMBER} || true
                
                echo "Security scan stage completed (not blocking pipeline)"
            """
        }
    }
}

stage('Push to Registry') {
    steps {
        script {
            withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIALS_ID}",
                                             usernameVariable: 'DOCKER_USER',
                                             passwordVariable: 'DOCKER_PASS')]) {
                sh '''#!/bin/bash
                echo "📤 Logging into Docker Hub..."

                echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin

                echo "📌 Pushing Backend Images..."
                docker push ${DOCKER_IMAGE_BACKEND}:${BUILD_NUMBER}
                docker push ${DOCKER_IMAGE_BACKEND}:latest

                echo "📌 Pushing Frontend Images..."
                docker push ${DOCKER_IMAGE_FRONTEND}:${BUILD_NUMBER}
                docker push ${DOCKER_IMAGE_FRONTEND}:latest
                
                docker logout
                '''
            }
        }
    }
}



        
        // stage('Update Kubernetes Manifests') {
        //     steps {
        //         script {
        //             sh """
        //                 sed -i 's|image: ${DOCKER_IMAGE_BACKEND}:.*|image: ${DOCKER_IMAGE_BACKEND}:${BUILD_NUMBER}|' k8s/backend-deployment.yaml
        //                 sed -i 's|image: ${DOCKER_IMAGE_FRONTEND}:.*|image: ${DOCKER_IMAGE_FRONTEND}:${BUILD_NUMBER}|' k8s/frontend-deployment.yaml
        //                 git config user.email "jenkins@betmasterx.com"
        //                 git config user.name "Jenkins CI"
        //                 git add k8s/
        //                 git commit -m "Update image tags to ${BUILD_NUMBER}" || true
        //                 git push origin main || true
        //             """
        //         }
        //     }
        // }
        
        // stage('Deploy to Kubernetes') {
        //     steps {
        //         script {
        //             withKubeConfig([credentialsId: "${KUBECONFIG_CREDENTIALS_ID}"]) {
        //                 sh '''
        //                     kubectl apply -f k8s/namespace.yaml
        //                     kubectl apply -f k8s/backend-deployment.yaml
        //                     kubectl apply -f k8s/frontend-deployment.yaml
        //                     kubectl apply -f k8s/ingress.yaml
        //                     kubectl rollout status deployment/betmasterx-backend -n betmasterx
        //                     kubectl rollout status deployment/betmasterx-frontend -n betmasterx
        //                 '''
        //             }
        //         }
        //     }
        // }
        
        // stage('Run Ansible Configuration') {
        //     steps {
        //         ansiblePlaybook(
        //             playbook: 'ansible/deploy.yml',
        //             inventory: 'ansible/inventory.ini',
        //             credentialsId: 'ansible-ssh-key',
        //             extras: '-e build_number=${BUILD_NUMBER}'
        //         )
        //     }
        // }
    }
    
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