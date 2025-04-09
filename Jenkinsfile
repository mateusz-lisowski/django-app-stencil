pipeline {
    agent {
        docker {
            image 'python:3.10-alpine'
            args '--user root'
            reuseNode true
        }
    }

    environment {
        // Name of the repository
        REPO_NAME = 'django-test-deploy-app'
        // Set Ci to true in order to use SQLite database
        CI = 'True'
        // Private key to deployment VPS
        SSH_PRIVATE_KEY = credentials('jenkins-private-key-file')
        // User on the VPS
        SSH_USER = credentials('hostinger-username')
        // IP or domain name of VPS
        SSH_HOST = credentials('hostinger-hostname')
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
                // Step 1: Install SSH Client, Prepare SSH directory and private key
                sh '''
                    echo "Updating package list and installing SSH client..."
                    # Update apk cache and install openssh-client
                    # --no-cache avoids keeping the cache, saving space in the container layer
                    apk update && apk add --no-cache openssh-client

                    echo "Setting up SSH configuration..."
                    mkdir -p ~/.ssh/
                    # Ensure the private key ends with a newline for compatibility
                    (echo "$SSH_PRIVATE_KEY"; echo) > ~/.ssh/github
                    chmod 600 ~/.ssh/github
                    echo "SSH key file created and permissions set."
                '''
                // Step 2: Create/Append SSH config using here document
                sh '''
                    echo "Appending to SSH config..."
                    cat >>~/.ssh/config <<END
Host target
  HostName $SSH_HOST
  User $SSH_USER
  IdentityFile ~/.ssh/github
  LogLevel ERROR
  StrictHostKeyChecking no
END
                    # Optional: Verify config file content
                    # echo "--- SSH Config ---"
                    # cat ~/.ssh/config
                    # echo "------------------"
                    echo "SSH config updated."
                '''
                // Step 3: Execute remote commands via SSH
                sh '''
                    echo "Attempting SSH connection and deployment..."
                    # Add -T to prevent pseudo-terminal allocation issues sometimes seen in CI
                    ssh -T target "
                        echo 'Connected to target host.'
                        cd $REPO_NAME/ || exit 1 # Exit if cd fails
                        echo 'Pulling latest changes...'
                        git pull || exit 1 # Exit if pull fails
                        echo 'Stopping existing containers...'
                        docker compose down
                        echo 'Building new images...'
                        docker compose build || exit 1 # Exit if build fails
                        echo 'Starting new containers...'
                        docker compose up -d --force-recreate || exit 1 # Exit if up fails
                        echo 'Remote commands executed.'
                    "
                    echo 'Application deployment commands sent successfully!'
                '''
            }
        }
    }
}