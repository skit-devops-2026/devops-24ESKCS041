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
                sh 'python3 -m pip --version'
            }
        }

        stage('Create Virtual Environment') {
            steps {
                sh 'python3 -m venv .jenkins-venv'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '.jenkins-venv/bin/python -m pip install --upgrade pip'
                sh '.jenkins-venv/bin/python -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh '.jenkins-venv/bin/python -m pytest -v'
            }
        }

        stage('Verify Project') {
            steps {
                sh 'test -f app.py'
                sh 'test -f predict.py'
                sh 'test -f requirements.txt'
                sh 'test -d models'
                sh 'test -d tests'
                sh 'test -f models/random_forest_classifier.joblib'
                sh 'test -f models/aqi_regression_model.joblib'

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