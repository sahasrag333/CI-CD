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
            def scannerHome = tool 'Sonarscanner'

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
stage('Deploy to QA') {
    steps {
        sh '''
        cp k8/qa/deployment.yaml k8/qa/deployment-temp.yaml

        sed -i "s/IMAGE_TAG/${BUILD_NUMBER}/g" k8/qa/deployment-temp.yaml

        kubectl apply -f k8/qa/deployment-temp.yaml
        kubectl apply -f k8/qa/service.yaml
        '''
    }
}
stage('QA Health Check') {
    steps {
        sh '''
        kubectl rollout status deployment/employee-portal -n qa
        '''
    }
}
stage('Approve Production Deployment') {
    steps {
        input(
            message: 'Deploy to Production?',
            ok: 'Deploy'
        )
    }
}
stage('Deploy to Production') {
    steps {
        sh '''
        cp k8/production/deployment.yaml k8/production/deployment-temp.yaml

        sed -i "s/IMAGE_TAG/${BUILD_NUMBER}/g" k8/production/deployment-temp.yaml

        kubectl apply -f k8/production/deployment-temp.yaml
        kubectl apply -f k8/production/service.yaml
        '''
    }
}stage('Production Health Check') {
    steps {
        sh '''
        kubectl rollout status deployment/employee-portal -n production
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