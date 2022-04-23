pipeline {
    agent {
        docker : {image 'python'}
    }
    environment {
        NEW_VERSION = '1.3.0'
    }
    stages {
        stage("Build") {
            steps {
                echo 'Building the application...'
                sh 'python3 --version'
                
            }
        }
        stage('Test') {
            steps {
                echo 'Testing the application...'
                sh 'pip3 install pytest'
                sh 'pytest lib/lambdafunctions/tests'
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