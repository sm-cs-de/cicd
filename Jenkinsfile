pipeline {
    agent any

    environment {
        DOCKER_BUILDKIT = "1"
        BUILD_TAG = "${env.GIT_COMMIT.substring(0,7)}"
    }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/sm-cs-de/cicd.git'
            }
        }

	stage('Install dependencies') {
	    steps {
		sh """
		python3 -m venv venv
		. venv/bin/activate
		pip install --upgrade pip
		pip install -r requirements.txt
		"""
	    }
	}

	stage('Lint') {
	    steps {
		sh """
		. venv/bin/activate
		pip install flake8
		flake8 --exclude venv .> flake8.log || true
		"""
                archiveArtifacts artifacts: 'flake8.log', fingerprint: true
	    }
	}

	stage('Formatting Check') {
	    steps {
		sh """
		. venv/bin/activate
		pip install black
		black --check --exclude "venv" . > black.log 2>&1 || true
		"""
                archiveArtifacts artifacts: 'black.log', fingerprint: true
	    }
	}

	stage('Unit tests') {
	    steps {
		sh """
		. venv/bin/activate
		python -m unittest discover -v tests
		"""
	    }
	}

        stage('Build Docker Images') {
            steps {
                sh '''
                echo "Building docker containers..."
                BUILD_TAG=${BUILD_TAG} docker compose build --pull
                '''
            }
        }

        stage('Run Docker Images') {
            steps {
                sh '''
                BUILD_TAG=${BUILD_TAG} docker compose down || true
                BUILD_TAG=${BUILD_TAG} docker compose up -d
                '''
            }
        }
    }
}

