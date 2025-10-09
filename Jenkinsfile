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
    container('python') {
      script {
        sh '''
set -euo pipefail
cd MotioCI/api/CLI

echo "Installing MotioCI CLI dependencies..."
python3 -m pip install --user -r requirements.txt

echo "Creating credentials JSON for DEV/TEST and PRD..."
cat <<ENDJSON > creds.json
[
  {
    "instanceId": "1",
    "apiKey": "AWlGMEQ4OUM2RkIyQzM0OUIzQTBFMEQ1OUM5MzRCM0M3RYJm/hgt2Duf9rDSo6EiYmE1RaWG"
  },
  {
    "instanceId": "3",
    "apiKey": "AWlFMTc2QUMzM0YwM0E0RTg4OUJDQUIyMTIzNjY2NEI5NZTADudaMR2xZKCPVFaRLu2/LEp5"
  }
]
ENDJSON

echo "Logging in to MotioCI..."
python3 ci-cli.py \
  --server="https://cgrptmcip01.cloud.cammis.ca.gov" \
  login --credentialsFile creds.json > login.out 2>&1 || true

echo "=== login.out (first 40 lines) ==="
sed -n '1,40p' login.out || true
echo "================================="

# Extract Auth Token
awk 'match($0,/(Auth[[:space:]]*[Tt]oken|x-auth_token|xauthtoken)[[:space:]]*[:=][[:space:]]*([A-Za-z0-9._-]+)/,m){print m[2]}' login.out | tail -n1 > login.token || true

TOKEN=$(cat login.token 2>/dev/null || true)

echo "MotioCI token captured (len=${#TOKEN})"
echo "$TOKEN" > ../token.txt

          
        '''
      }
    }
  }
}

   stage('Auth: Cognos API session (PROD)') {
      steps {
        container('python') {
          withCredentials([string(credentialsId: 'cognos-api-key-prd', variable: 'COGNOS_API_KEY_PRD')]) {
            sh '''
              set -eu
              echo "Starting Cognos API session (PROD)..."
              BASE="https://dhcsprodcognos.ca.analytics.ibm.com/api/v1"

              rm -f login.json session.json || true
              mkdir -p MotioCI/api

              cat > login.json <<JSON
{ "parameters": [ { "name": "CAMAPILoginKey", "value": "AWlGMEQ4OUM2RkIyQzM0OUIzQTBFMEQ1OUM5MzRCM0M3RYJm/hgt2Duf9rDSo6EiYmE1RaWG" } ] }
JSON

              curl --fail-with-body -sS -X PUT "$BASE/session" \
                   -H "Content-Type: application/json" \
                   -d @login.json -o session.json

              SESSION_KEY=$(python3 -c 'import json; print(json.load(open("session.json")).get("session_key",""))')
              if [ -z "$SESSION_KEY" ]; then
                echo "ERROR: No session_key from PROD Cognos."
                cat session.json || true
                exit 1
              fi

              case "$SESSION_KEY" in
                "CAM "*) AUTH_VALUE="$SESSION_KEY" ;;
                "CAM"*)  AUTH_VALUE="$SESSION_KEY" ;;
                *)       AUTH_VALUE="CAM $SESSION_KEY" ;;
              esac

              echo "✅ Cognos API session verified for PROD."
              printf "PROD_CAMPASSPORT='%s'\n" "$AUTH_VALUE" > MotioCI/api/motio_env_prod
            '''
          }
        }
        script {
          def envFile = readFile('MotioCI/api/motio_env_prod').trim()
          envFile.split("\n").each { line ->
            def (k,v) = line.split('=', 2)
            if (v.startsWith("'") && v.endsWith("'")) {
              v = v.substring(1, v.length()-1)
            }
            env[k] = v
          }
          echo "Captured Prod Passport: ${env.PROD_CAMPASSPORT.take(15)}..."
        }
      }
    }

stage('MotioCI Token Debug') {
  steps {
    container('python') {
      sh '''
set -euo pipefail
cd MotioCI/api/CLI
TOKEN=$(cat ../token.txt)
echo "Testing token: ${TOKEN:0:6}... (len=${#TOKEN})"

echo "=== Listing instances ==="
python3 ci-cli.py --server="https://cgrptmcip01.cloud.cammis.ca.gov" \
  instance ls --xauthtoken "$TOKEN" || true

echo "=== Listing projects (DEV/TEST) ==="
python3 ci-cli.py --server="https://cgrptmcip01.cloud.cammis.ca.gov" \
  project ls --instanceName "Cognos-DEV/TEST" --xauthtoken "$TOKEN" || true

echo "=== Listing projects (PRD) ==="
python3 ci-cli.py --server="https://cgrptmcip01.cloud.cammis.ca.gov" \
  project ls --instanceName "Cognos-PRD" --xauthtoken "$TOKEN" || true
  
 
      '''
    }
  }
}
stage('MotioCI Deploy (DEV → PRD)') {
  steps {
    container('python') {
      script {
        sh '''
set -euo pipefail
cd MotioCI/api/CLI

# Read token captured during login
TOKEN=$(cat ../token.txt)

# Use label ID from DEV/TEST that want to promote

SOURCE_LABEL_ID=57

echo "=== Starting Promotion from DEV/TEST → PRD ==="
echo "Using token: ${TOKEN:0:6}... (len=${#TOKEN})"
echo "Promoting Label ID: $SOURCE_LABEL_ID from DEV/TEST to PRD"

python3 ci-cli.py \
  --server="https://cgrptmcip01.cloud.cammis.ca.gov" \
  deploy \
  --xauthtoken "$TOKEN" \
  --sourceInstanceId 3 \
  --targetInstanceId 1 \
  --projectName "Demo" \
  --labelId "$SOURCE_LABEL_ID" \
  --targetLabelName "PROMOTED-${BUILD_NUMBER}" \
  --camPassportId "$SESSION_KEY" > deploy.out 2>&1 || true

echo "=== Deploy Output (first 100 lines) ==="
sed -n '1,100p' deploy.out || true
echo "======================================="

# check for any obvious GraphQL errors
if grep -q '"errors"' deploy.out; then
  echo " MotioCI Deploy failed — see deploy.out above for details."
  exit 1
else
  echo " MotioCI Deploy stage completed successfully."
fi
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
