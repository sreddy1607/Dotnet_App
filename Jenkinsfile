/*
=======================================================================================
This file is being updated constantly by the DevOps team to introduce new enhancements
based on the template.  If you have suggestions for improvement,
please contact the DevOps team so that we can incorporate the changes into the
template.  In the meantime, if you have made changes here or don't want this file to be
updated, please indicate so at the beginning of this file.
=======================================================================================
*/

def branch = env.BRANCH_NAME ?: "Dev"
def workingDir = "/home/jenkins/agent"

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
    timeout(time:5 , unit: 'HOURS')
    skipDefaultCheckout()
    buildDiscarder(logRotator(numToKeepStr: '20'))
  }

  environment {
    env_current_git_commit=""
    env_accesskey=""
    env_secretkey=""
    env_tag_name=""
    env_deploy_env=""
    env_DEPLOY_CONFIG="true"
  }

  stages {
    stage("initialize") {
      steps {
        container(name: "node") {
          script {

            properties([
              parameters([
                choice(name: 'DEPLOY_ENV', choices: ['NONE','SBX','HFX'], description: 'Deployment Environment'),
              ])
            ])
             WHEN SBX SELECTED II SHOULD BE EQUAL TO DEV 
             WHEN HFX SELECTED IT SHOULD BE EQUAL TO SIT
            // SURGE_ENV = params.DEPLOY_ENV
            SURGE_ENV = params.DEPLOY_ENV

            deleteDir()

            checkout(scm).GIT_COMMIT

            echo "Current deployment environment is ${SURGE_ENV}"
          } //END script
        } //END container node
      } //END steps
    } //END stage

    stage('Prepare Deployment') {
      when {
        expression {
          SURGE_ENV != "NONE"
        }
      }
      steps {
        container(name: "aws-boto3") {
          script {
            sh """#!/bin/bash
              echo "Setting up app directories with files, or deployment will fail"
              mkdir devops/codedeploy/surgeapi
              touch devops/codedeploy/surgeapi/placeholder.txt
              
              
              echo "Update after-install.bat to deploy config"
              sed -i "s,{DEPLOY_CONFIG},${env_DEPLOY_CONFIG}," devops/codedeploy/after-install.bat
              sed -i "s,{server-environment},${SURGE_ENV}," devops/codedeploy/serverconfig/index.html
            """
          } // end of script
        } // end of container
      } // end of steps
    }  // end of Prepare Deployment Stage

    stage('Deploy') {
      when {
        expression {
          SURGE_ENV != "NONE"
        }
      }
      steps {
        container(name: "aws-boto3") {
          script {
            echo "Deploy to Non-DR"

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

            if ("${SURGE_ENV}" != "DEV") {
              echo "Deploy to DR"
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
            }
          } // end of script
        } // end of container
      } // end of steps
    } // end of Deploy stage
  } // end of stages

  //pipeline post actions
  post {
    always {
        echo "Build Process complete."
    } // always

    success {
        echo "Build Process was success."
    } //success

    unstable {
        echo "Build is unstable."
    } // unstable

    aborted {
        echo "Pipeline aborted."
    } // aborted

    failure {
        echo "Build encountered failures ."
    } // failure

    changed {
        echo "Build content was changed."
    } // changed

  } // post
}
