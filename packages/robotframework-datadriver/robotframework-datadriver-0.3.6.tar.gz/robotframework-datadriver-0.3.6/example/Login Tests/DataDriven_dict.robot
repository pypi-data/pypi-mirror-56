*** Settings ***
Library           DataDriver
Library           Collections
Resource          login_resources.robot

Suite Setup       Open my Browser
Suite Teardown    Close Browsers
Test Setup        Open Login Page
Test Template     Invalid Login
Force Tags        1    2

*** Test Cases ***
Login with user '${user}' and password '${user.pwd}'    Default    UserData

*** Keywords ***
Invalid login
    [Arguments]    ${user}
    log    ${user}
    &{user}=    evaluate     json.loads('''${user}''')    json
    log    ${user}
    Input username    ${user.name}
    Input pwd    ${user.pwd}
    click login button
    Error page should be visible
