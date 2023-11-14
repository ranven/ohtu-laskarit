*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Register Page

*** Test Cases ***
Register With Valid Username And Password
    Set Username  ville
    Set Password  ville123
    Set Password Confirmation  ville123
    Submit Credentials
    Register Should Succeed

Register With Too Short Username And Valid Password
    Set Username  v
    Set Password  ville123
    Set Password Confirmation  ville123
    Submit Credentials
    Register Should Fail With Message  Invalid username. Username must be at least 3 characters long and consist of letters a-z

Register With Valid Username And Invalid Password
    Set Username  vvvvv
    Set Password  vvvvvvvvv
    Set Password Confirmation  vvvvvvvvv
    Submit Credentials
    Register Should Fail With Message  Invalid password. Password must be at least 8 characters long and not consist of only letters.

Register With Nonmatching Password And Password Confirmation
    Set Username  villeville
    Set Password  ville123
    Set Password Confirmation  ville456
    Submit Credentials
    Register Should Fail With Message  Password confirmation didn't match the password.

Login After Successful Registration
    Set Username  venla
    Set Password  venla123
    Set Password Confirmation  venla123
    Submit Credentials
    Register Should Succeed
    Go To Login Page 
    Login Page Should Be Open
    Set Username  venla
    Set Password  venla123
    Submit Login Credentials
    Login Should Succeed

Login After Failed Registration
    Set Username  venlavenla
    Set Password  venlavenla
    Set Password Confirmation  venlavenla
    Submit Credentials
    Register Should Fail With Message  Invalid password. Password must be at least 8 characters long and not consist of only letters.
    Go To Login Page
    Login Page Should Be Open
    Set Username  venlavenla
    Set Password  venlavenla
    Submit Login Credentials
    Login Should Fail With Message  Invalid username or password


*** Keywords ***
Register Should Succeed
    Welcome Page Should Be Open

Register Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}

Submit Credentials
    Click Button  Register

Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}

Set Password Confirmation
    [Arguments]  ${password_confirmation}
    Input Password  password_confirmation  ${password_confirmation}

Submit Login Credentials 
    Click Button  Login

Login Should Succeed 
    Main Page Should Be Open

Login Should Fail With Message
    [Arguments]  ${message}
    Login Page Should Be Open
    Page Should Contain  ${message}