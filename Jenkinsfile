/*
=======================================================================================
This file is being updated constantly by the DevOps team to introduce new enhancements
based on the template.  If you have suggestions for improvement,
please contact the DevOps team so that we can incorporate the changes into the
template.  In the meantime, if you have made changes here or don't want this file to be
updated, please indicate so at the beginning of this file.
=======================================================================================
*/

def branch = env.BRANCH_NAME ?: "master"
def workingDir = "/home/jenkins/agent"

def DEPLOY_FROM_ENV = [
    "dev":"N/A",
    "sit":"dev",
    "uat":"sit",
    "prd":"uat"
  ]

def SURGE_ENV

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
            - name: dotnet
              image: 136299550619.dkr.ecr.us-west-2.amazonaws.com/cammismspapp:1.0.34
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
              image: registry.access.redhat.com/ubi8/nodejs-18:latest
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
            - name: aws-boto3
              image: 136299550619.dkr.ecr.us-west-2.amazonaws.com/cammisboto3:1.0.1
              tty: true
              command: ["/bin/bash"]
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
      """
    }
  }

options {
    timestamps()
    disableConcurrentBuilds()
    timeout(time: 3, unit: 'HOURS')
    skipDefaultCheckout()
    buildDiscarder(logRotator(numToKeepStr: '20'))
  }

  environment {
    env_promotion_to_environment = ""
    env_promotion_from_environment = ""
  }

  stages {
    stage("Initialize") {
      steps {
        container("node") {
          script {
            properties([
              parameters([
                choice(name: 'PROMOTE_TO_ENV', choices: ['sit','uat','prd'], description: 'Target environment to promote to')
              ])
            ])

            env_promotion_to_environment = params.PROMOTE_TO_ENV
            env_promotion_from_environment=DEPLOY_FROM_ENV["${env_promotion_to_environment}"]

            deleteDir()

            checkout(scm).GIT_COMMIT

            echo "Promoting to environment: ${env_promotion_to_environment}"
            echo "Promoting from environment: ${env_promotion_from_environment}"
          }
        }
      }
    }

    stage("Prepare Artifacts") {
      steps {
        container("node") {
          script {
            sh """
              set -e
              # Clone deployments-combined-devops repo
              git clone https://github.com/ca-mmis/deployments-combined-devops.git
              cd deployments-combined-devops
              git checkout master
              git pull

              mkdir -p ../devops/codedeploy/SurgeUpdate

              # Unzip DEV SurgeUpdate package
              unzip tar-surge-client/dev/SurgeUpdate_DEV.ZIP -d tmp/SurgeUpdate

              # Overlay configs for target env
              cp ../tar-surge-client/<whatever dev cerates>/config/${env_promotion_to_environment.toUpperCase()}/* tmp/SurgeUpdate/

              # Re-zip with target env name
              cd tmp
              zip -r ../devops/codedeploy/SurgeUpdate/SurgeUpdate_${env_promotion_to_environment.toUpperCase()}.ZIP SurgeUpdate
              cd ..

              # Copy Version.TXT from DEV
              cp tar-surge-client/dev/Version.TXT ../devops/codedeploy/SurgeUpdate/
            """
          }
        }
      }
    }

    stage("Update Deployment Repo") {
      steps {
        container("aws-boto3") {
          script {
            lock(resource: 'tar-surge-client-deployment', inversePrecedence: false) {
              dir("${WORKSPACE}/deploytarget") {
                withCredentials([usernamePassword(credentialsId: "github-key", usernameVariable: 'NUSER', passwordVariable: 'NPASS')]) {
                  sh """
                    set -e
                    echo "Cloning tar-surge-client-deployment..."
                    git clone https://${NUSER}:${NPASS}@github.com/ca-mmis/tar-surge-client-deployment.git
                    cd tar-surge-client-deployment
                    git config --global user.email "jenkins@cammis.com"
                    git config --global user.name "jenkins"
                    git checkout master
                    git pull

                    ZIP_NAME=SurgeUpdate_${env_promotion_to_environment.toUpperCase()}.ZIP
                    echo "Updating deployment repo with \$ZIP_NAME..."
                    rm -f tar-surge-client/\$ZIP_NAME
                    cp ${WORKSPACE}/devops/codedeploy/SurgeUpdate/\$ZIP_NAME tar-surge-client/

                    git add tar-surge-client/\$ZIP_NAME
                    git commit -m "Deploy \$ZIP_NAME from ${env_promotion_to_environment} promotion" || true
                    git push origin master

                    commitId=\$(git rev-parse --short=8 HEAD)
                    dateTime=\$(git show -s --format=%cd --date=format:%Y-%m-%d_%H-%M-%S \$commitId)
                    commitTag="Deployed_to_${env_promotion_to_environment}_\${commitId}_\$dateTime"
                    git tag -f -a "\$commitTag" -m "Deployment tag for \$ZIP_NAME" "\$commitId"
                    git push origin master --tags
                  """
                }
              }
            }
          }
        }
      }
    }
         
 stage('Deploy') {
      steps {
        container(name: "aws-boto3") {
          script {
            echo "Deploy Using AWS CodeDeploy"

            SURGE_ENV = "${env_promotion_to_environment}".toUpperCase()

            echo "Here is the environment to go to: ${SURGE_ENV}"

            echo "Deploying to Non-DR"

            withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'jenkins-ecr', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
              step([$class: 'AWSCodeDeployPublisher',
                  applicationName: "tar-surge-app-${SURGE_ENV}",
                  awsAccessKey: "${AWS_ACCESS_KEY_ID}",
                  awsSecretKey: "${AWS_SECRET_ACCESS_KEY}",
                  credentials: 'awsAccessKey',
                  deploymentConfig: "tar-surge-app-${SURGE_ENV}-config",
                  deploymentGroupAppspec: false,
                  deploymentGroupName: "tar-surge-app-${SURGE_ENV}-INPLACE-deployment-group",
                  deploymentMethod: 'deploy',
                  excludes: '', iamRoleArn: '', includes: '**', pollingFreqSec: 15, pollingTimeoutSec: 900, proxyHost: '', proxyPort: 0,
                  region: 'us-west-2', s3bucket: 'dhcs-codedeploy-app', 
                  subdirectory: 'devops/codedeploy', versionFileName: '', waitForCompletion: true])
            }

            echo "Deploying to DR"

            withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'jenkins-ecr', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
              step([$class: 'AWSCodeDeployPublisher',
                  applicationName: "tar-surge-app-${SURGE_ENV}-DR",
                  awsAccessKey: "${AWS_ACCESS_KEY_ID}",
                  awsSecretKey: "${AWS_SECRET_ACCESS_KEY}",
                  credentials: 'awsAccessKey',
                  deploymentConfig: "tar-surge-app-${SURGE_ENV}-DR-config",
                  deploymentGroupAppspec: false,
                  deploymentGroupName: "tar-surge-app-${SURGE_ENV}-DR-INPLACE-deployment-group",
                  deploymentMethod: 'deploy',
                  excludes: '', iamRoleArn: '', includes: '**', pollingFreqSec: 15, pollingTimeoutSec: 900, proxyHost: '', proxyPort: 0,
                  region: 'us-east-1', s3bucket: 'dhcs-codedeploy-app-dr', 
                  subdirectory: 'devops/codedeploy', versionFileName: '', waitForCompletion: true])
            }
          } // end of script
        } // end of container
      } // end of steps
    } // end of Deploy stage
  }

  post {
    always { echo "Promotion pipeline complete." }
    success { echo "Promotion succeeded." }
    failure { echo "Promotion failed." }
  }
}
