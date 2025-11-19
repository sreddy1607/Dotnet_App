parameters([
                  [
                    $class: 'ChoiceParameter',
                    choiceType: 'PT_SINGLE_SELECT',
                    // filterLength: 1,
                    // filterable: false,
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
                                return["${env.BRANCH_NAME}"]
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
                                  "return['Could not get the environments']"
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
