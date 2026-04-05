pipeline {
    agent {
        docker {
            image 'selenium/standalone-chrome:latest'  // Chrome + ChromeDriver built in!
            args '--user root -v /dev/shm:/dev/shm'
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

        stage('UI Smoke Tests') {
            steps {
                echo 'Running Smoke Tests...'
                sh 'python -m pytest tests/ui/ -m smoke'
            }
        }
        /*
        stage('UI Regression Tests') {
            steps {
                echo 'Running Regression Tests...'
                sh 'python -m pytest tests/ui/ -m regression'
            }
        */
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