/*
=======================================================================================
MotioCI → Cognos Automated Deployment Pipeline
Maintained by: DevOps Team
Purpose: Automate Cognos content promotion from DEV/TEST to PRD using MotioCI CLI.
=======================================================================================
Uses: Active Choice Reactive Parameters Plugin for dynamic dropdowns from MotioCI
=======================================================================================
*/

def branch = env.BRANCH_NAME ?: "DEV"
def namespace = env.NAMESPACE ?: "dev"
def cloudName = env.CLOUD_NAME == "openshift" ? "openshift" : "kubernetes"
def workingDir = "/home/jenkins/agent"

def APP_NAME = "combined-devops-cognos-deployments"

// ═══════════════════════════════════════════════════════════════════════════════════
// ACTIVE CHOICE REACTIVE PARAMETERS - Must be OUTSIDE pipeline block
// ═══════════════════════════════════════════════════════════════════════════════════
// Prerequisites: Install "Active Choices" plugin in Jenkins
//   - Manage Jenkins → Plugin Manager → Available → "Active Choices"
// ═══════════════════════════════════════════════════════════════════════════════════

properties([
  parameters([
    // ─────────────────────────────────────────────────────────────────────────
    // SOURCE_ENV: Dynamically fetch Cognos instances from MotioCI
    // ─────────────────────────────────────────────────────────────────────────
    [$class: 'ChoiceParameter',
      name: 'SOURCE_ENV',
      description: 'Source Cognos environment (fetched from MotioCI)',
      choiceType: 'PT_SINGLE_SELECT',
      filterLength: 1,
      filterable: true,
      randomName: 'source-env-choice',
      script: [
        $class: 'GroovyScript',
        fallbackScript: [
          classpath: [],
          sandbox: true,
          script: '''
            return ["Error fetching instances - check MotioCI connection"]
          '''
        ],
        script: [
          classpath: [],
          sandbox: false,
          script: '''
            import groovy.json.JsonSlurper
            import groovy.json.JsonOutput
            import javax.net.ssl.*
            import java.security.cert.X509Certificate
            
            // Disable SSL verification for self-signed certs
            def trustAllCerts = [
              checkClientTrusted: { chain, authType -> },
              checkServerTrusted: { chain, authType -> },
              getAcceptedIssuers: { null }
            ] as X509TrustManager
            
            def sc = SSLContext.getInstance("TLS")
            sc.init(null, [trustAllCerts] as TrustManager[], new java.security.SecureRandom())
            HttpsURLConnection.setDefaultSSLSocketFactory(sc.getSocketFactory())
            HttpsURLConnection.setDefaultHostnameVerifier({ hostname, session -> true } as HostnameVerifier)
            
            def motioServer = "https://cgrptmcip01.cloud.cammis.ca.gov"
            def graphUrl = "${motioServer}/api/graphql"
            def loginUrl = "${motioServer}/api/login"
            
            try {
              // Read credentials from Jenkins credential store
              def credentialsJson = ""
              try {
                def creds = com.cloudbees.plugins.credentials.CredentialsProvider.lookupCredentials(
                  com.cloudbees.plugins.credentials.common.StandardCredentials.class,
                  jenkins.model.Jenkins.instance,
                  null,
                  null
                ).find { it.id == 'cognos-credentials' }
                
                if (creds instanceof org.jenkinsci.plugins.plaincredentials.FileCredentials) {
                  credentialsJson = creds.getContent().text
                }
              } catch (Exception e) {
                def credsPath = "/var/jenkins_home/motio-creds.json"
                def credsFile = new File(credsPath)
                if (credsFile.exists()) {
                  credentialsJson = credsFile.text
                }
              }
              
              if (!credentialsJson) {
                return ["ERROR: Cannot read credentials file"]
              }
              
              // Login to MotioCI - Token is in RESPONSE HEADERS!
              def loginConn = new URL(loginUrl).openConnection()
              loginConn.setRequestMethod("POST")
              loginConn.setDoOutput(true)
              loginConn.setRequestProperty("Content-Type", "application/json")
              loginConn.getOutputStream().write(credentialsJson.getBytes("UTF-8"))
              
              // Get response code first
              def responseCode = loginConn.getResponseCode()
              if (responseCode != 200) {
                return ["ERROR: Login failed with status ${responseCode}"]
              }
              
              // Token comes from response HEADERS, not body!
              def authToken = loginConn.getHeaderField("x-auth-token")
              
              if (!authToken) {
                return ["ERROR: No x-auth-token in response headers"]
              }
              
              // Query instances from GraphQL API
              def instanceQuery = """{"query":"query { instances { edges { node { id name } } } }"}"""
              
              def graphConn = new URL(graphUrl).openConnection()
              graphConn.setRequestMethod("POST")
              graphConn.setDoOutput(true)
              graphConn.setRequestProperty("Content-Type", "application/json")
              graphConn.setRequestProperty("x-auth-token", authToken)
              graphConn.getOutputStream().write(instanceQuery.getBytes("UTF-8"))
              
              def graphResponse = new JsonSlurper().parseText(graphConn.getInputStream().getText())
              def instances = graphResponse?.data?.instances?.edges?.collect { it.node.name }
              
              if (!instances || instances.isEmpty()) {
                return ["No instances found"]
              }
              
              return instances
              
            } catch (Exception e) {
              return ["ERROR: ${e.getMessage()}"]
            }
          '''
        ]
      ]
    ],
    
    // ─────────────────────────────────────────────────────────────────────────
    // TARGET_ENV: Reactive parameter - excludes selected SOURCE_ENV
    // ─────────────────────────────────────────────────────────────────────────
    [$class: 'CascadeChoiceParameter',
      name: 'TARGET_ENV',
      description: 'Target Cognos environment (excludes source)',
      choiceType: 'PT_SINGLE_SELECT',
      filterLength: 1,
      filterable: true,
      randomName: 'target-env-choice',
      referencedParameters: 'SOURCE_ENV',
      script: [
        $class: 'GroovyScript',
        fallbackScript: [
          classpath: [],
          sandbox: true,
          script: '''
            return ["Error fetching target instances"]
          '''
        ],
        script: [
          classpath: [],
          sandbox: false,
          script: '''
            import groovy.json.JsonSlurper
            import groovy.json.JsonOutput
            import javax.net.ssl.*
            
            // Disable SSL verification
            def trustAllCerts = [
              checkClientTrusted: { chain, authType -> },
              checkServerTrusted: { chain, authType -> },
              getAcceptedIssuers: { null }
            ] as X509TrustManager
            
            def sc = SSLContext.getInstance("TLS")
            sc.init(null, [trustAllCerts] as TrustManager[], new java.security.SecureRandom())
            HttpsURLConnection.setDefaultSSLSocketFactory(sc.getSocketFactory())
            HttpsURLConnection.setDefaultHostnameVerifier({ hostname, session -> true } as HostnameVerifier)
            
            def motioServer = "https://cgrptmcip01.cloud.cammis.ca.gov"
            def graphUrl = "${motioServer}/api/graphql"
            def loginUrl = "${motioServer}/api/login"
            
            // Check if SOURCE_ENV is valid
            if (!SOURCE_ENV || SOURCE_ENV.toString().startsWith("ERROR") || SOURCE_ENV.toString().startsWith("No ")) {
              return ["Select valid source environment first"]
            }
            
            try {
              def credentialsJson = ""
              try {
                def creds = com.cloudbees.plugins.credentials.CredentialsProvider.lookupCredentials(
                  com.cloudbees.plugins.credentials.common.StandardCredentials.class,
                  jenkins.model.Jenkins.instance,
                  null,
                  null
                ).find { it.id == 'cognos-credentials' }
                
                if (creds instanceof org.jenkinsci.plugins.plaincredentials.FileCredentials) {
                  credentialsJson = creds.getContent().text
                }
              } catch (Exception e) {
                def credsFile = new File("/var/jenkins_home/motio-creds.json")
                if (credsFile.exists()) credentialsJson = credsFile.text
              }
              
              if (!credentialsJson) return ["ERROR: Cannot read credentials"]
              
              // Login - Token from HEADERS
              def loginConn = new URL(loginUrl).openConnection()
              loginConn.setRequestMethod("POST")
              loginConn.setDoOutput(true)
              loginConn.setRequestProperty("Content-Type", "application/json")
              loginConn.getOutputStream().write(credentialsJson.getBytes("UTF-8"))
              
              def responseCode = loginConn.getResponseCode()
              if (responseCode != 200) return ["ERROR: Login failed"]
              
              def authToken = loginConn.getHeaderField("x-auth-token")
              if (!authToken) return ["ERROR: No auth token"]
              
              // Query instances
              def instanceQuery = """{"query":"query { instances { edges { node { id name } } } }"}"""
              
              def graphConn = new URL(graphUrl).openConnection()
              graphConn.setRequestMethod("POST")
              graphConn.setDoOutput(true)
              graphConn.setRequestProperty("Content-Type", "application/json")
              graphConn.setRequestProperty("x-auth-token", authToken)
              graphConn.getOutputStream().write(instanceQuery.getBytes("UTF-8"))
              
              def graphResponse = new JsonSlurper().parseText(graphConn.getInputStream().getText())
              def instances = graphResponse?.data?.instances?.edges?.collect { it.node.name }
              
              // Filter out the source environment
              def filtered = instances?.findAll { it.toString() != SOURCE_ENV.toString() }
              
              if (!filtered || filtered.isEmpty()) {
                return ["No target instances available"]
              }
              
              return filtered
              
            } catch (Exception e) {
              return ["ERROR: ${e.getMessage()}"]
            }
          '''
        ]
      ]
    ],
    
    // ─────────────────────────────────────────────────────────────────────────
    // PROJECT_NAME: Reactive - fetches projects for selected SOURCE_ENV
    // ─────────────────────────────────────────────────────────────────────────
    [$class: 'CascadeChoiceParameter',
      name: 'PROJECT_NAME',
      description: 'MotioCI project (fetched based on source environment)',
      choiceType: 'PT_SINGLE_SELECT',
      filterLength: 1,
      filterable: true,
      randomName: 'project-name-choice',
      referencedParameters: 'SOURCE_ENV',
      script: [
        $class: 'GroovyScript',
        fallbackScript: [
          classpath: [],
          sandbox: true,
          script: '''
            return ["Error fetching projects"]
          '''
        ],
        script: [
          classpath: [],
          sandbox: false,
          script: '''
            import groovy.json.JsonSlurper
            import javax.net.ssl.*
            
            // SSL bypass
            def trustAllCerts = [
              checkClientTrusted: { chain, authType -> },
              checkServerTrusted: { chain, authType -> },
              getAcceptedIssuers: { null }
            ] as X509TrustManager
            def sc = SSLContext.getInstance("TLS")
            sc.init(null, [trustAllCerts] as TrustManager[], new java.security.SecureRandom())
            HttpsURLConnection.setDefaultSSLSocketFactory(sc.getSocketFactory())
            HttpsURLConnection.setDefaultHostnameVerifier({ hostname, session -> true } as HostnameVerifier)
            
            def motioServer = "https://cgrptmcip01.cloud.cammis.ca.gov"
            def graphUrl = "${motioServer}/api/graphql"
            def loginUrl = "${motioServer}/api/login"
            
            if (!SOURCE_ENV || SOURCE_ENV.toString().startsWith("ERROR") || SOURCE_ENV.toString().startsWith("No ")) {
              return ["Select source environment first"]
            }
            
            try {
              // Get credentials
              def credentialsJson = ""
              def creds = com.cloudbees.plugins.credentials.CredentialsProvider.lookupCredentials(
                com.cloudbees.plugins.credentials.common.StandardCredentials.class,
                jenkins.model.Jenkins.instance, null, null
              ).find { it.id == 'cognos-credentials' }
              if (creds instanceof org.jenkinsci.plugins.plaincredentials.FileCredentials) {
                credentialsJson = creds.getContent().text
              }
              if (!credentialsJson) return ["ERROR: No credentials"]
              
              // Login
              def loginConn = new URL(loginUrl).openConnection()
              loginConn.setRequestMethod("POST")
              loginConn.setDoOutput(true)
              loginConn.setRequestProperty("Content-Type", "application/json")
              loginConn.getOutputStream().write(credentialsJson.getBytes("UTF-8"))
              if (loginConn.getResponseCode() != 200) return ["ERROR: Login failed"]
              def authToken = loginConn.getHeaderField("x-auth-token")
              if (!authToken) return ["ERROR: No token"]
              
              // Query all projects then filter by instance name
              def sourceEnvName = SOURCE_ENV.toString()
              def projectQuery = '{"query":"{ instances { edges { node { name projects { edges { node { name } } } } } } }"}'
              
              def graphConn = new URL(graphUrl).openConnection()
              graphConn.setRequestMethod("POST")
              graphConn.setDoOutput(true)
              graphConn.setRequestProperty("Content-Type", "application/json")
              graphConn.setRequestProperty("x-auth-token", authToken)
              graphConn.getOutputStream().write(projectQuery.getBytes("UTF-8"))
              
              def json = new JsonSlurper().parseText(graphConn.getInputStream().getText())
              
              // Find the matching instance and get its projects
              def projects = []
              json?.data?.instances?.edges?.each { instanceEdge ->
                if (instanceEdge?.node?.name == sourceEnvName) {
                  instanceEdge?.node?.projects?.edges?.each { projectEdge ->
                    def pname = projectEdge?.node?.name
                    if (pname) {
                      projects.add(pname)
                    }
                  }
                }
              }
              
              if (projects.isEmpty()) {
                return ["No projects found in ${sourceEnvName}"]
              }
              
              return projects.sort()
              
            } catch (Exception e) {
              return ["ERROR: " + e.getMessage()]
            }
          '''
        ]
      ]
    ],
    
    // ─────────────────────────────────────────────────────────────────────────
    // VERSIONED_ITEM: Reactive - fetches versioned item paths for selected source environment
    // Returns only paths (no IDs), filtered by SOURCE_ENV only (not project)
    // ─────────────────────────────────────────────────────────────────────────
    [$class: 'CascadeChoiceParameter',
      name: 'VERSIONED_ITEM',
      description: 'Versioned item path to promote (fetched from MotioCI)',
      choiceType: 'PT_SINGLE_SELECT',
      filterLength: 1,
      filterable: true,
      randomName: 'versioned-item-choice',
      referencedParameters: 'SOURCE_ENV',
      script: [
        $class: 'GroovyScript',
        fallbackScript: [
          classpath: [],
          sandbox: true,
          script: '''
            return ["Error fetching versioned items"]
          '''
        ],
        script: [
          classpath: [],
          sandbox: false,
          script: '''
            import groovy.json.JsonSlurper
            import javax.net.ssl.*
            
            // SSL bypass
            def trustAllCerts = [
              checkClientTrusted: { chain, authType -> },
              checkServerTrusted: { chain, authType -> },
              getAcceptedIssuers: { null }
            ] as X509TrustManager
            def sc = SSLContext.getInstance("TLS")
            sc.init(null, [trustAllCerts] as TrustManager[], new java.security.SecureRandom())
            HttpsURLConnection.setDefaultSSLSocketFactory(sc.getSocketFactory())
            HttpsURLConnection.setDefaultHostnameVerifier({ hostname, session -> true } as HostnameVerifier)
            
            def motioServer = "https://cgrptmcip01.cloud.cammis.ca.gov"
            def graphUrl = "${motioServer}/api/graphql"
            def loginUrl = "${motioServer}/api/login"
            
            if (!SOURCE_ENV || 
                SOURCE_ENV.toString().startsWith("ERROR") || 
                SOURCE_ENV.toString().startsWith("Select") || 
                SOURCE_ENV.toString().startsWith("No ")) {
              return ["Select source environment first"]
            }
            
            try {
              // Get credentials
              def credentialsJson = ""
              def creds = com.cloudbees.plugins.credentials.CredentialsProvider.lookupCredentials(
                com.cloudbees.plugins.credentials.common.StandardCredentials.class,
                jenkins.model.Jenkins.instance, null, null
              ).find { it.id == 'cognos-credentials' }
              if (creds instanceof org.jenkinsci.plugins.plaincredentials.FileCredentials) {
                credentialsJson = creds.getContent().text
              }
              if (!credentialsJson) return ["ERROR: No credentials"]
              
              // Login
              def loginConn = new URL(loginUrl).openConnection()
              loginConn.setRequestMethod("POST")
              loginConn.setDoOutput(true)
              loginConn.setRequestProperty("Content-Type", "application/json")
              loginConn.getOutputStream().write(credentialsJson.getBytes("UTF-8"))
              if (loginConn.getResponseCode() != 200) return ["ERROR: Login failed"]
              def authToken = loginConn.getHeaderField("x-auth-token")
              if (!authToken) return ["ERROR: No token"]
              
              // Query versioned items - only prettyPath, no ID
              def sourceEnvName = SOURCE_ENV.toString()
              
              // Query all versioned items for the instance (across all projects)
              def query = '{"query":"{ instances { edges { node { name projects { edges { node { versionedItems(currentOnly: true) { edges { node { prettyPath } } } } } } } } } }"}'
              
              def graphConn = new URL(graphUrl).openConnection()
              graphConn.setRequestMethod("POST")
              graphConn.setDoOutput(true)
              graphConn.setRequestProperty("Content-Type", "application/json")
              graphConn.setRequestProperty("x-auth-token", authToken)
              graphConn.getOutputStream().write(query.getBytes("UTF-8"))
              
              def json = new JsonSlurper().parseText(graphConn.getInputStream().getText())
              
              // Find the matching instance, get all versioned items (across all projects)
              def paths = []
              json?.data?.instances?.edges?.each { instanceEdge ->
                if (instanceEdge?.node?.name == sourceEnvName) {
                  instanceEdge?.node?.projects?.edges?.each { projectEdge ->
                    projectEdge?.node?.versionedItems?.edges?.each { itemEdge ->
                      def path = itemEdge?.node?.prettyPath
                      if (path) {
                        // Force string conversion
                        String pathStr = "" + path
                        paths.add(pathStr)
                      }
                    }
                  }
                }
              }
              
              if (paths.isEmpty()) {
                return ["No versioned items in ${sourceEnvName}"]
              }
              
              // Return unique sorted paths
              return paths.unique().sort()
              
            } catch (Exception e) {
              return ["ERROR: " + e.getMessage()]
            }
          '''
        ]
      ]
    ],
    
    // ─────────────────────────────────────────────────────────────────────────
    // ROLLBACK_LABEL: Reactive - fetches existing labels for rollback
    // ─────────────────────────────────────────────────────────────────────────
    [$class: 'CascadeChoiceParameter',
      name: 'ROLLBACK_LABEL',
      description: 'Optional: select existing label to redeploy (for rollback)',
      choiceType: 'PT_SINGLE_SELECT',
      filterLength: 1,
      filterable: true,
      randomName: 'rollback-label-choice',
      referencedParameters: 'SOURCE_ENV,PROJECT_NAME',
      script: [
        $class: 'GroovyScript',
        fallbackScript: [
          classpath: [],
          sandbox: true,
          script: '''
            return ["(None - Create New Deployment)"]
          '''
        ],
        script: [
          classpath: [],
          sandbox: false,
          script: '''
            import groovy.json.JsonSlurper
            import javax.net.ssl.*
            
            // SSL bypass
            def trustAllCerts = [
              checkClientTrusted: { chain, authType -> },
              checkServerTrusted: { chain, authType -> },
              getAcceptedIssuers: { null }
            ] as X509TrustManager
            def sc = SSLContext.getInstance("TLS")
            sc.init(null, [trustAllCerts] as TrustManager[], new java.security.SecureRandom())
            HttpsURLConnection.setDefaultSSLSocketFactory(sc.getSocketFactory())
            HttpsURLConnection.setDefaultHostnameVerifier({ hostname, session -> true } as HostnameVerifier)
            
            def motioServer = "https://cgrptmcip01.cloud.cammis.ca.gov"
            def graphUrl = "${motioServer}/api/graphql"
            def loginUrl = "${motioServer}/api/login"
            
            // First option is always "no rollback"
            def labels = ["(None - Create New Deployment)"]
            
            if (!SOURCE_ENV || !PROJECT_NAME || 
                SOURCE_ENV.toString().startsWith("ERROR") || PROJECT_NAME.toString().startsWith("ERROR") ||
                SOURCE_ENV.toString().startsWith("Select") || PROJECT_NAME.toString().startsWith("No ") ||
                PROJECT_NAME.toString().contains("object Object")) {
              return labels
            }
            
            try {
              // Get credentials
              def credentialsJson = ""
              def creds = com.cloudbees.plugins.credentials.CredentialsProvider.lookupCredentials(
                com.cloudbees.plugins.credentials.common.StandardCredentials.class,
                jenkins.model.Jenkins.instance, null, null
              ).find { it.id == 'cognos-credentials' }
              if (creds instanceof org.jenkinsci.plugins.plaincredentials.FileCredentials) {
                credentialsJson = creds.getContent().text
              }
              if (!credentialsJson) return labels
              
              // Login
              def loginConn = new URL(loginUrl).openConnection()
              loginConn.setRequestMethod("POST")
              loginConn.setDoOutput(true)
              loginConn.setRequestProperty("Content-Type", "application/json")
              loginConn.getOutputStream().write(credentialsJson.getBytes("UTF-8"))
              if (loginConn.getResponseCode() != 200) return labels
              def authToken = loginConn.getHeaderField("x-auth-token")
              if (!authToken) return labels
              
              // Query all labels then filter by instance and project
              def sourceEnvName = SOURCE_ENV.toString()
              def projectName = PROJECT_NAME.toString()
              
              def query = '{"query":"{ instances { edges { node { name projects { edges { node { name labels { edges { node { name } } } } } } } } } }"}'
              
              def graphConn = new URL(graphUrl).openConnection()
              graphConn.setRequestMethod("POST")
              graphConn.setDoOutput(true)
              graphConn.setRequestProperty("Content-Type", "application/json")
              graphConn.setRequestProperty("x-auth-token", authToken)
              graphConn.getOutputStream().write(query.getBytes("UTF-8"))
              
              def json = new JsonSlurper().parseText(graphConn.getInputStream().getText())
              
              // Find the matching instance and project, get its labels
              json?.data?.instances?.edges?.each { instanceEdge ->
                if (instanceEdge?.node?.name == sourceEnvName) {
                  instanceEdge?.node?.projects?.edges?.each { projectEdge ->
                    if (projectEdge?.node?.name == projectName) {
                      projectEdge?.node?.labels?.edges?.each { labelEdge ->
                        def labelName = labelEdge?.node?.name
                        if (labelName) {
                          labels.add(labelName)
                        }
                      }
                    }
                  }
                }
              }
              
              return labels
              
            } catch (Exception e) {
              return labels
            }
          '''
        ]
      ]
    ]
  ])
])

// ═══════════════════════════════════════════════════════════════════════════════════
// PIPELINE DEFINITION
// ═══════════════════════════════════════════════════════════════════════════════════

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
          
          // Handle rollback label selection
          def rollbackLabel = params.ROLLBACK_LABEL
          if (rollbackLabel == "(None - Create New Deployment)") {
            rollbackLabel = ""
          }
          env.ROLLBACK_LABEL_CLEANED = rollbackLabel
          
          // VERSIONED_ITEM is now just the path (no ID)
          env.VERSIONED_ITEM_PATH = params.VERSIONED_ITEM ?: ""
          
          echo """
          ================================================
          MotioCI → Cognos Deployment Pipeline (Enhanced)
          ================================================
          Source: ${params.SOURCE_ENV}
          Target: ${params.TARGET_ENV}
          Project: ${params.PROJECT_NAME}
          Versioned Item Path: ${env.VERSIONED_ITEM_PATH}
          Rollback Label: ${env.ROLLBACK_LABEL_CLEANED ?: "N/A (New Deployment)"}
          ================================================
          """
          
          // Validate parameters
          if (params.SOURCE_ENV?.startsWith("ERROR") || params.SOURCE_ENV?.startsWith("Select")) {
            error("Invalid SOURCE_ENV selection: ${params.SOURCE_ENV}")
          }
          if (params.TARGET_ENV?.startsWith("ERROR") || params.TARGET_ENV?.startsWith("No target") || params.TARGET_ENV?.startsWith("Select")) {
            error("Invalid TARGET_ENV selection: ${params.TARGET_ENV}")
          }
          if (params.PROJECT_NAME?.startsWith("ERROR") || params.PROJECT_NAME?.startsWith("Select") || params.PROJECT_NAME?.startsWith("No ")) {
            error("Invalid PROJECT_NAME selection: ${params.PROJECT_NAME}")
          }
          if (!env.VERSIONED_ITEM_PATH || params.VERSIONED_ITEM?.startsWith("ERROR") || params.VERSIONED_ITEM?.startsWith("Select") || params.VERSIONED_ITEM?.startsWith("No ")) {
            error("Invalid VERSIONED_ITEM selection: ${params.VERSIONED_ITEM}")
          }
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
          }
        }
      }
    }

    stage('Prepare deployment') {
      when { expression { return !env.ROLLBACK_LABEL_CLEANED?.trim() } }
      steps {
        container('python') {
          sh '''
            set -e
            cd MotioCI/api/CLI

            TOKEN=$(cat ../token.txt)
            echo "Using MotioCI token (length: ${#TOKEN})"

            ITEM_PATH="${VERSIONED_ITEM_PATH}"
            
            if [ -z "${ITEM_PATH}" ]; then
              echo "ERROR: Versioned Item Path not provided!"
              exit 1
            fi
            
            echo "Versioned Item Path: ${ITEM_PATH}"
            echo "Project: ${PROJECT_NAME}"
            echo "Source Instance: ${SOURCE_ENV}"

            # Look up versioned item ID from the path
            echo "Looking up versioned item ID for path: ${ITEM_PATH}"
            python3 ci-cli.py --server="$MOTIO_SERVER" \
              versionedItems ls \
              --xauthtoken "$TOKEN" \
              --instanceName "${SOURCE_ENV}" \
              --projectName "${PROJECT_NAME}" > items_full.out

            # Find the ID for the exact path
            grep -A8 "prettyPath.: '${ITEM_PATH}'" items_full.out > items.out || true
            
            # Extract the ID
            ITEM_ID=$(grep "'id':" items.out | grep -v "instanceId" | grep -o "[0-9][0-9]*" | head -1 || true)
            
            if [ -z "${ITEM_ID}" ]; then
              echo "ERROR: Could not find versioned item ID for path: ${ITEM_PATH}"
              echo "Available paths in this project:"
              grep "prettyPath" items_full.out | head -20
              exit 1
            fi
            
            echo "Found Versioned Item ID: ${ITEM_ID}"

            # Create deployment label with the versioned item ID
            VERSION_NAME="AutoLabel_${BUILD_NUMBER}_$(date +%Y%m%d_%H%M)"
            echo "Creating Deployment Label: $VERSION_NAME with ID [${ITEM_ID}]"
            python3 ci-cli.py --server="$MOTIO_SERVER" label create \
              --xauthtoken "$TOKEN" \
              --instanceName "${SOURCE_ENV}" \
              --projectName "${PROJECT_NAME}" \
              --name "$VERSION_NAME" \
              --versionedItemIds "[${ITEM_ID}]"

            # Get the label ID for deployment
            python3 ci-cli.py --server="$MOTIO_SERVER" label ls \
              --xauthtoken "$TOKEN" \
              --instanceName "${SOURCE_ENV}" \
              --projectName "${PROJECT_NAME}" \
              --labelName "$VERSION_NAME" > label_info.out

            LABEL_ID=$(python3 -c "import ast; data=open('label_info.out').read(); parsed=ast.literal_eval(data); print(parsed['data']['instances']['edges'][0]['node']['projects']['edges'][0]['node']['labels']['edges'][0]['node']['id'])" 2>/dev/null || echo "")
            echo "$LABEL_ID" > ../label_id.txt
            echo "Label $VERSION_NAME (ID: $LABEL_ID) created successfully."

            echo "Verifying label contents ..."
            python3 ci-cli.py --server="$MOTIO_SERVER" label ls \
              --xauthtoken "$TOKEN" \
              --instanceName "${SOURCE_ENV}" \
              --projectName "${PROJECT_NAME}" \
              --labelName "$VERSION_NAME" > label_verify.out
            grep "prettyPath" label_verify.out || echo "(no paths found)"
          '''
        }
      }
    }
    
    stage('Retrieve CAMPassport & Deploy') {
        steps {
          container('python') {
            withCredentials([string(credentialsId: 'cognos-api-key-prd', variable: 'COGNOS_API_KEY_PRD')]) {
              sh '''
                set -e
                cd MotioCI/api/CLI

                # If rollback specified, skip label creation
                ROLLBACK_LABEL="${ROLLBACK_LABEL_CLEANED}"
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


