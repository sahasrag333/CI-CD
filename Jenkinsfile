pipeline {
    agent any

    stages {

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
stage('SonarQube Analysis') {
    steps {
        script {
            def scannerHome = tool 'SonarScanner'

            withSonarQubeEnv('SonarQube') {
                sh """
                ${scannerHome}/bin/sonar-scanner
                """
            }
        }
    }
}

stage('Quality Gate') {
    steps {
        timeout(time: 5, unit: 'MINUTES') {
            waitForQualityGate abortPipeline: true
        }
    }
}
        stage('Build Docker Image') {
    steps {
        sh '''
        docker build -t employee-portal:${BUILD_NUMBER} .
        '''
    }
}

stage('Docker Login') {
    steps {
        withCredentials([usernamePassword(
            credentialsId: 'dockerhub-creds',
            usernameVariable: 'DOCKER_USER',
            passwordVariable: 'DOCKER_PASS'
        )]) {
            sh '''
            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
            '''
        }
    }
}

stage('Push Docker Image') {
    steps {
        sh '''
        docker tag employee-portal:${BUILD_NUMBER} gsahasra333/employee-portal:${BUILD_NUMBER}
        docker push gsahasra333/employee-portal:${BUILD_NUMBER}
        '''
    }
}

        stage('Deploy Container') {
            steps {
                sh '''
                docker rm -f employee-portal || true

                docker run -d \
                  --name employee-portal \
                  -p 5000:5000 \
                  employee-portal:${BUILD_NUMBER}
                '''
            }
        }
stage('Health Check') {
    steps {
        sh '''
        echo "Waiting for application to start..."
        sleep 5

        curl -f http://host.docker.internal:5000

        echo "Application is healthy!"
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