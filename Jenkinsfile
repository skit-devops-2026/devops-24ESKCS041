pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Environment') {
            steps {
                sh 'python3 --version'
                sh 'pip3 --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m pip install --upgrade pip'
                sh 'python3 -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'python3 -m pytest -v'
            }
        }

        stage('Verify Project') {
            steps {
                sh 'test -f app.py'
                sh 'test -f predict.py'
                sh 'test -d models'
                sh 'test -d tests'
                echo 'AirQualityPrediction project verification successful.'
            }
        }
    }

    post {
        success {
            echo 'AirQualityPrediction Jenkins pipeline completed successfully.'
        }

        failure {
            echo 'AirQualityPrediction Jenkins pipeline failed.'
        }

        always {
            echo 'Jenkins build finished.'
        }
    }
}