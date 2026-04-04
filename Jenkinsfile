pipeline {
    agent {
        docker {
            image 'python:3.11'
            args '--user root'
        }
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Smoke Tests') {
            steps {
                echo 'Running Smoke Tests...'
                sh 'python -m pytest tests/smoke/'
            }
        }

        stage('Regression Tests') {
            steps {
                echo 'Running Regression Tests...'
                sh 'python -m pytest tests/regression/'
            }
        }
    }

    post {
        always {
            echo 'Pipeline complete.'
        }
        failure {
            echo 'Some tests failed — check the report!'
        }
    }
}