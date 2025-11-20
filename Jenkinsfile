pipeline {
    agent any
    
    environment {
        APP_NAME = "cicd"
    }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '15'))
        timeout(time: 40, unit: 'MINUTES')
    }

    stages {
        stage('Clone') {
            steps {
                git branch: 'main', url: 'https://github.com/sm-cs-de/cicd.git'
            }
        }

        stage('Install dependencies') {
            steps {
                sh """
                pip install --upgrade pip
                pip3 install -r requirements.txt
                """
            }
        }

        stage('Lint') {
            steps {
                sh """
                pip install flake8
                flake8 app --count --select=E9,F63,F7,F82 --show-source --statistics
                """
            }
        }

        stage('Formatting Check') {
            steps {
                sh """
                pip install black
                black --check app
                """
            }
        }

        stage('Run tests') {
            steps {
                sh 'python3 -m unittest discover -v'
            }
        }
    }
}

