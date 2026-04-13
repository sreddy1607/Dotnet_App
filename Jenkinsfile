
    stage('Deploy') {
      steps {
        container(name: "aws-boto3") {
          script {
             sh """#!/bin/bash
            echo "Deploy Using AWS CodeDeploy"
            """
            withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'jenkins-ecr-ecs', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
              step([$class: 'AWSCodeDeployPublisher',
                  applicationName: "tar-etar-app-${env_deploy_env}",
                  awsAccessKey: "${AWS_ACCESS_KEY_ID}",
                  awsSecretKey: "${AWS_SECRET_ACCESS_KEY}",
                  credentials: 'awsAccessKey',
                  deploymentConfig: "tar-etar-app-${env_deploy_env}-config",
                  deploymentGroupAppspec: false,
                  deploymentGroupName: "tar-etar-app-${env_deploy_env}-INPLACE-deployment-group",
                  deploymentMethod: 'deploy',
                  excludes: '', iamRoleArn: '', includes: '**', pollingFreqSec: 15, pollingTimeoutSec: 900, proxyHost: '', proxyPort: 0,
                  region: 'us-west-2', s3bucket: 'dhcs-codedeploy-app', 
                  subdirectory: 'devops.ETAR/codedeploy', versionFileName: '', waitForCompletion: true])
            }
          } // end of script
        } // end of container

        container(name: "jnlp") {
          lock(resource: 'deployments-github-repo',inversePrecedence: false ) {
           dir("${WORKSPACE}/deployrepo"){
              withCredentials([usernamePassword(credentialsId: "github-key", usernameVariable: 'NUSER', passwordVariable: 'NPASS')]) {
                sh """
                  git clone https://${NUSER}:${NPASS}@github.com/ca-mmis/deployments-combined-devops.git --depth=1
                  git config  --global user.email "jenkins@cammis.com"
                  git config  --global user.name "jenkins"

                  cd deployments-combined-devops
                  git checkout master
                  git pull

                  cp ${WORKSPACE}/devops.ETAR/codedeploy/serverconfig/index.html ${WORKSPACE}/deployrepo/deployments-combined-devops/tar-etar-api/sandbox

                            
                    echo "Cammis.Surge.Api was built, need to update deployment repository"
                    echo "Comparing the directories with DIFF:"
                    set +e
                    diff -r ${WORKSPACE}/devops.ETAR/codedeploy/eTAR ${WORKSPACE}/deployrepo/deployments-combined-devops/tar-etar-api/sandbox/eTAR
                    set -e
                    # remove and replace deployment for eTAR
                    rm -r ${WORKSPACE}/deployrepo/deployments-combined-devops/tar-etar-api/sandbox/eTAR/*
                    cp -a ${WORKSPACE}/devops.ETAR/codedeploy/eTAR/. ${WORKSPACE}/deployrepo/deployments-combined-devops/tar-etar-api/sabdbox/eTAR/
                    rm ${WORKSPACE}/deployrepo/deployments-combined-devops/tar-etar-api/sandbox/eTAR/placeholder.txt
                    updates_to_deploy=true
                  

                  if [ "\$updates_to_deploy" = true ] ; then
                    touch tar-etar-api/updates_to_deploy
                  fi


                """
                
                script {
                   incrementVersion()
                }

                sh """
                  cd ${WORKSPACE}/deployrepo/deployments-combined-devops
                  if [ -f tar-etar-api/updates_to_deploy ] ; then
                    echo 'Pushing to the deployment repository'
                    rm tar-etar-api/updates_to_deploy
                    echo "Will tag deploy repo with: \"Updated build artifacts for tar-etar-api build\""
                    git add -Av
                    git commit -m "Updated build artifacts for tar-etar-api build"
                    git push https://${NUSER}:${NPASS}@github.com/ca-mmis/deployments-combined-devops.git
                  else
                    echo "Nothing needs to be pushed to deployment repository"
                  fi
                  pwd
                """
              } //end withCredentials
            } //end dir
          } //end lock
        }  //end container

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


def incrementVersion() {
  def versionInfo = readYaml file: "deployments-combined-devops/tar-etar-api/sandbox/release/version.yaml"
  def Integer newMinor = versionInfo.app.version.minor
  def Integer newMajor = versionInfo.app.version.major
  def Integer newPatch = versionInfo.app.version.patch
  
  if(env_release_type == "PATCH" ) {
    newPatch = newPatch+1
  } else if (env_release_type == "MINOR") {
    newMinor = newMinor+1
    newPatch = 0
  } else if (env_release_type == "MAJOR") {
    newMajor = newMajor+1
    newMinor = 0
    newPatch = 0
  }
  
  def updatedVersionInfo = versionInfo
  def buildDate = new Date()
  updatedVersionInfo.app.version.patch=newPatch
  updatedVersionInfo.app.version.major=newMajor
  updatedVersionInfo.app.version.full=updatedVersionInfo.app.version.major+"."+updatedVersionInfo.app.version.minor+"."+updatedVersionInfo.app.version.patch
  updatedVersionInfo.app.build.date=buildDate.format("yyyy-MM-dd_HH:mm")
  updatedVersionInfo.app.build.number="${BUILD_NUMBER}"
  updatedVersionInfo.app.build.commit="${env_current_git_commit}"
  println "Saving version.yaml file...\n${updatedVersionInfo}"
  writeYaml file: "deployments-combined-devops/tar-etar-api/sandbox/release/version.yaml", data: updatedVersionInfo, overwrite: true
}
