pipeline {
    agent any

    environment {
        NEW_VERSION = '1.3.0'
    }
    stages {
        stage("Build") {
            steps {
                echo 'Building the application...'
                sh 'python3 --version'
                sh 'pip3 install -r requirements.txt'
                
            }
        }
        stage('Test') {
            steps {
                echo 'Testing the application...'
                sh 'pytest lib/lambdafunctions/appointment/tests'
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
}

node {

}
