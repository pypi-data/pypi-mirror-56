 
 Copy of https://pypi.org/project/robotframework-testrail/ library
 changed for python2 (only reporting part)
 
 # RobotFramework Testrail


Short Description
---

[Robot Framework](http://www.robotframework.org) library and listener for working with TestRail.

Installation
---

```
pip install robot-testrail-python2
```

Documentation
---

See documentation on [GitHub](https://github.com/peterservice-rnd/robotframework-testrail/tree/master/docs).

Usage
---

[How to enable TestRail API](http://docs.gurock.com/testrail-api2/introduction)

### TestRail API Client

Library for working with [TestRail](http://www.gurock.com/testrail/).

#### Example

```robot
*** Settings ***
Library    TestRailAPIClient    host    user    password    run_id

*** Test Cases ***
Case
    ${project}=    Get Project    project_id
    ${section}=    Add Section    project_id=${project['id']    name=New Section
    ${case}=       Add Case    ${section['id']}    Title    Steps    Description    Refs    type_id    priority_id
    Update Case    ${case['id']}    request_fields
```

### TestRail Listener

Fixing of testing results and updating test cases.

#### Example

1. Create custom field "case_description" with type "text", which corresponds to the Robot Framework's test case documentation.

2. Create Robot test:

    ```robot
    *** Test Cases ***
    Autotest name
        [Documentation]    Autotest documentation
        [Tags]    testrailid=10    defects=BUG-1, BUG-2    references=REF-3, REF-4
        Fail    Test fail message
    ```

3. Run Robot Framework with listener:

    ```
    pybot --listener TestRailListener.py:testrail_server_name:tester_user_name:tester_user_password:run_id:https:update  robot_suite.robot
    ```

    Test with case_id=10 will be marked as failed in TestRail with message "Test fail message" and defects "BUG-1, BUG-2".
    
    Also title, description and references of this test will be updated in TestRail. Parameter "update" is optional.


 

License
---

Apache License 2.0
 