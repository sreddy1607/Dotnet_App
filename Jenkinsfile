def branch = env.BRANCH_NAME ?: "ecr"
def namespace = env.NAMESPACE ?: "dev"
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
            - name: mspdotnet
              image: 136299550619.dkr.ecr.us-west-2.amazonaws.com/cammismspapp:1.0.35
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
                - name: NEXUS_ACCESS_TOKEN
                  valueFrom:
                    secretKeyRef:
                      name: jenkins-token-qqsb2
                      key: token
                - name: GIT_SSL_CAINFO
                  value: "/etc/pki/tls/certs/ca-bundle.crt"
              volumeMounts:
                - name: jenkins-trusted-ca-bundle
                  mountPath: /etc/pki/tls/certs
      """
    }
  }

  options {
    disableConcurrentBuilds()
    timeout(time: 5, unit: 'HOURS')
    skipDefaultCheckout()
    buildDiscarder(logRotator(numToKeepStr: '20'))
  }

  environment {
    env_git_branch_type = "feature"
    env_git_branch_name = ""
    env_current_git_commit = ""
    env_skip_build = "false"
    env_stage_name = ""
    env_step_name = ""
    DOTNET_CLI_TELEMETRY_OPTOUT = '1'
  }

  stages {
    stage("Initialize") {
      steps {
        container(name: "node") {
          script {
            properties([
              parameters([])
            ])

            env_stage_name = "initialize"
            env_step_name = "checkout"

            deleteDir()
            echo 'Checkout source and get the commit ID'
            // env_current_git_commit = checkout(scm).GIT_COMMIT

            echo 'Loading properties file'
            env_step_name = "load properties"
            // load the pipeline properties
            // load(".jenkins/pipelines/Jenkinsfile.ecr.properties")

            env_step_name = "set global variables"
            echo 'Initialize Slack channels and tokens'
            // initSlackChannels()

            // env_git_branch_name = BRANCH_NAME
            // env_current_git_commit = "${env_current_git_commit[0..7]}"
            // echo "The commit hash from the latest git current commit is ${env_current_git_commit}"
            // currentBuild.displayName = "#${BUILD_NUMBER}"
            // slackNotification("pipeline","${APP_NAME}-${env_git_branch_name}: <${BUILD_URL}console|build #${BUILD_NUMBER}> started.","#439FE0","false")
          }
        }
      }
    }

       stage('Upload Artifact to Nexus') {
      steps {
        container('mspdotnet') {
          script {
            withCredentials([usernamePassword(credentialsId: 'nexus-credentials', passwordVariable: 'NEXUS_PASSWORD', usernameVariable: 'NEXUS_USERNAME')]) {
              def nexusUrl = "http://nexusrepo-sonatype-nexus-service.tools.svc.cluster.local:8081/repository/cammis-dotnet-repo-group"
              def artifactFile = "compose.yaml"

              sh '''
             
              yum update
              yum install -y ca-certificates
              yum update -y
# Import the Microsoft repository GPG keys
rpm -Uvh https://packages.microsoft.com/config/centos/8/packages-microsoft-prod.rpm

# Enable the .NET repository
yum install -y dotnet-sdk-6.0

# Verify .NET installation
dotnet --version

             # wget https://dist.nuget.org/win-x86-commandline/latest/nuget.exe -O /usr/local/bin/nuget
              #chmod +x /usr/local/bin/nuget
                rm -rf Dotnet_App
                git clone https://github.com/sreddy1607/Dotnet_App.git
                ls -l
                dotnet restore Dotnet_App/src/
                dotnet publish Dotnet_App/src/ -c Release
                dotnet nuget setapikey 7eb5424c-5f47-381c-b1fa-8c8592508455 -source http://nexusrepo-sonatype-nexus-service.tools.svc.cluster.local:8081/repository/cammis-dotnet-repo-group/
                
                #curl -kv -u Eshwar:Redd1234 -F "file=@appsettings.json" "http://nexusrepo-sonatype-nexus-service.tools.svc.cluster.local:8081/repository/cammis-dotnet-repo-group/appsettings.json"
              '''
            }
          }
        }
      }
    }
  }
}
