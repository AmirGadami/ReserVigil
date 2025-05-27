
pipeline{

    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages{
        stage('Clone Github repo to Jenkins'){
            steps{
                echo 'Clone Github repo to Jenkins...............'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'GitHub-token', url: 'https://github.com/AmirGadami/MLOps.git']])

            }
        }

    stage('Setting up our vertual Environment and Installing dependencies'){
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
    }


}