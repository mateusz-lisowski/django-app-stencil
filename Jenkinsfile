pipeline {
    agent {
        docker {
            image 'python:3.10-alpine'
            args '--user root'
            reuseNode true
        }
    }

    environment {
        // Set Ci to true in order to use SQLite database
        CI = 'True'
    }

    stages {
        stage('Install all dependencies') {
            steps {
                sh '''
                    cd src
                    # Update pip first (optional but good practice)
                    pip install --upgrade pip
                    echo "Installing production requirements..."
                    pip install -r requirements.txt
                    echo "Installing development requirements..."
                    pip install -r requirements_dev.txt
                '''
            }
        }
        stage('Setup django application') {
            steps {
                sh '''
                    python src/manage.py collectstatic --no-input
                    python src/manage.py migrate --no-input
                '''
            }
        }
        stage('Lint project with flake8') {
            steps {
                sh '''
                    # Uncomment this line to actually run flake8
                    # flake8 --max-line-length 120 src
                    echo "Skipping flake8 linting (commented out)."
                '''
            }
        }
        stage('Perform all unit tests') {
            steps {
                sh '''
                    cd src
                    coverage run --source='.' manage.py test .
                    # Optional: Generate coverage report
                    # coverage report
                    # coverage html # For HTML report
                '''
            }
        }
        stage('Deploy app to production environment') {
            steps {
                sh '''
                    echo 'Mock deploying to production...'
                    # Add actual deployment commands here later
                    echo 'Application successfully deployed!'
                '''
            }
        }
    }
}