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
    MOTIO_SERVER = "https://cgrptmcip01.cloud.cammis.ca.gov"
  }
  
  options {
    disableConcurrentBuilds()
    timestamps()
  }

  stages {

    stage('Initialize') {
      steps {
        script {
          echo "Branch: ${env.GIT_BRANCH}"
    
    properties([
  parameters([

    //Source Environment
    [
      $class: 'ChoiceParameter',
      choiceType: 'PT_SINGLE_SELECT',
      name: 'SOURCE_ENV',
      description: 'Select Cognos Source Environment',
      script: [
        $class: 'GroovyScript',
        fallbackScript: [
          classpath: [], sandbox: true,
          script: "return ['Error loading environments']"
        ],
        script: [
          classpath: [], sandbox: true,
          script: """
            return ['Cognos-DEV/TEST', 'Cognos-SIT', 'Cognos-UAT']
          """
        ]
      ]
    ],

    //Target Environment (Reactive)
    [
      $class: 'CascadeChoiceParameter',
      choiceType: 'PT_SINGLE_SELECT',
      name: 'TARGET_ENV',
      description: 'Select Target Cognos Environment',
      referencedParameters: 'SOURCE_ENV',
      script: [
        $class: 'GroovyScript',
        fallbackScript: [
          classpath: [], sandbox: true,
          script: "return ['Error loading targets']"
        ],
        script: [
          classpath: [], sandbox: true,
          script: """
            if (SOURCE_ENV == 'Cognos-DEV/TEST') return ['Cognos-SIT','Cognos-UAT','Cognos-PRD']
            else if (SOURCE_ENV == 'Cognos-SIT') return ['Cognos-UAT','Cognos-PRD']
            else return ['Cognos-PRD']
          """
        ]
      ]
    ],

    //Dynamic Project List (from projects.txt)
    [
      $class: 'ChoiceParameter',
      choiceType: 'PT_SINGLE_SELECT',
      name: 'PROJECT_NAME',
      description: 'Select MotioCI Project (auto-loaded after first login)',
      script: [
        $class: 'GroovyScript',
        fallbackScript: [
          classpath: [], sandbox: true,
          script: "return ['(Run MotioCI Login once to fetch projects)']"
        ],
        script: [
          classpath: [], sandbox: true,
          script: """
            import java.nio.file.*
            def f = new File("${WORKSPACE}/projects.txt")
            if (f.exists()) {
              def lines = f.readLines().findAll { it?.trim() }
              if (lines) return lines
              else return ['(No projects found — rerun login)']
            } else {
              return ['(projects.txt not found — run MotioCI Login stage first)']
            }
          """
        ]
      ]
    ],

    //Dynamic Folder List (depends on Project)
    [
      $class: 'CascadeChoiceParameter',
      choiceType: 'PT_SINGLE_SELECT',
      name: 'OBJECT_PATH',
      description: 'Select Folder or Report Path (auto-loaded from folders.txt)',
      referencedParameters: 'PROJECT_NAME',
      script: [
        $class: 'GroovyScript',
        fallbackScript: [
          classpath: [], sandbox: true,
          script: "return ['(No folders found)']"
        ],
        script: [
          classpath: [], sandbox: true,
          script: """
            import java.nio.file.*
            def f = new File("${WORKSPACE}/folders.txt")
            if (f.exists()) {
              def lines = f.readLines().findAll { it?.trim() }
              if (lines) return lines
              else return ['(Empty — rerun login)']
            } else {
              return ['(folders.txt not found — run MotioCI Login)']
            }
          """
        ]
      ]
    ],

    //Manual Project & Path overrides
    [
      $class: 'DynamicReferenceParameter',
      name: 'PROJECT_NAME',
      description: 'Enter Project manually if not listed',
      defaultValue: ''
    ],
    [
      $class: 'DynamicReferenceParameter',
      name: 'OBJECT_PATH',
      description: 'Enter Folder Path manually if not listed',
      defaultValue: ''
    ],
    [
      $class: 'StringParameterDefinition',
      name: 'ROLLBACK_LABEL',
      defaultValue: '',
      description: 'Enter existing label name to redeploy'
    ]
  ])
])           
        echo """
                  ================================================
                  MotioCI → Cognos Deployment Pipeline (Enhanced)
                  ================================================
                  Source: ${params.SOURCE_ENV}
                  Target: ${params.TARGET_ENV}
                  Project: ${params.PROJECT_NAME}
                  Object Path: ${params.OBJECT_PATH}
                  Rollback Label: ${params.ROLLBACK_LABEL ?: "N/A"}
                  ================================================
                  """
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
              python3 ci-cli.py --server="$MOTIO_SERVER" \
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
              echo "Login successful"
            '''
          echo "Fetching available projects for ${SOURCE_ENV}..."
python3 ci-cli.py --server="$MOTIO_SERVER" \
  project ls --xauthtoken "$TOKEN" \
  --instanceName "${SOURCE_ENV}" > ../projects_raw.json


grep -o "'name': '[^']*'" ../projects_raw.json | cut -d"'" -f4 | sort | uniq > ../../projects.txt || true
echo "Saved project list to: $WORKSPACE/projects.txt"
head -n 10 ../../projects.txt || echo "(No projects found)"

if [ -n "${PROJECT_NAME:-}" ]; then
  echo "Fetching folders for project: ${PROJECT_NAME}"
  python3 ci-cli.py --server="$MOTIO_SERVER" \
    versionedItems ls --xauthtoken "$TOKEN" \
    --instanceName "${SOURCE_ENV}" \
    --projectName "${PROJECT_NAME}" > ../folders_raw.json || true

  grep "prettyPath" ../folders_raw.json | cut -d"'" -f4 | sort | uniq > ../../folders.txt || true
  echo "Saved folder list to: $WORKSPACE/folders.txt"
  head -n 10 ../../folders.txt || echo "(No folders found)"
else
  echo "Skipping folder discovery — PROJECT_NAME not provided yet."
fi

ls -lh ../../projects.txt ../../folders.txt || true
        }
      }
    }
}
stage('Prepare deployment') {
  when { expression { return !params.ROLLBACK_LABEL?.trim() } }
  steps {
    container('python') {
      sh '''
        set -e
        cd MotioCI/api/CLI

        TOKEN=$(cat ../token.txt)
        echo "Using MotioCI token (length: ${#TOKEN})"

        echo "Project: ${PROJECT_NAME}"
        echo "Object Path: ${OBJECT_PATH:-<none>}"

        # List all versioned items for the project
        echo "Discovering versioned items in project ${PROJECT_NAME}..."
        python3 ci-cli.py --server="$MOTIO_SERVER" \
          versionedItems ls \
          --xauthtoken "$TOKEN" \
          --instanceName "${SOURCE_ENV}" \
          --projectName "${PROJECT_NAME}" > items_full.out

        echo "Total items listed (raw): $(grep -c \"'id':\" items_full.out || true)"

        # ------------------------------------------------------------
        # Determine which IDs to label (whole project vs. specific path)
        # ------------------------------------------------------------
        if [ -z "${OBJECT_PATH}" ]; then
          echo "No OBJECT_PATH provided — deploying the entire project ${PROJECT_NAME}"
          grep "'id':" items_full.out | grep -v "instanceId" | grep -o "[0-9][0-9]*" \
            | paste -sd, - > ids.txt || true
        else
          echo "Filtering for path: ${OBJECT_PATH}"
          grep -A8 "prettyPath.: '${OBJECT_PATH}'" items_full.out > items.out || true
          grep "'id':" items.out | grep -v "instanceId" | grep -o "[0-9][0-9]*" \
            | paste -sd, - > ids.txt || true
        fi

        IDS=$(cat ids.txt || true)

        if [ -z "$IDS" ]; then
          echo "ERROR: No versioned items found for selection."
          echo "Hint: Check if the object is versioned or the path is correct."
          exit 1
        fi

        ID_COUNT=$(echo $IDS | tr ',' '\\n' | wc -l | tr -d ' ')
        echo "Found ${ID_COUNT} versioned item(s)."
        echo "Matched IDs: $IDS"

        # ------------------------------------------------------------
        # Create Deployment label for identified IDs
        # ------------------------------------------------------------
        VERSION_NAME="AutoLabel_${BUILD_NUMBER}_$(date +%Y%m%d_%H%M)"
        echo "Creating Deployment Label: $VERSION_NAME with IDs [$IDS]"
        python3 ci-cli.py --server="$MOTIO_SERVER" label create \
          --xauthtoken "$TOKEN" \
          --instanceName "${SOURCE_ENV}" \
          --projectName "${PROJECT_NAME}" \
          --name "$VERSION_NAME" \
          --versionedItemIds "[$IDS]"

        # ------------------------------------------------------------
        # Fetch and store Label ID
        # ------------------------------------------------------------
        python3 ci-cli.py --server="$MOTIO_SERVER" label ls \
          --xauthtoken "$TOKEN" \
          --instanceName "${SOURCE_ENV}" \
          --projectName "${PROJECT_NAME}" \
          --labelName "$VERSION_NAME" > label_info.out

        LABEL_ID=$(python3 -c "import ast; data=open('label_info.out').read(); \
          parsed=ast.literal_eval(data); \
          print(parsed['data']['instances']['edges'][0]['node']['projects']['edges'][0]['node']['labels']['edges'][0]['node']['id'])" \
          2>/dev/null || echo "")

        if [ -z "$LABEL_ID" ]; then
          echo "ERROR: Unable to retrieve label ID!"
          exit 1
        fi

        echo "$LABEL_ID" > ../label_id.txt
        echo "Label $VERSION_NAME (ID: $LABEL_ID) created successfully."

      '''
    }
  }
}
    
  stage('Deploy') {
      steps {
        container('python') {
          withCredentials([string(credentialsId: 'cognos-api-key-prd', variable: 'COGNOS_API_KEY_PRD')]) {
            sh '''
              set -e
              cd MotioCI/api/CLI

              # If rollback specified, skip label creation
              if [ -n "${ROLLBACK_LABEL}" ]; then
                echo "Using existing rollback label: ${ROLLBACK_LABEL}"
                echo "0" > ../label_id.txt
              fi

              TOKEN=$(cat ../token.txt)
              echo "Obtaining PROD CAMPassport..."
              BASE="https://dhcsprodcognos.ca.analytics.ibm.com/api/v1"
              echo "{\\"parameters\\":[{\\"name\\":\\"CAMAPILoginKey\\",\\"value\\":\\"$COGNOS_API_KEY_PRD\\"}]}" > login.json
              curl -sS -X PUT "$BASE/session" -H "Content-Type: application/json" -d @login.json -o session.json
              SESSION_KEY=$(python3 -c 'import json; print(json.load(open("session.json")).get("session_key",""))')
              SESSION_KEY=$(echo "$SESSION_KEY" | sed 's/^CAM[ ]*//')
              echo "✓ CAMPassport captured"

              if [ -n "${ROLLBACK_LABEL}" ]; then
                LABEL_NAME="${ROLLBACK_LABEL}"
                echo "Promoting rollback label ${ROLLBACK_LABEL}"
                DEPLOY_LABEL_NAME="Rollback_${BUILD_NUMBER}"
              else
                LABEL_ID=$(cat ../label_id.txt)
                LABEL_NAME=""
                DEPLOY_LABEL_NAME="PROMOTED_${BUILD_NUMBER}"
              fi

              echo "Deploying to ${TARGET_ENV}..."
              python3 ci-cli.py --server="$MOTIO_SERVER" deploy \
                --xauthtoken "$TOKEN" \
                --sourceInstanceName "${SOURCE_ENV}" \
                --targetInstanceName "${TARGET_ENV}" \
                --projectName "${PROJECT_NAME}" \
                ${LABEL_NAME:+--labelName "$LABEL_NAME"} \
                ${LABEL_ID:+--labelId "$LABEL_ID"} \
                --targetLabelName "$DEPLOY_LABEL_NAME" \
                --camPassportId "$SESSION_KEY" > deploy.out 2>&1 || true

              cat deploy.out
              if grep -q '"errors"' deploy.out; then echo "Deployment failed"; exit 1; fi
              echo "Deployment executed successfully."
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
