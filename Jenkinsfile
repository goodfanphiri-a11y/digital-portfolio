pipeline {

    agent any

    environment {

        AWS_DEFAULT_REGION = 'us-east-1'

        S3_BUCKET = 'goodfan-digital-portfolio-2026'

    }

    stages {

        stage('Checkout') {

            steps {

                echo 'Checking out GitHub repository...'

                checkout scm
            }
        }

        stage('Create Python Environment') {

            steps {

                echo 'Creating Python virtual environment...'

                sh '''
                    python3 -m venv venv

                    . venv/bin/activate

                    python -m pip install --upgrade pip

                    pip install -r requirements.txt
                '''
            }
        }

        stage('Deploy to S3') {

            steps {

                echo 'Deploying website to Amazon S3...'

                withCredentials([
                    [
                        $class: 'AmazonWebServicesCredentialsBinding',
                        credentialsId: 'aws-jenkins',
                        accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                        secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                    ]
                ]) {

                    sh '''
                        . venv/bin/activate

                        python deploy.py
                    '''
                }
            }
        }

        stage('Deployment Complete') {

            steps {

                echo 'Portfolio deployment completed successfully.'
            }
        }
    }

    post {

        success {

            echo 'SUCCESS: Portfolio deployed to S3.'
        }

        failure {

            echo 'ERROR: Portfolio deployment failed.'
        }
    }
}
