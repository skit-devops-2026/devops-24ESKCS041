pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Environment Info') {
            steps {
                sh 'python3 --version || python --version'
                sh 'docker --version'
            }
        }

        stage('Install Dependencies & Test') {
            steps {
                sh 'python3 -m venv .venv || python -m venv .venv'
                sh '. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt && pytest -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t aqi-prediction:latest .'
            }
        }

        stage('Verify Monitoring Configs') {
            steps {
                sh 'test -f monitoring/prometheus.yml'
                sh 'test -f monitoring/aqi-dashboard.json'
                sh 'test -f docker-compose.yml'
                echo 'Monitoring and Docker configurations verified.'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
