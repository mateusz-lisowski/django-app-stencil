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
                    # Install unittest-xml-reporting for JUnit XML reports
                    pip install unittest-xml-reporting
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
        stage('Perform tests and generate reports') { // Renamed stage
            steps {
                sh '''
                    cd src
                    # Run tests using the XMLTestRunner to generate JUnit XML report
                    # Ensure tests are discovered correctly (adjust '.' if needed)
                    coverage run --source='.' manage.py test --testrunner=xmlrunner.extra.djangotestrunner.XMLTestRunner .

                    # Generate coverage report in Cobertura XML format
                    coverage xml -o coverage.xml

                    # Optional: Generate console report
                    # coverage report

                    # Optional: Generate HTML report for Browse
                    # coverage html # Output will be in htmlcov/ directory
                '''
            }
            // Post actions to publish reports
            post {
                always {
                    // Publish JUnit XML test results
                    junit '**/TEST-*.xml' // Default pattern for unittest-xml-reporting

                    // Publish Cobertura coverage report
                    publishCoverage adapters: [coberturaAdapter('**/coverage.xml')]
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