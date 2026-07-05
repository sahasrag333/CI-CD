pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                sh '''
                python -m venv venv
                ./venv/bin/python -m pip install --upgrade pip
                ./venv/bin/python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                ./venv/bin/python -m pytest
                '''
            }
        }

        stage('Run Ruff') {
            steps {
                sh '''
                ./venv/bin/python -m ruff check .
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline Successful'
        }
        failure {
            echo 'Pipeline Failed'
        }
    }
}