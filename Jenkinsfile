pipeline {
    agent any
    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "hip-watch-461221-r5"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    }
    stages {
        stage('Install gcloud CLI') {
            steps {
                sh """
                    # Install gcloud if missing
                    if [ ! -d "${GCLOUD_PATH}" ]; then
                        curl -sSL https://sdk.cloud.google.com | bash
                        export PATH=\$PATH:${GCLOUD_PATH}
                        gcloud components install --quiet gke-gcloud-auth-plugin
                    fi
                """
            }
        }
        
        stage('Clone GitHub Repo') {
            steps {
                checkout scmGit(
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        credentialsId: 'GitHub-token',
                        url: 'https://github.com/AmirGadami/ReserVigil.git'
                    ]]
                )
            }
        }

        stage('Set Up Python') {
            steps {
                sh """
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip wheel
                    pip install -e .
                """
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    sh """
                        export PATH=\$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=\${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet
                        
                        # Force AMD64 build for Cloud Run
                        docker build --platform linux/amd64 -t gcr.io/${GCP_PROJECT}/ml-project:latest .
                        docker push gcr.io/${GCP_PROJECT}/ml-project:latest
                    """
                }
            }
        }

        stage('Deploy to Cloud Run') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    sh """
                        export PATH=\$PATH:${GCLOUD_PATH}
                        gcloud run deploy ml-project \\
                            --image=gcr.io/${GCP_PROJECT}/ml-project:latest \\
                            --platform=managed \\
                            --region=us-central1 \\
                            --allow-unauthenticated \\
                            --quiet
                    """
                }
            }
        }
    }
}