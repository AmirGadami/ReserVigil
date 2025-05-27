
pipeline{

    agent any

    stages{
        stage('Clone Github repo to Jenkins'){
            steps{
                echo 'Clone Github repo to Jenkins...............'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'GitHub-token', url: 'https://github.com/AmirGadami/MLOps.git']])

            }
        }
    }


}