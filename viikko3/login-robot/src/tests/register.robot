*** Settings ***
Resource  resource.robot
Test Setup  Input New Command and Create User

*** Test Cases ***
Register With Valid Username And Password
    Input Credentials  ville  ville123
    Output Should Contain  New user registered

Register With Already Taken Username And Valid Password
    Input Credentials  kalle  kalle123
    Output Should Contain  Username is already taken

Register With Too Short Username And Valid Password
    Input Credentials  k  kalle123
    Output Should Contain  Invalid username. Username must be at least 3 characters long and consist of letters a-z

Register With Enough Long But Invald Username And Valid Password
    Input Credentials  kalle123  kalle123
    Output Should Contain  Invalid username. Username must be at least 3 characters long and consist of letters a-z

Register With Valid Username And Too Short Password
    Input Credentials  ville  vv
    Output Should Contain  Invalid password. Password must be at least 8 characters long and not consist of only letters.

Register With Valid Username And Long Enough Password Containing Only Letters
        Input Credentials  ville  villeville
    Output Should Contain  Invalid password. Password must be at least 8 characters long and not consist of only letters.

*** Keywords ***
Input New Command And Create User
    Create User  kalle  kalle123
    Input New Command

