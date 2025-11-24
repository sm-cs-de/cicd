pipeline {
    agent any

    environment {
        DOCKER_BUILDKIT = "1"
        VERSION = "${env.GIT_COMMIT.substring(0,7)}"
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

	    stage('Install Dependencies') {
	        steps {
		        sh '''
		        python3 -m venv venv
		        . venv/bin/activate
		        pip install --upgrade pip
		        pip install -r requirements.txt
		        '''
	        }
	    }

	    stage('Check Style') {
	        steps {
		        sh '''
		        . venv/bin/activate
		        flake8 --exclude venv .> flake8.log || true
		        '''
                archiveArtifacts artifacts: 'flake8.log', fingerprint: true
	        }
	    }

	    stage('Check Formatting') {
	        steps {
		        sh '''
		        . venv/bin/activate
		        black --check --exclude "venv" . > black.log 2>&1 || true
		        '''
                archiveArtifacts artifacts: 'black.log', fingerprint: true
	        }
	    }

	    stage('Run Unit Tests 1') {
	        steps {
		        sh '''
		        . venv/bin/activate
		        python -m unittest discover -v tests
		        '''
	        }
	    }

	    stage('Build Docker Images') {
		    steps {
		        sh '''
		        echo "Building docker containers..."
		        VERSION=${VERSION} docker compose build --pull
		        '''
		    }
	    }

	    stage('Run Unit Tests 2') {
	        steps {
	            sh '''
	            SERVICES=$(docker compose config --services)
	            for SERVICE in ${SERVICES}; do
	                LOG_FILE=${SERVICE}_test.log
	                echo "Running pytest inside ${SERVICE}..."
	                docker compose run --rm ${SERVICE} pytest --maxfail=5 --disable-warnings > ${LOG_FILE} 2>&1 || true
	            done
	            '''
	            archiveArtifacts artifacts: '*_test.log', fingerprint: true
	        }
	    }

	    stage('Run Docker Images') {
	        steps {
	            sh '''
	            VERSION=${VERSION} docker compose down || true
	            VERSION=${VERSION} docker compose up -d
	            '''
	        }
	    }
    }
}

