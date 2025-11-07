11:53:56  + echo 'Validating object path in source project...'
11:53:56  Validating object path in source project...
11:53:56  + echo 'Using searchPath=/Team Content/MotioCI Reports/Testing/Test Results Detail'
11:53:56  Using searchPath=/Team Content/MotioCI Reports/Testing/Test Results Detail
11:53:56  + python3 ci-cli.py --server=https://cgrptmcip01.cloud.cammis.ca.gov versionedItems ls --instanceName Cognos-DEV/TEST --projectName Demo --xauthtoken ca25348d-7300-476b-a695-0250d55e66b7 '--searchPath=/Team Content/MotioCI Reports/Testing/Test Results Detail' --currentOnly=True
11:53:56  + grep -F '/Team Content/MotioCI Reports/Testing/Test Results Detail'
11:53:56  Traceback (most recent call last):
11:53:56    File "/home/jenkins/agent/workspace/Cognos Jobs/testing/MotioCI/api/CLI/ci-cli.py", line 543, in <module>
11:53:56      versioned_items.get_versioned_items_specific(args.instanceName, args.projectName,
11:53:56    File "/home/jenkins/agent/workspace/Cognos Jobs/testing/MotioCI/api/CLI/versioned_items.py", line 32, in get_versioned_items_specific
11:53:56      versioned_item_array = response.json()["data"]["instances"]["edges"][0]["node"]["projects"]["edges"][0]["node"][
11:53:56  KeyError: 'data'
11:53:56  + echo 'Object /Team Content/MotioCI Reports/Testing/Test Results Detail not found in source project.'
11:53:56  Object /Team Content/MotioCI Reports/Testing/Test Results Detail not found in source project.
11:53:56  + echo 'Tip: Try checking the exact path in MotioCI UI (right-click → Properties).'
11:53:56  Tip: Try checking the exact path in MotioCI UI (right-click → Properties).
11:53:56  + exit 1
