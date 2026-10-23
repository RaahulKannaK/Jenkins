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
                    . .venv/bin/activate
                    pytest -v --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit testResults: 'test-results.xml', allowEmptyResults: true
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
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
                    URL="http://127.0.0.1:${LOCAL_PORT}"
                    ok=0
                    for attempt in $(seq 1 20); do
                      if curl --fail --silent --show-error "${URL}/health"; then
                        ok=1
                        break
                      fi
                      echo "Application not ready yet (attempt ${attempt}/20)"
                      sleep 3
                    done

                    if [ "${ok}" -ne 1 ]; then
                      echo "Health check failed. Container logs:"
                      docker logs "${APP_CONTAINER}" || true
                      exit 1
                    fi

                    BODY="$(curl --fail --silent --show-error "${URL}/")"
                    echo "${BODY}"
                    echo "${BODY}" | grep -q 'Jenkins CI/CD Demo'
                    echo "${BODY}" | grep -q 'Deployment successful'
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
