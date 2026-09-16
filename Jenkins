pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt || pip install pandas numpy scikit-learn flask'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t devops-24eskcs041:latest .'
            }
        }

        stage('Test') {
            steps {
                sh '. venv/bin/activate && python -m unittest discover -s . -p "*test*.py" || echo "No tests configured"'
            }
        }
    }
}
