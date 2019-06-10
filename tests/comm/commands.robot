*** Settings ***
Documentation    Test basic commands
Library    mock_dmm_dut.MockDmmDut    ${PORT}    WITH NAME    ser

*** Test Cases ***
Version
    [Documentation]    Verify VER response is correctly formatted
    ser.write    VER
    ${rsp} =    ser.read    1.0
    Should Match Regexp    ${rsp}    [0-9]+\\.[0-9]+\\.[0-9]
