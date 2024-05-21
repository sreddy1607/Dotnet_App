
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
            - name: mspdotnet
              image: 136299550619.dkr.ecr.us-west-2.amazonaws.com/cammismspapp:1.0.35
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
    //timestamps()
    disableConcurrentBuilds()
    timeout(time:5 , unit: 'HOURS')
    skipDefaultCheckout()
    buildDiscarder(logRotator(numToKeepStr: '20'))
  }

  environment {
    env_git_branch_type="feature"
    env_git_branch_name=""
    env_current_git_commit=""
    env_skip_build="false"
    env_stage_name=""
    env_step_name=""
    DOTNET_CLI_TELEMETRY_OPTOUT = '1'
    


  }

  stages {
    stage("initialize") {
      steps {
        container(name: "node") {
          script {

            properties([
              parameters([
                // booleanParam(name: 'S3', defaultValue: false, description: 'select S3 to upload the truststore file')        
		//string(name: 'CLIENT_EMAIL', defaultValue: 'srinivas.reddy@dhcs.ca.gov', description: 'Client Email Address')
              ])
            ])

            env_stage_name = "initialize"
            env_step_name = "checkout"

            deleteDir()

            echo 'checkout source  and get the commit id'
            //env_current_git_commit = checkout(scm).GIT_COMMIT

            echo 'Loading properties file'
            env_step_name = "load properties"
            // load the pipeline properties
            // load(".jenkins/pipelines/Jenkinsfile.ecr.properties")

            env_step_name = "set global variables"
            echo 'initialize slack channels and tokens'
            //initSlackChannels()

            //env_git_branch_name = BRANCH_NAME


            // get the short version of commit
           //env_current_git_commit="${env_current_git_commit[0..7]}"
            //echo "The commit hash from the latest git current commit is ${env_current_git_commit}"
                      
            //include commit id in build name
            currentBuild.displayName = "#${BUILD_NUMBER}"

           // slackNotification("pipeline","${APP_NAME}-${env_git_branch_name}: <${BUILD_URL}console|build #${BUILD_NUMBER}> started.","#439FE0","false")
          } //END script
        } //END container node
      } //END steps
    } //END stage

  
stage('test dotnet image') {
    steps {
         
        container(name: "mspdotnet") {
		
            script {
                withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'jenkins-ecr', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                
                   
                    sh """
		                dotnet --version 
		
                   # git clone https://github.com/sreddy1607/Dotnet_App.git
		    #ls -l
                    #dotnet restore Dotnet_App/src/
		    #dotnet publish Dotnet_App/src/ -c Release
                    java --version
		    which java
                    echo $PATH
		  
                    
		
                    ls -l /opt/sonar-scanner/sonar-scanner-5.0.1.3006
		    #ls -l /opt/sonar-scanner/sonar-scanner-6.2.0.85879-net-framework
                     ls -l  /opt/sonar-scanner/latest/bin/
                    /opt/sonar-scanner/latest/bin/sonar-scanner --version

                    """
                }
            }
        }
        
    }
	}
	stage('Upload Artifact to Nexus') {
            steps {
                container('mspdotnet') {
                    script {
                        def nexusUrl = "https://nexusrepo-tools.apps.bld.cammis.medi-cal.ca.gov/repository/cammis-dotnet-repo-group/"
                        def artifactFile = "compose.yaml"

                        sh """
			   git clone https://github.com/sreddy1607/Dotnet_App.git
                           ls -l Dotnet_App
			   ls -l Dotnet_App/src/
                            curl -k -v -H "Authorization: Bearer ZXlKaGJHY2lPaUpTVXpJMU5pSXNJbXRwWkNJNkluSTROelpWTlRKV1NGZHNOeTFRY1U1b1JubEpVMGxJUlhOeldrSjBPRk5KTTAxb1pHSnBPVTAxVURBaWZRLmV5SnBjM01pT2lKcmRXSmxjbTVsZEdWekwzTmxjblpwWTJWaFkyTnZkVzUwSWl3aWEzVmlaWEp1WlhSbGN5NXBieTl6WlhKMmFXTmxZV05qYjNWdWRDOXVZVzFsYzNCaFkyVWlPaUpxWlc1cmFXNXpMV0oxYVd4a1pYSWlMQ0pyZFdKbGNtNWxkR1Z6TG1sdkwzTmxjblpwWTJWaFkyTnZkVzUwTDNObFkzSmxkQzV1WVcxbElqb2lhbVZ1YTJsdWN5MTBiMnRsYmkxeGNYTmlNaUlzSW10MVltVnlibVYwWlhNdWFXOHZjMlZ5ZG1salpXRmpZMjkxYm5RdmMyVnlkbWxqWlMxaFkyTnZkVzUwTG01aGJXVWlPaUpxWlc1cmFXNXpJaXdpYTNWaVpYSnVaWFJsY3k1cGJ5OXpaWEoyYVdObFlXTmpiM1Z1ZEM5elpYSjJhV05sTFdGalkyOTFiblF1ZFdsa0lqb2lZVEJsWTJZM1pUZ3RPV015TXkwME4yRXlMV0psT0dVdE1qVTBOR0l4T1RSaFkyUTRJaXdpYzNWaUlqb2ljM2x6ZEdWdE9uTmxjblpwWTJWaFkyTnZkVzUwT21wbGJtdHBibk10WW5WcGJHUmxjanBxWlc1cmFXNXpJbjAubjBwR3BVWXNUMHFLNUlUemRHZFhFRVVXUkdwLU5Rb2h3OFg4UGdEVGxCRm1FdTNxZzdDWUJpUWNTVmdJeExRajl4cktrTVdKZV85MGZkdkpZNHoxc1A3ZWM2SWpGd09sT0F5VVVVVEc0OGVVN3F0MEpqdWo0Z1o1TWhadDY3eEhBT2NtQ2U3Q0c2ajZ0bHExbzJsc1g2WkdRQTdZTGRnWmNhYzRDYlVIMGVmdy1JckJGQlZWUXd6MmZiU2ZKNDBpemhmM0kxLUE3bWUzVXdicGJCdjVUZkR2QXFqSUMxV2JrU0l5ZjBVdmJYcUtraVM0REttQjl5YVBsYmRXMi1Kd2ZyYl8yMFhhOGtrQzVtWWJjYXpXeEhOTDdzQmJqM3JKdE5rbjF2bTQ4aXFlUlhsWkYyd0FRX3BoUUxIa2pxX0NBTk01UmFSbzA0MnBjRnlZNzBoLW5vY3NxTl9VRVp1QjUtMU8yRHFKT3VwOExPX2pGYVBrUUVRVllueFpobE5NdlJkVlBWME04T3BuT20wVUNuODB4UWhLdHlPcXhQUm0wTV9ESmRrZHE1M3FZVjJPQjdRTTQwT195MkktY2xIcU1NcTJNdnhlLTROd0FRMVQxVzNVNkQwbGxzOGwwaTI0SkJlSHlKUTRBLUhkSmtJMHl4Vm96RkZxRnNBTU9fMGI2Z19OX2ZwekZROWNoLUllWDRtSXFlMjRFcTdEbU9Fc3hDRTRQaEdTN19MaDBVV2tOTnF2VTEta2VCQWQ3VGdIcmphMFRJZlh1cC1NdUNub2g4Y2h0bnJCN2xteEo0ekluMkhCVHBIVEhHN1VwTDRQc2hpU2FyTGN3NE5Na2owN2g0Qmp0QllmakxGYy1uODNXQnh1QjZWSkZKMzUtaVMwaDBCWDZQMGpiVFE" \
                                 --upload-file Dotnet_App/$artifactFile \
                                 $nexusUrl
                        """
                    }
                }
            }
        }


}


 
}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
