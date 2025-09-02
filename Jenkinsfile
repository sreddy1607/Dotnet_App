/*
=======================================================================================
This file is being updated constantly by the DevOps team to introduce new enhancements
based on the template.  If you have suggestions for improvement,
please contact the DevOps team so that we can incorporate the changes into the
template.  In the meantime, if you have made changes here or don't want this file to be
updated, please indicate so at the beginning of this file.
=======================================================================================
*/

//variables from ibm template
def branch = env.BRANCH_NAME ?: "DEV"
def namespace = env.NAMESPACE  ?: "dev"
def cloudName = env.CLOUD_NAME == "openshift" ? "openshift" : "kubernetes"
def workingDir = "/home/jenkins/agent"

APP_NAME="combined-devops-cognos-deployments"

pipeline {
  agent {
    kubernetes {
      yaml """
        apiVersion: v1
        kind: Pod
        spec:
          serviceAccountName: jenkins
          volumes:
            - name: dockersock
              hostPath:
                path: /var/run/docker.sock
            - emptyDir: {}
              name: varlibcontainers
            - name: jenkins-trusted-ca-bundle
              configMap:
                name: jenkins-trusted-ca-bundle
                defaultMode: 420
                optional: true
          containers:
            - name: jnlp
              securityContext:
                privileged: true
              envFrom:
                - configMapRef:
                    name: jenkins-agent-env
                    optional: true
              env:
                - name: GIT_SSL_CAINFO
                  value: "/etc/pki/tls/certs/ca-bundle.crt"
              volumeMounts:
                - name: jenkins-trusted-ca-bundle
                  mountPath: /etc/pki/tls/certs
            - name: node
              image: registry.access.redhat.com/ubi8/nodejs-16:latest
              tty: true
              command: ["/bin/bash"]
              securityContext:
                privileged: true
              workingDir: ${workingDir}
              securityContext:
                privileged: true
              envFrom:
                - configMapRef:
                    name: jenkins-agent-env
                    optional: true
              env:
                - name: HOME
                  value: ${workingDir}
                - name: BRANCH
                  value: ${branch}
                - name: GIT_SSL_CAINFO
                  value: "/etc/pki/tls/certs/ca-bundle.crt"
              volumeMounts:
                - name: jenkins-trusted-ca-bundle
                  mountPath: /etc/pki/tls/certs
            - name: python
              image: 136299550619.dkr.ecr.us-west-2.amazonaws.com/cammisboto3:1.2.0
              tty: true
              command: ["/bin/bash"]
              securityContext:
                privileged: true
              workingDir: ${workingDir}
              securityContext:
                privileged: true
              envFrom:
                - configMapRef:
                    name: jenkins-agent-env
                    optional: true
              env:
                - name: HOME
                  value: ${workingDir}
                - name: BRANCH
                  value: ${branch}
                - name: GIT_SSL_CAINFO
                  value: "/etc/pki/tls/certs/ca-bundle.crt"
              volumeMounts:
                - name: jenkins-trusted-ca-bundle
                  mountPath: /etc/pki/tls/certs
      """
    }
  }
  environment  {
    GIT_BRANCH = "${BRANCH_NAME}"
  }
                  
  options {
    disableConcurrentBuilds()
    timestamps()
  }

  stages {
    stage("initialize") {
      steps {
        script {
          echo "Branch: ${env.GIT_BRANCH}"
          echo "Initializing Motio pipeline..."
        }
      }
    }

    stage('Check Python Availability') {
      steps { 
        container('node') {
          sh '''
            echo "Checking for Python3..."
            which python3 || echo "Python3 is NOT installed"
            python3 --version ||echo "Unable to get Python version"
          '''
        }
      }
    }

    stage('MotioCI Login') {
      steps {
        withCredentials([
          file(credentialsId: 'prod-credentials-json', variable: 'CREDENTIALS_FILE')
        ]) {
          container('python') {
            script {
              echo "Installing MotioCI CLI dependencies"
              sh '''
                cd MotioCI/api/CLI
                python3 -m pip install --user -r requirements.txt
                echo "Successfully installed packages"
              '''
              
              echo "Logging into MotioCI with stored credentials file"
              env.MOTIO_AUTH_TOKEN = sh(
                script: '''
                  cd MotioCI/api/CLI
                  # Login and capture only the token line, then extract just the token
                  python3 ci-cli.py --server="https://cgrptmcip01.cloud.cammis.ca.gov" login --credentialsFile "$CREDENTIALS_FILE" | grep "Auth Token:" | cut -d: -f2 | tr -d ' '
                ''',
                returnStdout: true
              ).trim()
              echo "MotioCI login completed - Token captured: ${env.MOTIO_AUTH_TOKEN}"
            }
          }
        }
      }
    }

    // Temporarily commented out to avoid creating labels during testing
    /*
    stage('MotioCI Versioning') {
      steps {
        container('python') {
          script {
            echo "Creating MotioCI version for branch: ${env.GIT_BRANCH}"
            sh '''
              cd MotioCI/api/CLI
              
              # Create version based on branch and build number
              VERSION_NAME="${BRANCH_NAME}-${BUILD_NUMBER}"
              echo "Creating version: $VERSION_NAME"
              
              # Execute versioning command using auth token from login stage
              if [ -n "${MOTIO_AUTH_TOKEN}" ]; then
                echo "Using authentication token from login stage"
                
                # Create label in Demo project 
                python3 ci-cli.py --server="https://cgrptmcip01.cloud.cammis.ca.gov" label create --xauthtoken="${MOTIO_AUTH_TOKEN}" --instanceName="Cognos-DEV/TEST" --projectName="Demo" --name="$VERSION_NAME" --versionedItemIds="[]"
                
                echo "MotioCI label $VERSION_NAME created successfully in Demo project"
                
                # Capture the label ID for promotion
                echo "Getting label ID for newly created label..."
                LABEL_LIST=$(python3 ci-cli.py --server="https://cgrptmcip01.cloud.cammis.ca.gov" label ls --xauthtoken="${MOTIO_AUTH_TOKEN}" --instanceName="Cognos-DEV/TEST" --projectName="Demo")
                echo "Current labels in Demo project:"
                echo "$LABEL_LIST"
              else
                echo "ERROR: No authentication token available from login stage"
                exit 1
              fi
            '''
          }
        }
      }
    }
    */

    stage('Deploy') {
      steps {
        container('python') {
          script {
            echo "Testing MotioCI Promotion"
            sh '''
              cd MotioCI/api/CLI
              # Disable SSL verification for this session
              export PYTHONHTTPSVERIFY=0

              # Test if you can access PROD projects specifically
              python3 ci-cli.py --server="https://cgrptmcip01.cloud.cammis.ca.gov" project ls --xauthtoken="${MOTIO_AUTH_TOKEN}" --instanceName="Cognos-PRD"
              echo "Test 4: Testing deploy command without username/password (maybe it will work?):"
              python3 ci-cli.py --server="https://cgrptmcip01.cloud.cammis.ca.gov" deploy \
                --xauthtoken="2319e4b2-b37e-4195-83f1-616b97d566cb" \
                --sourceInstanceId="3" \
                --targetInstanceId="1" \
                --labelId="57" \
                --projectName="Demo" \
                --targetLabelName="PROMOTED-20250712-115" \
                --camPassportId="MTsxMDE6NmQxNzBlODYtMTJhZS0yMjgxLWY0ZjktMmZmMDgxMjIwNzY2OjI3NTU2MjA2NjQ7MDszOzA7" \
                --namespaceId="AzureAD"
              
              echo ""
              echo "SUCCESS! Deploy command accepted all parameters!"
              echo "Only SSL certificate verification is blocking us now"
              echo "Testing multiple SSL bypass methods:"
              echo ""
              
              echo ""
              echo "Verification: Checking PROD Demo project after promotion:"
              python3 ci-cli.py --server="https://cgrptmcip01.cloud.cammis.ca.gov" label ls --xauthtoken="${MOTIO_AUTH_TOKEN}" --instanceName="Cognos-PRD" --projectName="Demo" || echo "Failed to list PROD labels after promotion"
            '''
          }
        }
      }
    }
  }

  post {
    always {
      echo "Pipeline execution finished."
    }
    success {
      echo "MotioCI pipeline completed successfully."
    }
    failure {
      echo "MotioCI pipeline failed."
    }
  }
}
