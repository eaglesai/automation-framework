pipeline {
    agent any

environment {
    BASE_URL      = "https://automationexercise.com"
    TEST_EMAIL    = "test2028now@yopmail.com"
    TEST_PASSWORD = "test"
    }
    stages {

        stage('Checkout') {
            steps {
                // Pull latest code from GitHub
                git branch: 'main',
                    url: 'https://github.com/eaglesai/automation-framework.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

     stage('Run BDD Login Tests') {
    steps {
        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
            sh '''
                . .venv/bin/activate
                pytest tests/bdd/step_defs/test_login_steps.py -v \
                    --alluredir=allure-results
            '''
            }
        }
    }

        stage('Run BDD Hybrid Tests') {
            steps {
                sh '''
                    . .venv/bin/activate
                    pytest tests/bdd/step_defs/test_hybrid_steps.py -v \
                        --alluredir=allure-results
                '''
            }
        }

    }

    post {
        always {
            // Publish Allure report after every run
            allure includeProperties: false,
                   jdk: '',
                   results: [[path: 'allure-results']]
        }
        failure {
            echo 'Pipeline failed — check Allure report for details'
        }
        success {
            echo 'All tests passed'
        }
    }
}