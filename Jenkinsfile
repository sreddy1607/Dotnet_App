/*
=======================================================================================
MotioCI → Cognos Automated Deployment Pipeline
Maintained by: DevOps Team
Purpose: Automate Cognos content promotion from DEV/TEST to PRD using MotioCI CLI.
=======================================================================================
*/

def branch = env.BRANCH_NAME ?: "DEV"
def namespace = env.NAMESPACE ?: "dev"
def cloudName = env.CLOUD_NAME == "openshift" ? "openshift" : "kubernetes"
def workingDir = "/home/jenkins/agent"

APP_NAME = "combined-devops-cognos-deployments"

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
            - name: varlibcontainers
              emptyDir: {}
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
 
  environment {
    GIT_BRANCH = "${BRANCH_NAME}"
  }

  options {
    disableConcurrentBuilds()
    timestamps()
  }

  stages {
    stage('Initialize') {
      steps {
        script {
          echo "================================================"
          echo "MotioCI → Cognos Deployment Pipeline"
          echo "================================================"
          echo "Branch: ${env.GIT_BRANCH}"
          echo "Build Number: ${BUILD_NUMBER}"
          echo "Initializing searchPath-based deployment..."
          echo "================================================"
        }
      }
    }

    stage('MotioCI Login') {
      steps {
        withCredentials([
          file(credentialsId: 'cognos-credentials', variable: 'CREDENTIALS_FILE')
        ]) {
          container('python') {
            sh '''
              set -euo pipefail
              cd MotioCI/api/CLI

              echo "Installing MotioCI CLI dependencies..."
              python3 -m pip install --user -r requirements.txt

              echo "Logging in to MotioCI with stored credentials file..."
              python3 ci-cli.py --server="https://cgrptmcip01.cloud.cammis.ca.gov" \
                login --credentialsFile "$CREDENTIALS_FILE" > login.out 2>&1 || true

              # Extract auth token from login output
              awk 'match($0,/(Auth[[:space:]]*[Tt]oken|x-auth_token|xauthtoken)[[:space:]]*[:=][[:space:]]*([A-Za-z0-9._-]+)/,m){print m[2]}' login.out | tail -n1 > login.token || true

              TOKEN=$(cat login.token 2>/dev/null || true)
              echo "MotioCI token captured (length: ${#TOKEN})"
             
              if [ -z "$TOKEN" ] || [ "${#TOKEN}" -lt 10 ]; then
                echo "ERROR: Failed to capture valid auth token!"
                echo "Login output:"
                cat login.out
                exit 1
              fi
             
              echo "$TOKEN" > ../token.txt
              echo "✓ Login successful"
            '''
          }
        }
      }
    }

    stage('Create Label with Admin Items') {
      steps {
        container('python') {
          sh '''
            set -euo pipefail
            cd MotioCI/api/CLI
          
            TOKEN=$(cat ../token.txt)
            VERSION_NAME="Admin-Deploy-${BUILD_NUMBER}"
          
            echo "Getting Admin item IDs..."
          
            # Get items - we know this works
            python3 ci-cli.py \
              --server="https://cgrptmcip01.cloud.cammis.ca.gov" \
              versionedItems ls \
              --xauthtoken "$TOKEN" \
              --instanceName "Cognos-DEV/TEST" \
              --projectName "Demo" \
              --searchPath "starts:/Team Content/MotioCI Reports/Admin" > items.out
          
            # Simple grep to get just ID numbers (avoid Python parsing)
            grep "'id':" items.out | grep -v "instanceId" | head -20 | grep -o "[0-9][0-9]*" | paste -sd, - > ids.txt
          
            IDS=$(cat ids.txt)
            echo "Creating label with IDs: [$IDS]"
          
            # Create label WITH items (your proven working command format)
            python3 ci-cli.py \
              --server="https://cgrptmcip01.cloud.cammis.ca.gov" \
              label create \
              --xauthtoken "$TOKEN" \
              --instanceName "Cognos-DEV/TEST" \
              --projectName "Demo" \
              --name "$VERSION_NAME" \
              --versionedItemIds "[$IDS]"
          
            echo "Label $VERSION_NAME created"
          
            # Get the label ID (your proven working extraction)
            python3 ci-cli.py \
              --server="https://cgrptmcip01.cloud.cammis.ca.gov" \
              label ls \
              --xauthtoken "$TOKEN" \
              --instanceName "Cognos-DEV/TEST" \
              --projectName "Demo" \
              --labelName "$VERSION_NAME" > label_info.out
          
            LABEL_ID=$(python3 -c "import ast; data=open('label_info.out').read(); parsed=ast.literal_eval(data); print(parsed['data']['instances']['edges'][0]['node']['projects']['edges'][0]['node']['labels']['edges'][0]['node']['id'])" 2>/dev/null || echo "")
          
            echo "Label ID: $LABEL_ID"
            echo "$LABEL_ID" > ../label_id.txt
          '''
        }
      }
    }

    stage('Retrieve CAMPASSPORT ID') {
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
{ "parameters": [ { "name": "CAMAPILoginKey", "value": "$COGNOS_API_KEY_PRD" } ] }
JSON

              curl --fail-with-body -sS -X PUT "$BASE/session" \
                -H "Content-Type: application/json" \
                -d @login.json -o session.json

              RAW_KEY=$(python3 -c 'import json; print(json.load(open("session.json")).get("session_key",""))')
              if [ -z "$RAW_KEY" ]; then
                echo "ERROR: No session_key from PROD Cognos."
                cat session.json || true
                exit 1
              fi

              # Strip CAM prefix if present
              SESSION_KEY=$(echo "$RAW_KEY" | sed 's/^CAM[ ]*//')

              echo "Cognos API session verified for PROD."
              printf "PROD_CAMPASSPORT='%s'\n" "$SESSION_KEY" > MotioCI/api/motio_env_prod
              echo "✓ Saved clean session key (no CAM prefix)"
            '''
          }
        }

        script {
          def envFile = readFile('MotioCI/api/motio_env_prod').trim()
          envFile.split("\n").each { line ->
            def (k, v) = line.split('=', 2)
            if (v.startsWith("'") && v.endsWith("'")) {
              v = v.substring(1, v.length() - 1)
            }
            env[k] = v
          }
          echo "Captured Cognos PROD Passport: ${env.PROD_CAMPASSPORT.take(15)}..."
        }
      }
    }

    stage('MotioCI Deploy (DEV → PRD)') {
      steps {
        container('python') {
          script {
            def sessionKey = env.PROD_CAMPASSPORT?.trim()
            if (!sessionKey) {
              error "Missing PROD_CAMPASSPORT"
            }

            sh """
              set -euo pipefail
              cd MotioCI/api/CLI

              TOKEN=\$(cat ../token.txt)
              SOURCE_LABEL_ID=\$(cat ../label_id.txt)

              echo "Promoting Label ID: \$SOURCE_LABEL_ID"

              python3 ci-cli.py \
                --server="https://cgrptmcip01.cloud.cammis.ca.gov" \
                deploy \
                --xauthtoken "\$TOKEN" \
                --sourceInstanceId 3 \
                --targetInstanceId 1 \
                --projectId 18 \
                --labelId "\$SOURCE_LABEL_ID" \
                --targetLabelName "PROMOTED-\${BUILD_NUMBER}" \
                --camPassportId "${sessionKey}" > deploy.out 2>&1 || true

              cat deploy.out
            
              if grep -q '"errors"' deploy.out; then
                exit 1
              fi
            """
          }
        }
      }
    }
  }

  post {
    always {
      echo "================================================"
      echo "Pipeline execution finished."
      echo "Build: ${BUILD_NUMBER}"
      echo "================================================"
    }
    success {
      echo "MotioCI pipeline completed successfully."
    }
    failure {
      echo "MotioCI pipeline failed. Review logs above."
    }
  }
}
