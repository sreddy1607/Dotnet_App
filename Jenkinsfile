
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
                            curl -k -v -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6InI4NzZVNTJWSFdsNy1QcU5oRnlJU0lIRXNzWkJ0OFNJM01oZGJpOU01UDAifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJqZW5raW5zLWJ1aWxkZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlY3JldC5uYW1lIjoiamVua2lucy10b2tlbi1xcXNiMiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJqZW5raW5zIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiYTBlY2Y3ZTgtOWMyMy00N2EyLWJlOGUtMjU0NGIxOTRhY2Q4Iiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50OmplbmtpbnMtYnVpbGRlcjpqZW5raW5zIn0.n0pGpUYsT0qK5ITzdGdXEEUWRGp-NQohw8X8PgDTlBFmEu3qg7CYBiQcSVgIxLQj9xrKkMWJe_90fdvJY4z1sP7ec6IjFwOlOAyUUUTG48eU7qt0Jjuj4gZ5MhZt67xHAOcmCe7CG6j6tlq1o2lsX6ZGQA7YLdgZcac4CbUH0efw-IrBFBVVQwz2fbSfJ40izhf3I1-A7me3UwbpbBv5TfDvAqjIC1WbkSIyf0UvbXqKkiS4DKmB9yaPlbdW2-Jwfrb_20Xa8kkC5mYbcazWxHNL7sBbj3rJtNkn1vm48iqeRXlZF2wAQ_phQLHkjq_CANM5RaRo042pcFyY70h-nocsqN_UEZuB5-1O2DqJOup8LO_jFaPkQEQVYnxZhlNMvRdVPV0M8OpnOm0UCn80xQhKtyOqxPRm0M_DJdkdq53qYV2OB7QM40O_y2I-clHqMMq2Mvxe-4NwAQ1T1W3U6D0lls8l0i24JBeHyJQ4A-HdJkI0yxVozFFqFsAMO_0b6g_N_fpzFQ9ch-IeX4mIqe24Eq7DmOEsxCE4PhGS7_Lh0UWkNNqvU1-keBAd7TgHrja0TIfXup-MuCnoh8chtnrB7lmxJ4zIn2HBTpHTHG7UpL4PshiSarLcw4NMkj07h4BjtBYfjLFc-n83WBxuB6VJFJ35-iS0h0BX6P0jbTQ" /
                                 -F file=@Dotnet_App/$artifactFile \
                                 $nexusUrl
                        """
                    }
                }
            }
        }


}


 
}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
