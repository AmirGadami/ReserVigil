
pipeline{

    agent any

    environment {
        VENV_DIR = 'venv'
        GCP = "jovial-talon-459814-r5"
        GCLOUD_PATH = "var/jenkins_home/google-cloud-sdk/bin"
    }

    stages{
        stage('Clone Github repo to Jenkins'){
            steps{
                echo 'Clone Github repo to Jenkins...............'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'GitHub-token', url: 'https://github.com/AmirGadami/MLOps.git']])

            }
        }

    stage('Setting up our Vertual Environment and Installing dependencies'){
            steps{
                echo 'Setting up our vertual Environment and Installing dependencies...............'
                sh """
                python -m venv ${VENV_DIR}
                . ${VENV_DIR}/bin/activate
                pip install --upgrade pip
                pip install -e .
                """
            }

        }

    stage('Building and Pushing Docker Image to GCR'){
            steps{
                withCredentials([file(credentialsId : 'gcp-token'), variable: 'GOOGLE_APPLICATION_CREDENTIALS']){

                    echo "Building and Pushing Docker Image to GCR............."
                    sh """
                       export PATH=$PATH:${GCLOUD_PATH}


                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud auth configure-docker --quiet

                        docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .

                        docker push gcr.io/${GCP_PROJECT}/ml-project:latest 
                    """
                }
                
            }
            
        }
        stage('Deploy to Google Cloud Run'){
            steps{
                withCredentials([file(credentialsId: 'gcp-key' , variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Deploy to Google Cloud Run.............'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}


                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud run deploy ml-project \
                            --image=gcr.io/${GCP_PROJECT}/ml-project:latest \
                            --platform=managed \
                            --region=us-central1 \
                            --allow-unauthenticated
                            
                        '''
                }
                
            }
            
        }
    }


}