// Jenkinsfile (hardened & non-interactive)
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
        # Make requests trust the mounted CA bundle (no -k)
        - name: REQUESTS_CA_BUNDLE
          value: "/etc/pki/tls/certs/ca-bundle.crt"
        - name: SSL_CERT_FILE
          value: "/etc/pki/tls/certs/ca-bundle.crt"
        # Non-interactive mode signal for the CLI
        - name: CI
          value: "1"
      volumeMounts:
        - name: jenkins-trusted-ca-bundle
          mountPath: /etc/pki/tls/certs
"""
    }
  }

  environment {
    GIT_BRANCH = "${BRANCH_NAME}"
    MOTIO_SERVER = "https://cgrptmcip01.cloud.cammis.ca.gov"

    // Source/Target config
    SRC_INSTANCE_NAME = "Cognos-DEV/TEST"
    SRC_INSTANCE_ID   = "3"
    TGT_INSTANCE_NAME = "Cognos-PRD"
    TGT_INSTANCE_ID   = "1"
    PROJECT_NAME      = "Demo"
    SOURCE_LABEL_ID   = "57"
    TARGET_LABEL_NAME = "PROMOTED-20250712-115"

    
    NAMESPACE_ID      = "AzureAD"
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
            set -e
            echo "Checking for Python3..."
            which python3 || true
            python3 --version || true
          '''
        }
      }
    }

    stage('Install CLI deps') {
      steps {
        container('python') {
          sh '''
            set -e
            cd MotioCI/api/CLI
            python3 -m pip install --user -r requirements.txt
            echo "Dependencies installed."
          '''
        }
      }
    }

stage('MotioCI Login') {
  steps {
    withCredentials([file(credentialsId: 'prod-credentials-json', variable: 'CREDENTIALS_FILE')]) {
      container('python') {
        sh '''
          set -e
          cd MotioCI/api/CLI
          python3 -m pip install --user -r requirements.txt >/dev/null 2>&1 || true

          # Capture ONLY the token (our ci-cli.py now prints just the token on success)
          TOKEN=$(python3 ci-cli.py --server="https://cgrptmcip01.cloud.cammis.ca.gov" \
                    --non-interactive login --credentialsFile "$CREDENTIALS_FILE" \
                    | tail -n1 | tr -d '\\r')

          if [ -z "$TOKEN" ]; then
            echo "ERROR: Empty MotioCI token." >&2
            exit 1
          fi

          # Export for later stages
          echo "TOKEN=$TOKEN" > ../motio_env
        '''
      }
      script {
        def envFile = readFile('MotioCI/api/motio_env').trim()
        for (pair in envFile.split("\n")) {
          def (k,v) = pair.split("=", 2)
          env[k] = v
        }
        echo "MotioCI login completed - token captured."
      }
    }
  }
}

stage('Debug Namespaces') {
  steps {
    container('python') {
      sh '''
        echo "Checking available namespaces for PRD instance..."
        curl -sk -X POST "https://cgrptmcip01.cloud.cammis.ca.gov/api/graphql" \
          -H "Content-Type: application/json" \
          -H "x-auth-token: ${TOKEN}" \
          -d '{
            "query":"query($id: Long!){ instance(id:$id){ namespaces { id name } } }",
            "variables":{"id":1}
          }' | jq .
      '''
    }
  }
}

stage('Deploy') {
  steps {
    withCredentials([usernamePassword(credentialsId: 'Cognosserviceaccount', usernameVariable: 'COG_USER', passwordVariable: 'COG_PASS')]) {
      container('python') {
        sh '''
          set -euo pipefail
          cd MotioCI/api/CLI

          echo "Sanity: list projects on Cognos-PRD..."
          python3 ci-cli.py --server="https://cgrptmcip01.cloud.cammis.ca.gov" \
            project ls --xauthtoken="${TOKEN}" --instanceName="Cognos-PRD"

          # Do the deployment (adjust ids/names as needed)
          python3 ci-cli.py --server="https://cgrptmcip01.cloud.cammis.ca.gov" \
            --non-interactive deploy \
            --xauthtoken="${TOKEN}" \
            --sourceInstanceId=3 \
            --targetInstanceId=1 \
            --labelId=57 \
            --projectName="Demo" \
            --targetLabelName="PROMOTED-20250712-115" \
            --camPassportId="MTsxMDE6NmQxNzBlODYtMTJhZS0yMjgxLWY0ZjktMmZmMDgxMjIwNzY2OjI3NTU2MjA2NjQ7MDszOzA7" \
            --namespaceId="AzureAD"

          echo "Verification: labels after deployment"
          python3 ci-cli.py --server="https://cgrptmcip01.cloud.cammis.ca.gov" \
            label ls --xauthtoken="${TOKEN}" --instanceName="Cognos-PRD" --projectName="Demo" \
            | tee verify_labels.json
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
