pipeline {
    agent any

    environment {
        DOCKER_BUILDKIT = "1"
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
		flake8 --exclude venv . || true
		"""
	    }
	}

	stage('Formatting Check') {
	    steps {
		sh """
		. venv/bin/activate
		pip install black
		black --check --exclude "venv" . || true
		"""
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
                docker compose build --pull
                '''
            }
        }

        stage('Run Docker Compose (optional)') {
            when {
                expression { fileExists('docker-compose.yml') }
            }
            steps {
                sh '''
                docker compose down || true
                docker compose up -d
                '''
            }
        }
    }
}

