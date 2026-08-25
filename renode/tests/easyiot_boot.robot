*** Settings ***
Suite Setup                   Setup
Suite Teardown                Teardown
Test Setup                    Reset Emulation
Resource                      ${RENODEKEYWORDS}

*** Variables ***
${SCRIPT}                     ${CURDIR}/../easyiot_esp32.resc
${UART}                       sysbus.uartSemihosting

*** Test Cases ***
Should Boot EasyIot ESP32 Firmware
    Execute Script            ${SCRIPT}
    Create Terminal Tester    ${UART}
    Start Emulation

    # Verify that the CPU starts execution
    Wait For Prompt On Uart   timeout=10
