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
        stage('Install development dependencies') {
            steps {
                sh '''
                    cd src
                    # Update pip first (optional but good practice)
                    pip install --upgrade pip
                    echo "Installing development requirements..."
                    pip install -r requirements_dev.txt
                '''
            }
        }
        stage('Lint project with flake8') {
            steps {
                sh '''
                    # Lint all code to ensure coherent styling
                    flake8 --max-line-length 120 src
                '''
            }
        }
        stage('Install production dependencies') {
            steps {
                sh '''
                    cd src
                    echo "Installing production requirements..."
                    pip install -r requirements.txt
                '''
            }
        }
        stage('Setup django application') {
            steps {
                sh '''
                    # Collect all static files needed for proper page work
                    python src/manage.py collectstatic --no-input
                    # Migrate all schemas to test database
                    python src/manage.py migrate --no-input
                '''
            }
        }
        stage('Perform all unit tests and generate coverage report') {
            steps {
                sh '''
                    cd src
                    # Run tests and collect coverage data
                    coverage run --source='.' manage.py test .

                    # Generate coverage report in XML format (Cobertura)
                    coverage xml -o coverage.xml

                    # Optional: Generate console report for quick view in logs
                    # coverage report

                    # Optional: Generate HTML report for Browse
                    # coverage html # Output will be in htmlcov/ directory
                '''
            }
            // Add a post-build action to publish the report
            post {
                always {
                    junit 'src/test-reports/unittest.xml' // Tell Jenkins to look for the XML file
                }
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