pipeline {
    agent any

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
                echo 'Running smoke tests...'
                sh 'pytest -m smoke -v --html=reports/report.html --self-contained-html'
            }
        }

        stage('Regression Tests') {
            steps {
                echo 'Running regression tests...'
                sh 'pytest -m regression -v'
            }
        }
    }

    post {
        success {
            echo 'All tests passed!'
        }
        failure {
            echo 'Some tests failed — check the report!'
        }
        always {
            echo 'Pipeline complete.'
        }
    }
}