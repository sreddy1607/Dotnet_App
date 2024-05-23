/*
=======================================================================================
This file is being updated constantly by the DevOps team to introduce new enhancements
based on the template for ngnix apps.  If you have suggestions for improvement,
please contact the DevOps team so that we can incorporate the changes into the
template.  In the meantime, if you have made changes here or don't want this file to be
updated, please indicate so at the beginning of this file.
=======================================================================================
*/

/*
naming convention:
    APP_NAME - all cap variables are either from Jenkinsfile.properties or jenkins built-in variables
               or pipeline parameters.
    g_stage_index - variables starting with "g_" are global variables declared in this file
    env_git_branch_type - variables starting with "env_" are declared in the environment section
*/

//this points to the current type of environment the build is supposed to be deployed and tested.
//BRANCHES[env_git_branch_type].stages[g_stage_index]
//should be part of environment. but env variables can't be integer
g_stage_index=0
g_my_docker_image=null
//namespace array for an env type
g_namespaces=[]

// variables from ibm template
 def branch = env.BRANCH_NAME ?: "master"
 def namespace = env.NAMESPACE ?: "dev"
 def cloudName = env.CLOUD_NAME == "openshift" ? "openshift" : "kubernetes"
 def workingDir = "/home/jenkins/agent"

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
          containers:
            - name: jnlp
              securityContext:
                privileged: true
              envFrom:
                - configMapRef:
                    name: jenkins-agent-env
                    optional: true
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
            - name: dotnet
              image: registry.access.redhat.com/ubi8/dotnet-60
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
            - name: buildah
              image: 136299550619.dkr.ecr.us-west-2.amazonaws.com/cammisbuildah:1.0
              tty: true
              command: ["/bin/bash"]
              workingDir: ${workingDir}
              envFrom:
                - configMapRef:
                    name: jenkins-agent-env
                    optional: true
              securityContext:
                privileged: true
              env:
                - name: HOME
                  value: /home/devops
                - name: ENVIRONMENT_NAME
                  value: ${env.NAMESPACE}
                - name: DOCKERFILE
                  value: ./Dockerfile
                - name: CONTEXT
                  value: .
                - name: TLSVERIFY
                  value: "false"
              volumeMounts:
                - mountPath: /var/lib/containers
                  name: varlibcontainers
            - name: aws-cli
              image: 136299550619.dkr.ecr.us-west-2.amazonaws.com/cammiscloud:1.12
              tty: true
              command: ["/bin/bash"]
              workingDir: ${workingDir}
              envFrom:
                - configMapRef:
                    name: jenkins-agent-env
                    optional: true
              env:
                - name: CHART_NAME
                  value: base
                - name: CHART_ROOT
                  value: chart
                - name: TMP_DIR
                  value: .tmp
                - name: HOME
                  value: /home/devops
                - name: ENVIRONMENT_NAME
                  value: ${env.NAMESPACE}
                - name: BRANCH
                  value: ${branch}
      """
    }
  }

  options {
    timestamps()
    disableConcurrentBuilds()
    timeout(time:5 , unit: 'HOURS')
    skipDefaultCheckout()
    buildDiscarder(logRotator(numToKeepStr: '20'))
    //sendSplunkConsoleLog()
  }

  environment {
    env_git_branch_type="feature"
    env_git_branch_name=""
    env_target_env_type=""
    env_target_namespace=""
    env_image_namespace=""
    env_image_fullspec=""
    env_kube_config_creds_id=""
    env_selected_jenkins_node=""
    env_current_git_commit=""
    env_skip_build="false"
    env_com_automation="com-automation"
    env_skip_smoke="false"
    env_skip_regression="false"
    env_skip_e2e="false"
    env_git_repo_url=""
    env_skip_sb_ut="false"
    env_sonar_props=""
    env_archive_artifacts="false"
    env_stage_name=""
    env_step_name=""
    env_git_tag_name=""
    env_startup_args_wget=""
    env_release_type=""
    //Following 2 variables added for argocd
    env_image_id=""
    env_deployment_yaml_path=""
    env_cluster_subdomain="${CLUSTER_SUBDOMAIN}"
    env_sonar_cli_version="${SONAR_CLI_VERSION}"
    env_cluster_env=""
    env_region_sn=""
    env_mcweb_env=""
	}

  stages {
    stage("initialize") {
      steps {
        container(name: "node") {
          script {
            properties([
              parameters([
                  [
                    $class: 'ChoiceParameter',
                    choiceType: 'PT_SINGLE_SELECT',
                    name: 'SOURCE_BRANCHNAME',
                    script: [
                        $class: 'GroovyScript',
                        fallbackScript: [
                            classpath: [],
                            sandbox: true,
                            script: 
                                "return ['error']"
                        ], 
                        script: [
                            classpath: [],
                            sandbox: true,
                            script: """
                                return['${env.BRANCH_NAME}']
                            """
                        ]
                    ]
                  ],
                  [   $class: 'ChoiceParameter', 
                      choiceType: 'PT_SINGLE_SELECT', 
                      name: 'TARGET_ENVIRONMENT', 
                      script: [
                          $class: 'GroovyScript', 
                          fallbackScript: [
                              classpath: [], 
                              sandbox: true, 
                              script: 
                                  "return['Could not get The environemnts']"
                          ], 
                          script: [
                              classpath: [], 
                              sandbox: true,
                              script: """
                                 if ('${env.BRANCH_NAME}'.contains('sandbox')){
                                     return['sandbox:selected']
                                    }
                                 else if('${env.BRANCH_NAME}'.contains('master')){
                                     return['dev:selected']
                                    }
                                """


                          ]
                      ]
                  ],
                  [     $class: 'ChoiceParameter', 
                        choiceType: 'PT_CHECKBOX', 
                        name: 'OPENSHIFT_NAMESPACES', 
                        script: 
                            [$class: 'GroovyScript', 
                            fallbackScript: [
                                    classpath: [], 
                                    sandbox: true, 
                                    script:
                                        "return['Could not get The namespaces']"
                                    ], 
                            script: [
                                    classpath: [], 
                                    sandbox: true,
                                    script: """
                                        if ('${env.BRANCH_NAME}'.contains('sandbox')){
                                            return['${env.BRANCH_NAME}:selected']
                                            }
                                        else if('${env.BRANCH_NAME}'.equals('master')){
                                            return['dev:selected']
                                            }
                                        """
                              ] 
                      ]
                  ],
                choice(name: 'RELEASE_TYPE', choices: ['PATCH','MINOR','MAJOR'], description: 'Enter Release type'),
                booleanParam(name: 'USE_GIT_TAG', defaultValue: false, description: 'Use the selected git tag instead of LATEST commit'),
                gitParameter(name: 'GIT_TAG', defaultValue: 'detec-service_deployed_in_dev_from_master', description: 'git tag', type: 'PT_TAG'),
                string(name: 'RELEASE',defaultValue: 'enter release name (Release-1.2.3)', description: 'Enter release name (overrides default config)'),
                string(name: 'GIT_SHA',defaultValue: 'enter git sha(8+ chars)', description: 'enter git sha that you want to deploy')
              ])
             ])

            env_stage_name = "initialize"
            env_step_name = "checkout"

            deleteDir()

            echo 'checkout source  and get the commit id'
            env_current_git_commit = checkout(scm).GIT_COMMIT

            //env_git_repo_url = sh(returnStdout: true, script: 'git config remote.origin.url').trim()
            env_git_repo_url = scm.userRemoteConfigs[0].url
            echo "Git repo URL: ${env_git_repo_url}"
            echo 'Loading properties file'
            env_step_name = "load properties"
            // load the pipeline properties
            load("devops/jenkins/Jenkinsfile.properties")

            echo "The cluster subdomain is ${env_cluster_subdomain}"

            env_step_name = "set global variables"
            echo 'initialize slack channels and tokens'
            initSlackChannels()

            echo 'set branch name'
		        echo "BRANCH_NAME: --- ${BRANCH_NAME}"
            env_git_branch_name = BRANCH_NAME
            echo 'Source branch'
            echo params.SOURCE_BRANCHNAME
            echo 'Target enviroment'
            echo params.TARGET_ENVIRONMENT

            echo ' capture the selected jenkins node and use it for every thing in the pipeline'

            env_selected_jenkins_node=NODE_NAME

            env_git_tag_name = params.GIT_TAG

            // override PO acceptance of build
            // by default, PO always checks the build in qa

            //set default image name space
            //change it to SANDBOX_IMAGE_SPACE if it's a feature branch
            env_image_namespace=NON_SANDBOX_IMAGE_SPACE

            //set branch type (master, develop,feature?)
            BRANCHES.each {key, value ->
                if ( value.branches.contains(env_git_branch_name) || env_git_branch_name.contains(key))
                    env_git_branch_type=key
            }

            if ( ! params.TARGET_ENVIRONMENT.contains("Choose") ){
                 KUBE_ENVS[params.TARGET_ENVIRONMENT].namespaces = params.OPENSHIFT_NAMESPACES.tokenize(",")
                 BRANCHES[env_git_branch_type].stages = params.TARGET_ENVIRONMENT.tokenize(",")
            }

            //override release name
            if ( ! params.RELEASE.contains("enter") )
                RELEASE_NAME=params.RELEASE
                // Release type - MAJOR/MINOR/PATCh
                env_release_type=params.RELEASE_TYPE

            // do we want to deploy a specific commit?
            if ( ! params.GIT_SHA.contains("enter") ) {
                env_step_name = "checkout non-latest"
                // if you choose a sha to deploy, shouldn't need to build again
                env_skip_build="true"
                env_current_git_commit=params.GIT_SHA

                //get ready to check out the commit for the sha
				    name_value=env_current_git_commit

                    //override earlier checked out source
                    checkout([
                        $class: 'GitSCM',
                        branches: [[name: "${name_value}"]],
                        doGenerateSubmoduleConfigurations: false,
                        extensions: [[$class: 'CloneOption', noTags: false, reference: '', shallow: true]],
                        submoduleCfg: [],
                        userRemoteConfigs: [[credentialsId: "${SSH_AGENT_GIT_ID}", url: "${env_git_repo_url}"]]
                    ])
                }

            // get the short version of commit
            env_current_git_commit="${env_current_git_commit[0..7]}"

            //include commit id in build name
            currentBuild.displayName = "#${BUILD_NUMBER} --- ${env_current_git_commit}"

            //set the values for the initial environment for deployment and tests
            setupForNextStage(g_stage_index,env_git_branch_type)
            slackNotification("pipeline","${APP_NAME}-${env_git_branch_name}: <${BUILD_URL}console|build #${BUILD_NUMBER}> started.","#439FE0","false")
          } //END script
        } //END container node
      } //END steps
    } //END stage

    stage('dotnet compile/unit tests') {
      when {
        expression {
          env_skip_build=="false"
        }
      }
      steps {
        container(name: "dotnet") {
          script {
            env_stage_name = 'dotnet compile/unit tests'
            env_step_name = "dotnet unit tests"

            sh """
      			      #!/bin/bash

                  pwd
                  #ls -l
                  dotnet restore "./provider-portal-detec-service.csproj"
               """
            def testResults = sh returnStdout: true, script: """
                  set +e
                  cd UnitTests/provider-portal-detec-service.tests
                  dotnet test
                  set -e
               """
            writeFile file: "devops/testResults.txt", text: testResults
            //def buildResults = sh returnStdout: true, script: "npm run build --if-present"
            //echo "Test results available from build job home page.\n\nBuild Results:\n${buildResults}"

            publishHTML (target: [
                allowMissing: true,
                alwaysLinkToLastBuild: false,
                keepAll: false,
                reportDir: 'devops',
                reportFiles: 'testResults.txt',
                reportName: "Unit Test Results"
              ])
          }
        }
      }
   }

    stage('build image') {
      when {
        expression {
          env_skip_build=="false" && (env_git_branch_type != "feature")
        }
      }
      steps {
        container(name:"buildah") {
          script {
            env_stage_name = 'build image'
            env_step_name = "build"
            APP_IMAGE="${IMAGE_REGISTRY}/${env_image_namespace}/${APP_NAME}:${env_git_branch_name}_${BUILD_NUMBER}_${env_current_git_commit}"
            if ( env_git_branch_name == "master" ) {
              APP_LATEST="${IMAGE_REGISTRY}/${env_image_namespace}/${APP_NAME}:latest"
            } else {
              APP_LATEST="${IMAGE_REGISTRY}/${env_image_namespace}/${APP_NAME}:${env_git_branch_name}_latest"
            }
            echo "APP_IMAGE: ${APP_IMAGE}"

            withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'jenkins-ecr', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {

            sh """
				      aws ecr get-login-password --region us-west-2 | buildah login --authfile ./auth.json -u AWS --password-stdin 136299550619.dkr.ecr.us-west-2.amazonaws.com
			        cat ./auth.json

				      # Changed Cammis
              sed -i "s/{CLUSTER_SUBDOMAIN}/${env_cluster_subdomain}/" devops/docker/Dockerfile
              echo "Building image"
              buildah --storage-driver vfs bud --tls-verify="false" --authfile ./auth.json --format=docker -f devops/docker/Dockerfile -t ${APP_LATEST} -t ${APP_IMAGE} .
				      buildah --storage-driver vfs images -a

			    	  echo "Show images"
			    	  buildah --storage-driver vfs images --digests
			    	  #buildah --storage-driver vfs images --format {{.ID}} ${IMAGE_REGISTRY}/${env_image_namespace}/${APP_NAME}
		    	  """
				    // Added Cammis - Outside of shell
				    echo "Building def"
			      //def Imageid = sh returnStdout: true, script: "buildah --storage-driver vfs images --format {{.ID}} ${IMAGE_REGISTRY}/${env_image_namespace}/${APP_NAME} | tr -d '\n' "

			      sh """
			  	    echo Buildah push
			  	    echo "IMAGE_REGISTRY: ${IMAGE_REGISTRY}"
              buildah --storage-driver vfs push --tls-verify="false" --authfile ./auth.json "${APP_IMAGE}"
              buildah --storage-driver vfs push --tls-verify="false" --authfile ./auth.json "${APP_LATEST}"
              aws ecr list-images --repository-name ${env_image_namespace}/${APP_NAME}

              sleep 15
            """
            }
          }
        }
        container(name:"aws-cli") {
          script {
            env_step_name = "pull vulnerability report"
            env_image_fullspec="${env_image_namespace}/${APP_NAME}"
            echo "env_image_fullspec = ${env_image_fullspec}"
            getVulnerabilityInfo(env_image_fullspec,env_git_branch_name,env_current_git_commit)
          }
        }
      }
    }

    //  deploy image to sandbox env using ArgoCD
    stage("sandbox deploy/tests") {
      when {
        expression {
          env_target_env_type == SANDBOX
        }
      }
      steps {
        script {
          env_stage_name = "sandbox deploy/tests"
          env_step_name = "deploy"
          milestone(SANDBOX_MILESTONE)
          // two level lock: type level and then instance level
          // scenarios: 1. builds involving single sandboxes
          // scenarios: 2. builds inovling multiple sandboxes
          // scenarios: 3. builds involving single sandbox vs builds involving multiple sandboxes
          // l_env_overall_lock_name = g_namespaces.join("-")+"-"+env_target_env_type+"-"+APP_NAME
          l_env_overall_lock_name = LOCK_DEPLOYMENTS_REPO
          lock(resource: l_env_overall_lock_name,inversePrecedence: false ) {
              g_namespaces.each { ns ->
                  env_target_namespace = ns
                  lock(resource: env_target_namespace+"-"+APP_NAME,inversePrecedence: LOCK_SKIPPING_OLD_BUILDS ) {
                        echo "Deploying to ${env_target_env_type}:${env_target_namespace}...."
                        container("aws-cli") {
                          env_image_tag="${env_git_branch_name}_${BUILD_NUMBER}_${env_current_git_commit}"
                          updateHelmTemplates(env_image_tag)
                        }
                        //Update deployment artifacts in GitHub
                        container("jnlp") {
                            env_image_id="${IMAGE_REGISTRY}/${env_image_namespace}/${APP_NAME}:${env_git_branch_name}_${env_current_git_commit}"
                            env_deployment_yaml_path="${GIT_DEPLOYMENT_REPO_NAME}/${APP_TYPE}/${env_target_env_type}/${env_target_namespace}/${APP_NAME}"
                            updateDeployment(env_deployment_yaml_path,env_image_namespace,env_current_git_commit,env_kube_config_creds_id)
                        }
                        container("node") {
                            env_step_name = "tag"
                            slackNotification("pipeline","${APP_NAME}-${env_git_branch_name}: <${BUILD_URL}console|build #${BUILD_NUMBER}> deployed to ${env_target_env_type}:${env_target_namespace} .","#31C624","false")
                            tag(SANDBOX_PASSED)
                        }
                   }
              }
              setupForNextStage(g_stage_index++,env_git_branch_type)
          }
        }
      }
    }

    // deploy image to dev
    stage("dev deploy/tests") {
      when {
        expression {
          env_target_env_type == DEV
        }
      }
      steps {
        script {
          env_stage_name = "dev deploy/tests"
          env_step_name = "deploy"
          milestone(DEV_MILESTONE)
          // two level lock: type level and then instance level
          // scenarios: 1. builds involving single sandboxes
          // scenarios: 2. builds inovling multiple sandboxes
          // scenarios: 3. builds involving single sandbox vs builds involving multiple sandboxes
          // l_env_overall_lock_name = g_namespaces.join("-")+"-"+env_target_env_type+"-"+APP_NAME
          l_env_overall_lock_name = LOCK_DEPLOYMENTS_REPO
          lock(resource: l_env_overall_lock_name,inversePrecedence: false ) {
            g_namespaces.each { ns ->
              env_target_namespace = ns

              lock(resource: env_target_namespace+"-"+APP_NAME,inversePrecedence: LOCK_SKIPPING_OLD_BUILDS ) {
                echo "Deploying to ${env_target_env_type}:${env_target_namespace}...."
                //Update deployment artifacts in GitHub
                container("aws-cli") {
                    env_image_tag="${env_git_branch_name}_${BUILD_NUMBER}_${env_current_git_commit}"
                    updateHelmTemplates(env_image_tag)
                }
                container("jnlp") {
                    env_image_id="${IMAGE_REGISTRY}/${env_image_namespace}/${APP_NAME}:${env_git_branch_name}_${env_current_git_commit}"
                    env_deployment_yaml_path="${GIT_DEPLOYMENT_REPO_NAME}/${APP_TYPE}/${env_target_env_type}/${APP_NAME}"
                    updateDeployment(env_deployment_yaml_path,env_image_namespace,env_current_git_commit,env_kube_config_creds_id)
                }
                container("node") {
                    env_step_name = "tag"
                    tag("${DEV_PASSED}_${env_target_namespace}_from_${env_git_branch_name}")
                    slackNotification("pipeline","${APP_NAME}-${env_git_branch_name}: <${BUILD_URL}console|build #${BUILD_NUMBER}> deployed to ${env_target_env_type}:${env_target_namespace} .","#31C624","false")
                }
              }
            }
            setupForNextStage(g_stage_index++,env_git_branch_type)
          } //end lock
        } // end script
      } //end step
    } //end stage

    //deploy image to qa
    stage("qa deploy/tests/po acceptance") {
      when {
        expression {
          env_target_env_type == QA
        }
      }
      steps {
        script {
          env_stage_name = "qa deploy/tests/po acceptance"
          env_step_name = "get approval"
          milestone(QA_MILESTONE)
          // two level lock: type level and then instance level
          // scenarios: 1. builds involving single sandboxes
          // scenarios: 2. builds inovling multiple sandboxes
          // scenarios: 3. builds involving single sandbox vs builds involving multiple sandboxes
          env_step_name = "deploy"
          l_env_overall_lock_name = g_namespaces.join("-")+"-"+env_target_env_type+"-"+APP_NAME
          lock(resource: l_env_overall_lock_name,inversePrecedence: LOCK_SKIPPING_OLD_BUILDS ) {
              g_namespaces.each { ns ->
                  env_target_namespace = ns
                  lock(resource: env_target_namespace+"-"+APP_NAME,inversePrecedence: LOCK_SKIPPING_OLD_BUILDS) {
                        echo "Deploying to ${env_target_env_type}:${env_target_namespace}...."
                        container("aws-cli") {
                        }
                        container("node") {
                          env_step_name = "smoke tests"
                          echo "Executing smoke tests...."

                        }

                        env_step_name = "get product owner approval"

                        def ackTimeoutInSeconds = KUBE_ENVS[QA].ack_timeout as Integer
                        //need attention from PO

                        //PO start manual acceptance tests
                        echo "PO perform manual tests..."

                        //PO accepts/rejects build
                        def approvalTimeoutInSeconds = KUBE_ENVS[QA].approval_timeout as Integer

                        env_step_name = "tag"
                        container("aws-cli") {
                          tag("${QA_PASSED}_${env_target_namespace}_from_${env_git_branch_name}")
                          slackNotification("pipeline","${APP_NAME}-${env_git_branch_name}: <${BUILD_URL}console|build #${BUILD_NUMBER}> deployed to ${env_target_env_type}:${env_target_namespace} .","#31C624","false")
                        }

                        //only require PO to be involved for the primary env if there are multiple namespaces for qa
                  }
              }
              setupForNextStage(g_stage_index++,env_git_branch_type)
          }
        }
      }
    }

    //deploy image to prod
    stage("prod deploy/tests") {
      when {
        expression {
          env_target_env_type == PRD
        }
      }

      steps {
        script {
          milestone(PROD_MILESTONE)
          // two level lock: type level and then instance level
          // scenarios: 1. builds involving single sandboxes
          // scenarios: 2. builds inovling multiple sandboxes
          // scenarios: 3. builds involving single sandbox vs builds involving multiple sandboxes
          l_env_overall_lock_name = g_namespaces.join("-")+"-"+env_target_env_type+"-"+APP_NAME
          lock(resource: l_env_overall_lock_name,inversePrecedence: LOCK_SKIPPING_OLD_BUILDS ) {

           }
        }
      }
    }
  }

  //pipeline post actions
  post {
    always {
        echo "Build Process complete."
        script {
            try{
              echo "skipping archival of regression test artifacts until implemented..."
              if ( env_archive_artifacts == "true" ) {
                archiveArtifacts artifacts: "${env_com_automation}/Regression/test-reports/**/*.html", fingerprint: true
              }
            } catch (Exception e){
              echo "Error arching artifacts for ${JOB_NAME} : " + e.toString()
            }
        }
    } // always

    success {
        echo "Build Process was success. Site is available at ${env.SITE_URL}"
        slackNotification("pipeline", "${JOB_NAME}: <${BUILD_URL}|build #${BUILD_NUMBER}> was successful :woohoo: after ${currentBuild.durationString}.\n`${SONAR_SLACK_MSG}`", "#215ACC","false")
    } //success

    unstable {
        echo "Build is unstable."
        slackNotification("pipeline","${JOB_NAME}: <${BUILD_URL}|build #${BUILD_NUMBER}> was unstable :shrug: after ${currentBuild.durationString}. Check `SonarQube Quality Gate` status.", "#F6F60F","true")
    } // unstable

    aborted {
        echo "Pipeline aborted."
        slackNotification("pipeline", "${JOB_NAME}: <${BUILD_URL}|build #${BUILD_NUMBER}> aborted :bkpabort: after ${currentBuild.durationString} in stage: `${env_stage_name}` step: `${env_step_name}`.", "#EA6E06","false")
    } // aborted

    failure {
        echo "Build encountered failures ."
        slackNotification("pipeline","${JOB_NAME}: <${BUILD_URL}|build #${BUILD_NUMBER}> failed :boom: after ${currentBuild.durationString} in stage: `${env_stage_name}` step: `${env_step_name}`. @here", "#EA0652","true")
        emailNotification("failed")
        container("aws-cli") {
          rollback()
        }
    } // failure

    changed {
        echo "Build content was changed."
    } // changed

  } // post
}

// function to deploy docker image in kubernetes namespace
//   target_env_type - type of namespace ("sandbox"/"develop"/"release"/"master")
//   target_namespace - the actual kubernetes namespace
//   image_namespace - the namespace(account) used in the image registry for the docker image
//   kube_config_creds_id - jenkinds creds id for deploying to kube namespace
//

//function to run postman tests assuming postman tests to be in src/test/postman
//   target_env_type - type of namespace ("sandbox"/"develop"/"release"/"master")
//   target_namespace - the actual kubernetes namespace
//   kube_config_creds_id - jenkinds creds id for deploying to kube namespace
//

//function to get relevant people to ack event
//   manual - "yes" or "no", "no" to skip the manual step
//   timeoutInSeconds - wait will time out if unanswered
//   message - message displayed in prompt
//   submitters - gatekeepers_jenkins
//

//function to allow simple approval to move forward in pipeline
//   manual - "yes" or "no", "no" to skip the manual step
//   timeoutInSeconds - wait will time out if unanswered
//   message - message displayed in prompt
//   submitters - gatekeepers_jenkins
//

//function to wait for approver to provide creds id for promotion into a kube namespace
//   timeoutInSeconds - wait will time out if unanswered
//   message - message displayed in prompt
//   submitters - gatekeepers_jenkins
//   default_kube_creds_id - default value displayed in prompt
//return:
//   kube_config_creds_id has the creds id for deployment into kube namespace
//

//function to wait for approval and info for deployment into env such as production
//  timeoutInSeconds - wait will time out if nobody clicks the button
//  message - message displayed in prompt
//  submitters - users to accept or abort
//return:
//  PROD_REPO, PROD_REPO_USERID and PROD_REPO_PASSWORD are populated as environment variables
//
def getGitRepoInfoForDeployment(timeoutInSeconds, message, submitters) {
    timeout(time: timeoutInSeconds, unit: 'SECONDS') {
        def INPUT  = input message: message, ok: 'Yes',submitter:submitters,
                     parameters: [
                       string(defaultValue: '', description: 'production repo url', name: 'repo'),
                       string(defaultValue: '', description: 'repo user id', name: 'userid'),
                       password(defaultValue: '', description: 'repo password', name: 'password')
                     ]

        env.PROD_REPO = INPUT.repo
        env.PROD_REPO_USERID = INPUT.userid
        env.PROD_REPO_PASSWORD=INPUT.password
    }
}

//function to send email notification
//  status_message - message included in the email body
//
def emailNotification(status_message) {
          echo "skipping email notification"
          return
          emailext subject: "${APP_NAME}-${env_git_branch_name} build $status_message",
                   body: "${APP_NAME}-${env_git_branch_name}:${BUILD_NUMBER} $status_message.  Please check log:${BUILD_URL}",
                   recipientProviders: [
                      [$class: 'CulpritsRecipientProvider'],
                      [$class: 'DevelopersRecipientProvider'],
                      [$class: 'RequesterRecipientProvider']
                   ],
                   to: 'wmschwar@us.ibm.com'
}

// fucntion to set up values for intial deployment environment based on the stage definition of a branch
//   stage_index - the index number of the next stage for given branch
def setupForNextStage(stage_index,git_branch_type) {
  if (BRANCHES["${git_branch_type}"].stages[stage_index]) {
    env_target_env_type=BRANCHES["${git_branch_type}"].stages[stage_index]
    g_namespaces=KUBE_ENVS["${env_target_env_type}"].namespaces
    env_kube_config_creds_id=KUBE_ENVS["${env_target_env_type}"].kube_config_creds_id
    env_startup_args_wget=KUBE_ENVS["${env_target_env_type}"].startup_args_wget
    env_cluster_env=KUBE_ENVS["${env_target_env_type}"].cluster_env
    env_region_sn=REGIONS["${PRIMARY_REGION}"].shortname
    env_mcweb_env=KUBE_ENVS["${env_target_env_type}"].mcweb_env
  }
}

//function to delete docker image from the local jenkins node

//function to tag docker image and git commit when certian milestone is achieved.
//needs more work.
def tag(progress_status,release_note="false") {
  script {
    echo "tagging current git commit as ${progress_status}"
    def image_build_number="${BUILD_NUMBER}"
    if ( env_skip_build == "true" ) {
      image_build_number=getImageBuildNumber("${WORKSPACE}/argocddeploy/${GIT_DEPLOYMENT_REPO_NAME}/${env_target_namespace}/${APP_NAME}/release/version.yaml")
    }

    withCredentials([usernamePassword(credentialsId: "${SSH_AGENT_GIT_ID}", usernameVariable: 'NUSER', passwordVariable: 'NPASS')]) {
      withEnv(["image_build_number=${image_build_number}"]) {
        sh """
            #tag every every passed
            #git tag -a ${progress_status}-\$(date +'%Y-%m-%d_%H-%M-%S') -m "image=${env_image_namespace}/${APP_NAME}:${env_git_branch_name}_${env_current_git_commit}"
            git config --global --add safe.directory '*'
            #get the current git commit id. it could be old image using latest kube config
            current_git_id=\$(git log --pretty=format:'%h' -n 1)
            annotation="version: ${VERSION}\nimage: ${env_image_namespace}/${APP_NAME}:${env_git_branch_name}_${image_build_number}_${env_current_git_commit}\nstatus: ${progress_status}\ngit-info: \${current_git_id}"

            #if release notes needs to be generated
            if [ ${release_note} = "true" ]
            then
              set +e
              annotation=\$(echo -e "\$annotation \n++++Release Notes++++\n")
              #check if tag PREVIOUS_PRODUCTION exists
              previous=\$(git rev-list -n 1 $PREVIOUS_PRODUCTION)
              if [ \$? -eq 0 ]
              then
                  changes=\$(git log $PREVIOUS_PRODUCTION..${env_current_git_commit} --pretty=format:' * %s' | grep -v Merge)
              else
                  changes="tag $PREVIOUS_PRODUCTION doesn't exist."
              fi
              annotation=\$(echo -e "\${annotation}\n\$changes")
            fi

            git config  --global user.email "jenkins@cammis.com"
            git config  --global user.name "jenkins"

            echo "progress_status :  ${progress_status}"
            echo "env_current_git_commit :  ${env_current_git_commit}"
            tagCommit="${env_git_branch_name}_${image_build_number}_${env_current_git_commit}"

            git tag -f -a "\$tagCommit" -m "\$annotation" ${env_current_git_commit}
            git push -f https://${NUSER}:${NPASS}@${GIT_HOST}/${GIT_GROUP}/${GIT_REPO_NAME}.git \$tagCommit
        """
      }
    }
  }
}

// point tag1 to tag2 for git
// the jenkins job needs to be configured to fetch tags
//  e.g.
//  tag1 = previous
//  tag2 = current
def tagReassign(tag1, tag2) {
    echo "Point ${tag1} to ${tag2}...."
    //withCredentials([usernamePassword(credentialsId: "${SSH_AGENT_GIT_ID}", passwordVariable: 'SSH_KEY', usernameVariable: 'SSH_USER')]) {
      // withEnv(["GIT_SSH_COMMAND=ssh -o StrictHostKeyChecking=no -o User=${SSH_USER} -i ${SSH_KEY}"]) {
        withCredentials([usernamePassword(credentialsId: "${SSH_AGENT_GIT_ID}", usernameVariable: 'NUSER', passwordVariable: 'NPASS')]) {
          sh """
              set +e
              current_prod_commit=\$(git rev-list -n 1 $tag2)
              if [ \$? -eq 0 ]
              then
                  echo "commit id for ${tag2} is \${current_prod_commit}"
                  #get annotation of current_product tag
                  annotation=\$(git tag -n9 ${tag2} | awk '{print \$2}')
                  git tag -f -a ${tag1} -m \${annotation}  \${current_prod_commit}

                  git push -f https://${NUSER}:${NPASS}@${GIT_HOST}/${GIT_GROUP}/${GIT_REPO_NAME}.git ${tag1}
                  #git push -f https://${SSH_USER}:${SSH_KEY}@${GIT_HOST}/${GIT_GROUP}/${GIT_REPO_NAME}.git ${tag1}
              fi
          """
      // }
    }
}

//function to back up current resources before deployment
//need more work and test
def createDeploymentBackup(app_name,target_namespace) {
  sh """
     set +e
     rm -rf rollback
     mkdir rollback
     kubectl get deployment ${app_name} -n ${target_namespace} -o yaml > rollback/deployment.yaml
     if [ \$? -eq 1 ]
     then
         rm -rf rollback/deployment.yaml
     fi
     kubectl get svc ${app_name} -n ${target_namespace} -o yaml > rollback/service.yaml
     if [ \$? -eq 1 ]
     then
         rm -rf rollback/service.yaml
     fi
     kubectl get configmap ${app_name}-config -n ${target_namespace} -o yaml > rollback/config.yaml
     if [ \$? -eq 1 ]
     then
         rm -rf rollback/config.yaml
     fi
     kubectl get secret ${app_name}-secret -n ${target_namespace} -o yaml > rollback/secret.yaml 2>/dev/null
     if [ \$? -eq 1 ]
     then
         rm -rf rollback/secret.yaml
     fi
  """
}

//function to rollback deployment along with resources on failure
//need more work and test
def rollback() {
  if (ROLLBACK_ENVS.contains(env_target_env_type)) {
    echo "Rolling back ${env_target_env_type}:${env_target_namespace}"
      withCredentials([
      file(credentialsId: "${env_kube_config_creds_id}",variable: 'KUBECONFIG'),
      usernamePassword(credentialsId: "${IMAGE_REGISTRY_CREDS_ID}",
                       passwordVariable: 'DOCKER_PASSWORD',
                       usernameVariable: 'DOCKER_USERNAME')]) {
                         sh """
                            #kubectl --kubeconfig=${env.KUBECONFIG} apply -f rollback -n ${env_target_namespace}
                            kubectl rollout undo deployment/${APP_NAME}

                            # check deployment status
                            sleep 1
                            continue=true
                            while [ \$continue == true ]
                            do
                                  kubectl rollout status deployment.v1.apps/${APP_NAME} -n ${env_target_namespace} | grep "successfully rolled out"
                                  if [ \$? -eq 0 ]
                                  then
                                      continue=false
                                  fi
                            done
                         """
                       }

  }
}
/*
    slack notification
    channel - "pipeline", "po" or "gate_keeper"
    msg - string
    color - "good", "danger" , may need more work
*/
def slackNotification(channel,msg,color,nc) {
    def lt,lc

    lt=SLACK_CHANNELS[channel].token
    lc=SLACK_CHANNELS[channel].channel


    slackSend color: color, channel: lc, message: msg, baseUrl: SLACK_URL, token: lt, notifyCommitters: nc
}

//set slack channels and tokens
def initSlackChannels() {
  SLACK_CHANNELS.each { key, value ->
      withCredentials([usernamePassword(credentialsId: value.channel,
                   passwordVariable: 'channel_token',
                   usernameVariable: 'channel_name')]) {
                     value.channel="#$channel_name"
                     value.token="$channel_token"
					           echo "channel_token is '${channel_token}'"
		                 echo "channel_name is '${channel_name}'"
                   }
  }
}

//get vulnerability assessment information from cloud registry scan
def getVulnerabilityInfo(fullImageSpec,branchName, gitCommit) {
  withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'jenkins-ecr', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {

      echo "Pulling vulnerability assessment information from AWS ECR Cloud Registry..."
      def imageTag="${branchName}_${BUILD_NUMBER}_${gitCommit}"

      try {
        sh 'aws ecr get-login-password --region us-west-2'

  	  	// wait for scan every 5 seconds 60 times.   Returns 255 on failure
  	  	def COUNT = sh returnStdout: true, script: "aws ecr wait image-scan-complete --repository-name ${env_image_fullspec} --image-id imageTag=${imageTag} --region us-west-2 | tr -d '\n'"
  	  	echo "COUNT : ${COUNT}"

  	    // 255 means the scan did not complete in 5 minutes
  	  	if ((COUNT != "255")) {
    			echo 'Found report'
  	  		sh "aws ecr describe-image-scan-findings --repository-name ${env_image_fullspec} --image-id imageTag=${imageTag} --region us-west-2  --output text | tee devops/ecr_report.txt"
  	  	} else {
	    		echo "Vulnerability scan has teken more then 5 minutes" > devops/ecr_report.txt
  	  	} // end if-else

        publishHTML (target: [
            allowMissing: true,
            alwaysLinkToLastBuild: false,
            keepAll: false,
            reportDir: 'devops',
            //reportFiles: 'vaReport.txt,npm_audit.html',
            reportFiles: 'ecr_report.txt',
            reportName: "Vulnerability Assessment Report"
          ])
      }

      catch(Exception e) {
        echo "Scan failed to complete. Please try again later."
        echo e.toString()
      }
  }
}

def dodeployment(image_namespace,git_commit) {
  script {
    echo "doing dodeployment"

	withCredentials([usernamePassword(credentialsId: "${SSH_AGENT_GIT_ID}", usernameVariable: 'NUSER', passwordVariable: 'NPASS')]) {

	    git(url: "https://${GIT_HOST}/${GIT_GROUP}/${GIT_REPO_NAME}.git",credentialsId: "${SSH_AGENT_GIT_ID}",branch: "master")

		// Set helm update.
		def tagVersion = '!' + "${env_git_branch_name}" + '_' + "${git_commit}" + '!'
		def tagVersionnoquote = "${env_git_branch_name}" + '_' + "${git_commit}"
        echo tagVersion

		// Update provider helm cart yaml file
		sh """
			sed -i "s/tag:.*/tag: ${tagVersion}/" devops/kubernetes/kubernetesArgoCD/provider/charts/starter/values.yaml
			tr '!' '"' < devops/kubernetes/kubernetesArgoCD/provider/charts/starter/values.yaml > new_values.yaml
			mv new_values.yaml devops/kubernetes/kubernetesArgoCD/provider/charts/starter/values.yaml

		"""

		sh """
	    	git status
			pwd
        	ls -l
        	dir="devops/kubernetes"
        	if [ -d \$dir -a ! -z "\$(ls \$dir/*.yaml | grep yaml)" ]
           	   then
            	sed -i "s/{NAME_SPACE}/${image_namespace}/" \$dir/*.yaml
            	sed -i "s/{APP_NAME}/${APP_NAME}/" \$dir/*.yaml
            	sed -i "s/{BRANCH_NAME}/${env_git_branch_name}/" \$dir/*.yaml
            	sed -i "s/{BUILD_NUM}/${git_commit}/" \$dir/*.yaml
              sed -i "s/{ENVIRONMENT}/${env_target_namespace}/" \$dir/*.yaml
              sed -i "s/{CLUSTER_SUBDOMAIN}/${env_cluster_subdomain}/" \$dir/*.yaml
            	# cp \$dir/*.yaml .

				# add to test argocd deployment
				cp devops/kubernetes/config.yaml devops/kubernetes/kubernetesArgoCD/config.yaml
				cp devops/kubernetes/deployment.yaml devops/kubernetes/kubernetesArgoCD/deployment.yaml
            	cp devops/kubernetes/service.yaml devops/kubernetes/kubernetesArgoCD/service.yaml

		 		git status

         		#cp devops/kubernetes/*.yaml devops/kubernetes/kubernetesArgoCD/
         		git config  --global user.email "jenkins@cammis.com"
         		git config  --global user.name "jenkins"
         		git add devops/kubernetes/kubernetesArgoCD/*.yaml
				git add devops/kubernetes/kubernetesArgoCD/provider/charts/starter/values.yaml

		 		#cat devops/kubernetes/kubernetesArgoCD/deployment.yaml
         		git commit -m "Updated yamls in kubernetesArgoCD"
		 		git status

         		#git push https://${GIT_HOST}/${GIT_GROUP}/${GIT_REPO_NAME}.git
		 		git push -f https://${NUSER}:${NPASS}@${GIT_HOST}/${GIT_GROUP}/${GIT_REPO_NAME}.git

         	else
             	echo "Oops... looks like no artifacts present for deployment"
         	fi

        """
	}
  }
}  // end dodeployment

// Added CAMMIS
// this whole function is currently hardcoded.  Fix it later if we take this approach
// Talk with us about waht going on here.
//
def deployParent(env_image_namespace,env_current_git_commit) {
  script {
    echo "doing deployParent"

	withCredentials([usernamePassword(credentialsId: "${SSH_AGENT_GIT_ID}", usernameVariable: 'NUSER', passwordVariable: 'NPASS')]) {
		dir('parent') {
	    	git(url: "https://github.com/ca-mmis/ca-mmis-aws-provider-portal-parent.git",credentialsId: "${SSH_AGENT_GIT_ID}",branch: "main")

		// set up git tag and ECR tags
		pwd
		def tagId = sh returnStdout: true, script: "git rev-list --tags --max-count=1"
		def tagValue = sh returnStdout: true, script: "git describe --tags ${tagId}"
		echo  "After tokenize patch : ${tagValue}"
		def (major, minor, patch) = tagValue.tokenize('.')
		echo  "After tokenize patch : ${patch}"
		def intTagValue = patch.toInteger()
		def tagpatch = intTagValue + 1
		def tagVersion = major + '.' + minor + '.' + tagpatch
		echo  "tagversion : ${tagVersion}"

		// Set helm update.
		def ecrTag = '!' + "${env_git_branch_name}" + '_' + "${env_current_git_commit}" + '!'
		echo "ecrTag : ${ecrTag}"
		def gitCommitTag = "${env_git_branch_name}" + '_' + "${env_current_git_commit}"

		// Update parent provider helm cart yaml file
		sh """

			sed -i "s/tag:.*/tag: ${ecrTag}/" provider/dev/charts/starter/values.yaml
			tr '!' '"' < provider/dev/charts/starter/values.yaml > new_values.yaml
			mv new_values.yaml provider/dev/charts/starter/values.yaml

			git status
			git add provider/dev/charts/starter/values.yaml
			git status

         	git config  --global user.email "jenkins@cammis.com"
         	git config  --global user.name "jenkins"

		 	#cat devops/kubernetes/kubernetesArgoCD/deployment.yaml
         	git commit -m "Updated ${APP_NAME} with Git Commit=${gitCommitTag}"

			#git tag -f -a "${tagVersion}" -m "Update parent version"

			git push -f https://${NUSER}:${NPASS}@github.com/ca-mmis/ca-mmis-aws-provider-portal-parent.git main

			git tag -f -a "${tagVersion}" -m "Updated ${APP_NAME} with Git Commit = ${gitCommitTag}"
		 	git push -f https://${NUSER}:${NPASS}@github.com/ca-mmis/ca-mmis-aws-provider-portal-parent.git ${tagVersion}
		"""

       }  // end dir
	}
  }
}  // end deployParent


// function argoCDManualSync triggers argocd sync process
// argocd_cred_id is namespace specific credential id -- in the default NS
def argoCDManualSync(argocd_cred_id) {
    withCredentials([string(credentialsId: "${argocd_cred_id}", variable: 'ARGOCD_AUTH_TOKEN')]) {
        withEnv(["ARGOCD_SERVER=${ARGOCD_SERVER}"]) {
          timeout(time: DEPLOYMENT_TIMEOUT_IN_SECONDS, unit: 'SECONDS') {
            sh """
				export ARGOCD_AUTH_TOKEN
				argocd account can-i sync applications default/starter --auth-token $ARGOCD_AUTH_TOKEN --insecure
				argocd app sync starter --dry-run  --insecure
            """

			//argocd --grpc-web app sync "${env_target_namespace}-${APP_NAME}" --insecure --dryrun
            //Below code can be put at the end of the sh block if timeout doesn't work
            //argocd --grpc-web app wait "${env_target_namespace}-${APP_NAME}" --timeout ${DEPLOYMENT_TIMEOUT_IN_SECONDS}
		  }
        }
	}
}  // End argoCDManualSync

//def updateHelmTemplates(env_target_env_type,image_namespace){
def updateHelmTemplates(image_tag){
  echo "image tag ${image_tag}"
  if(env_target_env_type == "sandbox"){
    dir("${WORKSPACE}/devops/kubernetes/overlays/${env_target_env_type}/${env_target_namespace}"){
      sh """
       sed -i "s/{IMAGE_TAG}/${image_tag}/" ${WORKSPACE}/devops/kubernetes/overlays/${env_target_env_type}/${env_target_namespace}/values.yaml
       sed -i "s/{VERSION}/${VERSION}/" ${WORKSPACE}/devops/kubernetes/overlays/${env_target_env_type}/${env_target_namespace}/values.yaml
       echo ${image_tag}
       kubectl kustomize --enable-helm >all.yaml
       ls -al
       """
    }
  }
  else{
     dir("${WORKSPACE}/devops/kubernetes/overlays/${env_target_namespace}"){
      sh """
      sed -i "s/{IMAGE_TAG}/${image_tag}/" ${WORKSPACE}/devops/kubernetes/overlays/${env_target_namespace}/values.yaml
      sed -i "s/{VERSION}/${VERSION}/" ${WORKSPACE}/devops/kubernetes/overlays/${env_target_namespace}/values.yaml
      kubectl kustomize --enable-helm >all.yaml
      """
     }
  }
}

// Update artifact in deployment repository
// the jenkins job needs to be configured to update deployment yaml in github
//
//  artifactPath is the path to artifact
//  imageID imageid to be updated in the yaml file
def updateDeployment(artifactPath,image_namespace,git_commit,kube_config_creds_id) {
    echo "Update image ID in deployment.yaml"
    def image_build_number="${BUILD_NUMBER}"
      withCredentials([usernamePassword(credentialsId: "${SSH_AGENT_GIT_ID}", usernameVariable: 'NUSER', passwordVariable: 'NPASS')]) {
        withEnv(["GIT_SSH_COMMAND=ssh -o StrictHostKeyChecking=no -o User=${NUSER} -i ${NPASS}","image_build_number=${image_build_number}"]) {
          if ( env_skip_build == "true" ) {
            image_build_number=getImageBuildNumber("${WORKSPACE}/argocddeploy/${artifactPath}/release/version.yaml")
          }

          dir("${WORKSPACE}/argocddeploy"){

            try{
              sh """
                  pwd
                  git clone https://${NUSER}:${NPASS}@${GIT_HOST}/${GIT_GROUP}/${GIT_DEPLOYMENT_REPO_NAME}.git --depth=1
                  git config  --global user.email "jenkins@cammis.com"
                  git config  --global user.name "jenkins"
                  ls -l
                  cd ${GIT_DEPLOYMENT_REPO_NAME}
                  git checkout master
                  if [ "\$(ls -al ${WORKSPACE}/argocddeploy/${artifactPath}/*.yaml | grep yaml | wc -l)" -gt "0" ]
                    then
                      echo "inside if loop file exists"
                      rm -v ${WORKSPACE}/argocddeploy/${artifactPath}/*.yaml
                  elif [ ! -d "${WORKSPACE}/argocddeploy/${artifactPath}" ]
                    then
                      echo "inside elif directory doesn't exists"
                      mkdir -p "${WORKSPACE}/argocddeploy/${artifactPath}"
                  fi

                  if [ "${env_target_env_type}" = "sandbox" ]
                    then
                    echo "sandbox ${env_target_namespace}"
                    cp ${WORKSPACE}/devops/kubernetes/overlays/${env_target_env_type}/"${env_target_namespace}"/all.yaml "${WORKSPACE}/argocddeploy/${artifactPath}"
                   else
                     echo "inside else ${env_target_env_type}"
                     cp ${WORKSPACE}/devops/kubernetes/overlays/${env_target_namespace}/all.yaml "${WORKSPACE}/argocddeploy/${artifactPath}"
                  fi

                  # Update version information
                  if [ ! -d "${WORKSPACE}/argocddeploy/${artifactPath}/release" ]
                    then
                      mkdir "${WORKSPACE}/argocddeploy/${artifactPath}/release"
                  fi
                  if [ ! -f "${WORKSPACE}/argocddeploy/${artifactPath}/release/version.yaml" ]
                    then
                      cp ${WORKSPACE}/devops/release/version.yaml "${WORKSPACE}/argocddeploy/${artifactPath}/release/"
                  fi
              """

              switch(env_target_namespace) {
                  case "dev":
                      incrementVersion("${WORKSPACE}/argocddeploy/${artifactPath}/release/version.yaml",git_commit,image_build_number,env_release_type)
                      break
                  case "sandbox00":
                      incrementVersion("${WORKSPACE}/argocddeploy/${artifactPath}/release/version.yaml",git_commit,image_build_number,env_release_type)
                      break
                  default:
                      def getDevVersion="${WORKSPACE}/argocddeploy/${GIT_DEPLOYMENT_REPO_NAME}/dev/${APP_NAME}/release/version.yaml"
                      incrementSandboxVersion("${WORKSPACE}/argocddeploy/${artifactPath}/release/version.yaml",getDevVersion,git_commit,image_build_number)
                      break
              }

              sh """
                  cd ${GIT_DEPLOYMENT_REPO_NAME}
                  git add -Av
                  git commit -m "Updated yamls in ${artifactPath} for build commit id ${git_commit}"
                  git push -f https://${NUSER}:${NPASS}@${GIT_HOST}/${GIT_GROUP}/${GIT_DEPLOYMENT_REPO_NAME}.git
                  cd ..
              """
            }
            catch(Exception e)
            {
              echo "Ignoring git check in case of a rerun of the build. " + e.toString()
            }
          }
        }
     }
}

// function getImageBuildNumber will pull in the last successful build number
def getImageBuildNumber(versionYaml) {
  def versionInfo = readYaml file: "${versionYaml}"
  def imageBuildNumber=versionInfo.service.build.number

  return(imageBuildNumber)
}

// function incrementVersion will increment the patch,minor and major version by one on a master branch build
def incrementVersion(versionYaml,gitCommit,imageBuildNumber,env_release_type) {
  def versionInfo = readYaml file: "${versionYaml}"
  def Integer newMinor = versionInfo.service.version.minor
  def Integer newMajor = versionInfo.service.version.major
  def Integer newPatch = versionInfo.service.version.patch

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
  updatedVersionInfo.service.version.patch=newPatch
  updatedVersionInfo.service.version.minor=newMinor
  updatedVersionInfo.service.version.major=newMajor
  updatedVersionInfo.service.version.full=updatedVersionInfo.service.version.major+"."+updatedVersionInfo.service.version.minor+"."+updatedVersionInfo.service.version.patch

  if ( env_skip_build == "false" ) {
    updatedVersionInfo.service.build.date=buildDate.format("yyyy-MM-dd_HH:mm")
  }
  updatedVersionInfo.service.build.number="${imageBuildNumber}"
  updatedVersionInfo.service.build.image="${IMAGE_REGISTRY}/${env_image_namespace}/${APP_NAME}:${BRANCH_NAME}_${imageBuildNumber}_${gitCommit}"
  updatedVersionInfo.service.build.commit="${gitCommit}"
  println "Saving version.yaml file...\n${updatedVersionInfo}"
  writeYaml file: "${versionYaml}", data: updatedVersionInfo, overwrite: true
}

// function incrementVersion will increment the patch version by one on a master branch build
def incrementSandboxVersion(versionYaml,devYaml,gitCommit,imageBuildNumber) {
  def versionInfo = readYaml file: "${versionYaml}"
  def updatedVersionInfo = versionInfo
  if ( fileExists("${devYaml}") ) {
    def devInfo = readYaml file: "${devYaml}"
    def newMajor = devInfo.service.version.major
    def newMinor = devInfo.service.version.minor
    def newPatch = devInfo.service.version.patch
    def buildDate = new Date()
    updatedVersionInfo.service.version.major=newMajor
    updatedVersionInfo.service.version.minor=newMinor
    updatedVersionInfo.service.version.patch=newPatch
    updatedVersionInfo.service.version.full=newMajor+"."+newMinor+"."+newPatch
    updatedVersionInfo.service.build.date=buildDate.format("yyyy-MM-dd_HH:mm")
    updatedVersionInfo.service.build.number="${imageBuildNumber}"
    updatedVersionInfo.service.build.image="${IMAGE_REGISTRY}/${env_image_namespace}/${APP_NAME}:${BRANCH_NAME}_${imageBuildNumber}_${gitCommit}"
    updatedVersionInfo.service.build.commit="${gitCommit}"
    updatedVersionInfo.release.version=devInfo.release.version
    updatedVersionInfo.release.status=devInfo.release.status
    updatedVersionInfo.release.notes=devInfo.release.notes
  } else {
    def buildDate = new Date()
    updatedVersionInfo.service.build.date=buildDate.format("yyyy-MM-dd_HH:mm")
    updatedVersionInfo.service.build.number="${imageBuildNumber}"
    updatedVersionInfo.service.build.image="${IMAGE_REGISTRY}/${env_image_namespace}/${APP_NAME}:${BRANCH_NAME}_${imageBuildNumber}_${gitCommit}"
    updatedVersionInfo.service.build.commit="${gitCommit}"
  }
  println "Saving version.yaml file...\n${updatedVersionInfo}"
  writeYaml file: "${versionYaml}", data: updatedVersionInfo, overwrite: true
}
