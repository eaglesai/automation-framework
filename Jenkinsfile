pipeline {
    agent {
        docker {
            image 'selenium/standalone-chrome:latest'
            args '--user root -v /dev/shm:/dev/shm'
        }
    }

    environment {
        TEST_EMAIL    = credentials('test-email')
        TEST_PASSWORD = credentials('test-password')
        BASE_URL      = 'https://www.automationexercise.com'
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

        stage('Parallel Test Execution') {
            parallel {

                stage('Smoke Tests') {
                    steps {
                        echo 'Running smoke tests...'
                        sh '''
                            python -m pytest tests/ui/ -m smoke \
                                -v -n 2 \
                                --html=reports/smoke_report.html \
                                --self-contained-html
                        '''
                    }
                }

                stage('Regression Tests') {
                    steps {
                        echo 'Running regression tests...'
                        sh '''
                            python -m pytest tests/ui/ -m regression \
                                -v -n 2 \
                                --html=reports/regression_report.html \
                                --self-contained-html
                        '''
                    }
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                echo 'Generating Allure report...'
                sh '''
                    python -m pytest tests/ -m "smoke or regression" \
                        --alluredir=allure-results \
                        -v
                '''
            }
        }
    }

    post {
        success {
            echo 'All tests passed!'
            archiveArtifacts artifacts: 'reports/*.html',
                             allowEmptyArchive: true
        }
        failure {
            echo 'Tests failed — check console output!'
            archiveArtifacts artifacts: 'reports/*.html',
                             allowEmptyArchive: true
        }
        always {
            echo 'Pipeline complete.'
        }
    }
}