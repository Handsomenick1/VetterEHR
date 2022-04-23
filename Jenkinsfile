pipeline {
    agent any
    environment {
        NEW_VERSION = '1.3.0'
    }
    stages {
        stage("Build") {
            steps {
                echo 'Building the application...'
                sh 'python --version'
                sh 'pip install pytest'
                sh 'pytest lib/lambdafunctions/tests'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing the application...'
                
            }
        }
        stage('Deploy') {
            steps {
                script {
                    echo 'Deploying the application...'
                }
            }
        }
    }

    post {
        always {
            // sending email to team
        }
        success {

        }
        failure {

        }

    }
}

node {

}