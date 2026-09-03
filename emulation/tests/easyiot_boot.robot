*** Settings ***
Suite Setup                   Setup
Suite Teardown                Teardown
Test Setup                    Reset Emulation
Resource                      ${RENODEKEYWORDS}

*** Variables ***
${SCRIPT}                     ${CURDIR}/../easyiot_esp32.resc
${UART}                       cpu.uartSemihosting

*** Test Cases ***
Should Boot EasyIot ESP32 Firmware
    Execute Script            ${SCRIPT}
    Start Emulation

    # Let the CPU execute and verify active execution state
    Sleep                     1s
    ${pc}=                    Execute Command    cpu PC
    Log                       CPU Program Counter: ${pc}
    ${time}=                  Execute Command    emulation GetTime
    Log                       Emulation Virtual Time: ${time}
