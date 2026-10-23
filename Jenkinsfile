
pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        timeout(time: 20, unit: 'MINUTES')
    }

    environment {
        APP_IMAGE = 'jenkins-github-cicd-demo'
        APP_CONTAINER = 'jenkins-github-cicd-demo'
        APP_PORT = '5000'
        LOCAL_PORT = '5000'
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'git rev-parse --short HEAD'
            }
        }

        stage('Build and Install Test Dependencies') {
            steps {
                sh '''
                    set -eu
                    python3 --version
                    python3 -m venv .venv
                    . .venv/bin/activate
                    python -m pip install --upgrade pip
                    python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Automated Tests') {
            steps {
                sh '''
                    set -eu
                    . .venv/bin/activate
                    PYTHONPATH=. pytest -v --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit testResults: 'test-results.xml',
                          allowEmptyResults: true
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    set -eu
                    docker build --pull \
                      --tag "${APP_IMAGE}:${BUILD_NUMBER}" \
                      --tag "${APP_IMAGE}:latest" .
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    set -eu

                    docker rm -f "${APP_CONTAINER}" 2>/dev/null || true

                    docker run -d \
                      --name "${APP_CONTAINER}" \
                      --restart unless-stopped \
                      -p "${LOCAL_PORT}:${APP_PORT}" \
                      "${APP_IMAGE}:${BUILD_NUMBER}"
                '''
            }
        }


        stage('Verify Deployed Application') {
            steps {
                sh '''
                    set -eu

                    echo "Checking application health inside the container..."

                    docker exec "${APP_CONTAINER}" python -c "
import json
import urllib.request

base = 'http://127.0.0.1:5000'

health = json.load(
    urllib.request.urlopen(base + '/health', timeout=5)
)
assert health.get('status') == 'healthy', health

body = json.load(
    urllib.request.urlopen(base + '/', timeout=5)
)
assert body.get('application') == 'Jenkins CI/CD Demo', body
assert body.get('message') == 'Deployment successful!', body

print('Health check passed:', health)
print('Application verification passed:', body)
"

                    echo "Deployment verification passed."
                '''
            }
        }

    }

    post {
        success {
            echo 'CI/CD pipeline succeeded: build, tests, deployment, and verification passed.'
        }
        failure {
            echo 'CI/CD pipeline failed. Review the failed stage and console output.'
        }
    }
}
