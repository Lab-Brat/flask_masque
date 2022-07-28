pipeline {
    agent any
    stages {
        stage('Get Repo') {
            steps {
                git url: 'https://github.com/Lab-Brat/flask_masque.git', branch: 'main'
                sh "chmod +x Docker/entry_point.sh"
            }
        }
        
        stage("verify tooling") {
            steps {
                sh '''
                    docker version
                    docker info
                    docker compose version 
                    curl --version
                    jq --version
                    '''
            }
        }

        stage('Start container') {
            steps {
                sh 'docker compose up -d --no-color --wait'
                sh 'docker compose ps'
            }
        }

        stage('Run connectivity test') {
            steps {
                sh 'sleep 10'
                sh 'curl -I http://127.0.0.1:5000/'
            }
        }

        stage('Run unit tests') {
            steps {
                sh 'pytest'
            }
        }
    }

    post {
        always {
            sh 'docker compose down --remove-orphans -v'
            sh 'docker compose ps'
        }
    }
}
