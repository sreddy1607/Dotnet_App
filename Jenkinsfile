
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
                            curl -k -v -H "Authorization: Bearer ZXlKaGJHY2lPaUpTVXpJMU5pSXNJbXRwWkNJNkluSTROelpWTlRKV1NGZHNOeTFRY1U1b1JubEpVMGxJUlhOeldrSjBPRk5KTTAxb1pHSnBPVTAxVURBaWZRLmV5SnBjM01pT2lKcmRXSmxjbTVsZEdWekwzTmxjblpwWTJWaFkyTnZkVzUwSWl3aWEzVmlaWEp1WlhSbGN5NXBieTl6WlhKMmFXTmxZV05qYjNWdWRDOXVZVzFsYzNCaFkyVWlPaUowYjI5c2N5SXNJbXQxWW1WeWJtVjBaWE11YVc4dmMyVnlkbWxqWldGalkyOTFiblF2YzJWamNtVjBMbTVoYldVaU9pSmlkV2xzWkdWeUxYUnZhMlZ1TFdSemJEWnlJaXdpYTNWaVpYSnVaWFJsY3k1cGJ5OXpaWEoyYVdObFlXTmpiM1Z1ZEM5elpYSjJhV05sTFdGalkyOTFiblF1Ym1GdFpTSTZJbUoxYVd4a1pYSWlMQ0pyZFdKbGNtNWxkR1Z6TG1sdkwzTmxjblpwWTJWaFkyTnZkVzUwTDNObGNuWnBZMlV0WVdOamIzVnVkQzUxYVdRaU9pSm1NemxoWVRNNFpTMHhZalZpTFRSa01XWXRZakV3T1MxaFkyRTFNREl5WmpZM01URWlMQ0p6ZFdJaU9pSnplWE4wWlcwNmMyVnlkbWxqWldGalkyOTFiblE2ZEc5dmJITTZZblZwYkdSbGNpSjkuZTN3akNxWXBiQV9oaHVXY0drUzVlLWRGa2VObFd5MGdEaUxuSzNVbjRnemFsZ0hYcXVlR2I3Z3FuMEpWSU9PakJzOGFtMDJjVXd2MEkwR0YwSzl5dFdrVkxFZ3B0RUU1eXpZUDQyZUtIY0Q4dzA0bXF6RzNQaTR3SGV2eUQ0N1hVWEVnUlAtVy11QTdmUVc3dTRTY1owem93WlBhMEZlNUcyX0pJX2VrTFdGY2RHWVdyam1EZWZpdkl5c1gxUkxHUDJHcGw1bS1xLTl4aDFHbWdtV1BsaDVlbDM0b1BDdW1jYV9pQTdYTTdONHhCbjZFczVaelhxQTJFLW9RTUVYYjF1RjR4c3NSSXltZkVYeVI5Q3k5ajZzT19tdUpNVUxuamlhblpZcmxDRGJtSXdkc0F5SUM2Z1kzQ3ZPVFBnYWJCc29TWHJBWXB2MlhHQlRIRjJLcFNpTXRGUlZiME5WU2pXWFd1bm9KeWk4Skt2VTZMTjJtZzNCOUlNbk94NlBUajBpVy1rRUwyR2JnbUNya2hIbnUzVUlrdWRnVFI2MmcwcmlHWW9ya3pvN1ZvMFg5czcxWjNoYUpLNWZBeHZTMlRLWF8yMTdZTml4LTNjZXlBdzEyNFRPSi11V09kMEY1ZzhqMWRiLWt3b3YxWnhLNU1NUENMejNFMTVZemh4cFZuRzRkaExhMjFXckdEMTFfdDkwQzBJRHlNY0VsajF5WFpubUlMUVR5M0tQRExiWHRxRWxYdUNmNW13UjQ3b0g5eVhGNDZEdEMwWHFOSDZhcExTMWZMbmF0Mm1BTVpWNWlMZ3JqbWpFU3hxQmRULUxaNkRpbzNLT3RmZDRabnhqVC1YQ2dlRlBhbTNBb3A1VU0xWmI1U0MtZlg0WXNFcmNNdy1aT0NrUzV0Mjg=" \
                                 --upload-file Dotnet_App/$artifactFile \
                                 $nexusUrl
                        """
                    }
                }
            }
        }


}


 
}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
