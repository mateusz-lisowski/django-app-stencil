pipeline {
    agent {
        docker {
            image 'python:3.10-alpine'
            reuseNode true
        }
    }

    stages {
         stage('Install all dependencies') {
            steps {
                sh '''
                    cd src
                    pip install -r requirements.txt
                    pip install -r requirements_dev.txt
                '''
            }
        }
        stage('Setup django aplication') {
            steps {
                sh '''
                    cd src
                    python manage.py collectstatic --no-input
                '''
            }
        }
        stage('Lint project with flake8') {
            steps {
                sh '''
                    cd src
                    # flake8 --max-line-length 120
                '''
            }
        }
        stage('Perform all unit tests') {
            steps {
                sh '''
                    cd src
                    coverage run --source='.' manage.py test .
                '''
            }
        }
        stage('Deploy app to production environment') {
            steps {
                sh '''
                    echo 'Mock deploying to production...'
                    echo 'Application successfully deployed!'
                '''
            }
        }
    }
}
