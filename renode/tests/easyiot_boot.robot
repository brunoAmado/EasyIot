*** Settings ***
Suite Setup                   Setup
Suite Teardown                Teardown
Test Setup                    Reset Emulation
Resource                      ${RENODEKEYWORDS}

*** Variables ***
${SCRIPT}                     ${CURDIR}/../easyiot_esp32.resc
${UART}                       sysbus.uart0

*** Test Cases ***
Should Boot EasyIot ESP32 Firmware
    Execute Script            ${SCRIPT}
    Create Terminal Tester    ${UART}
    Start Emulation

    # Verify that the CPU starts and outputs serial boot information
    Wait For Line On Uart     [ONOFRE]    timeout=10
