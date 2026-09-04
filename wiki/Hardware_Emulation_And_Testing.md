# 🚀 Emulação de Hardware, Toolchain e Testes do Web Panel

O EasyIot suporta **emulação real de hardware (instruções de máquina Xtensa)** com **Renode**, **simulação interativa de interface web** via Node.js/Express, e testes ponta-a-ponta (E2E) com **Playwright**, permitindo desenvolver, compilar e validar firmware e interfaces sem necessidade de placas físicas conectadas.

---

## 1. 🛠️ Pré-Requisitos e Configuração do Ambiente

### A. PlatformIO Core CLI
Para compilar o firmware via terminal:
```powershell
# Instalar / Atualizar o PlatformIO Core via Python 3.11+
py -3.11 -m pip install -U platformio

# Adicionar ao PATH do utilizador (se necessário)
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
[Environment]::SetEnvironmentVariable("Path", "$currentPath;C:\dev_tools\Python311\Scripts;C:\dev_tools\Python311", "User")
```

Verificar a instalação:
```powershell
pio --version
# Output: PlatformIO Core, version 6.x.x
```

### B. Renode (Emulador de Hardware Open-Source)
[Renode](https://renode.io/) (desenvolvido pela Antmicro) emula núcleos Xtensa LX6 dual-core e periféricos MMIO a nível de instrução:

* **Windows:**
  ```powershell
  winget install Renode.Renode
  # Instalado por defeito em: C:\Program Files\Renode\bin\Renode.exe
  ```
* **Linux (Ubuntu / Debian):**
  ```bash
  sudo apt-get install renode
  ```
* **macOS:**
  ```bash
  brew install --cask renode
  ```

---

## 2. ⚙️ Compilação do Firmware

Antes de iniciar a emulação, compile o binário ELF alvo:

```powershell
# Compilar versão ESP32 Debug
pio run -e ESP32_DEBUG

# Compilar versão ESP8266 Debug
pio run -e ESP8266_DEBUG
```

O binário gerado para a emulação fica localizado em:
📂 `.pio/build/ESP32_DEBUG/firmware.elf`

---

## 3. 🧠 Emulação de Hardware ESP32 com Renode

### Ficheiros de Configuração:
* **[`emulation/platforms/easyiot_esp32.repl`](file:///c:/Users/bruno/CLionProjects/EasyIot/emulation/platforms/easyiot_esp32.repl):**
  * Define o CPU Xtensa LX6 dual-core (`240 MHz`).
  * Mapeamento de memória:
    * `data_space`: `0x00000000 - 0x3FFFFFFF` (1 GB)
    * `inst_space`: `0x40000000 - 0x40FFFFFF` (16 MB - IRAM / Flash Cache)
    * `rom`: `0x50000000 - 0x53FFFFFF` (64 MB)
    * `ram`: `0x60000000 - 0x67FFFFFF` (128 MB)
    * `high_mmio`: `0x80000000 - 0x80FFFFFF` (16 MB - absorve acessos de registos WDT/MMIO)
  * Periféricos: LEDs virtuais para `relay1`, `relay2`, `valve_ring_1` a `valve_ring_4`, e `uartSemihosting`.
* **[`emulation/easyiot_esp32.resc`](file:///c:/Users/bruno/CLionProjects/EasyIot/emulation/easyiot_esp32.resc):**
  * Inicializa registos de arranque Xtensa (`PS`, `A1`, `WINDOWBASE`, `WINDOWSTART`).
  * Ignora sondagem de coprocessador F64 inexistente no HAL Xtensa.
  * Interceta handlers de pânico e reinicialização (`esp_restart_noos`).
* **[`emulation/tests/easyiot_boot.robot`](file:///c:/Users/bruno/CLionProjects/EasyIot/emulation/tests/easyiot_boot.robot):**
  * Suite de testes automatizados em Robot Framework.

### Como Executar o Emulador:

#### Modo Interativo com Consola Gráfica e UART Semihosting:
```powershell
& "C:\Program Files\Renode\bin\Renode.exe" emulation/easyiot_esp32.resc
```

#### Modo Linha de Comandos (Headless):
```powershell
& "C:\Program Files\Renode\bin\Renode.exe" --plain -e "include @emulation/easyiot_esp32.resc; start"
```

#### Comandos Úteis na Consola do Renode (`monitor`):
```text
(monitor) cpu PC                      # Consulta o Program Counter atual
(monitor) cpu ExecutedInstructions   # Número de instruções de máquina executadas
(monitor) currentTime                 # Tempo decorrido de emulação
(monitor) relay1 State                # Estado do relé 1 (True / False)
(monitor) valve_ring_1 State          # Estado da válvula da fonte
(monitor) pause                       # Pausa a execução do CPU
(monitor) start                       # Retoma a execução
(monitor) runMacro $reset             # Faz reset à máquina e recarrega o ELF
```

### Diagnóstico de Avisos Sysbus no Renode:
Se o firmware aceder a endereços de periféricos durante rotinas de Watchdog Timer ou reinicialização (`esp_restart_noos`):
* `0x4009471A` escreve `0x50D83AA1` (`TIMG_WDT_WKEY_VALUE` de desbloqueio de escrita WDT).
* `0x40094796` / `0x4009479F` desativam o watchdog antes do reboot.
* O mapeamento `high_mmio` no ficheiro `.repl` absorve estes acessos sem gerar erros de periférico inexistente.
* O hook em `0x40083c24` interceta o reboot suave para evitar loops infinitos de pânico.

---

## 4. 🌐 Como Iniciar e Testar o Web Panel

O Renode emula a execução das instruções do CPU, mas não emula a camada física rádio 802.11 Wi-Fi proprietária do ESP32. Para testar o **Web Panel** e as APIs REST, o projeto fornece um servidor mock integrado de alta fidelidade:

### A. Servidor Mock Interativo (Node.js / Express)

Inicia o servidor web local servindo o frontend [`webpanel/`](file:///c:/Users/bruno/CLionProjects/EasyIot/webpanel) com todos os endpoints REST do firmware simulados (`/config`, `/state`, `/save`, `/scan`, `/firmware`, etc.):

```powershell
node -e "require('./web-tests/mock-server.js').startServer(3000)"
```

Aceda no navegador em:
👉 **[http://localhost:3000](http://localhost:3000)**

### B. Testes Automatizados E2E do Web Panel (Playwright)

Para executar a validação completa de interface e componentes gráficos (Radar Studio, AquaDance, Rega, Diagnósticos):

```powershell
cd web-tests

# Executar todos os testes
npm test

# Executar testes de componentes específicos
npm run test:radar        # Radar Studio UI & Canvas
npm run test:aquadance    # AquaDance Show Matrix
npm run test:irrigation   # Agendador de Rega
npm run test:diagnostics  # Painel de Diagnóstico do Sistema
npm run test:resiliency   # Resiliência de rede e timeouts
```

### C. Conversão e Minificação de Assets Web para C++ PROGMEM

Sempre que modificar ficheiros em `webpanel/` (`index.html`, `css/styles.css`, `js/index.js`), converta-os em cabeçalhos C++ embebidos antes de compilar o firmware:

```powershell
python tools/html_converter.py
```
*(Gera os ficheiros `include/IndexHtml.h`, `include/StylesMinCss.h` e `include/IndexJs.h`)*

---

## 5. 🔌 Execução em Hardware Físico Real

Ao carregar o firmware numa placa real (OnOfre V5/V6, ESP32, ESP8266):

1. **Modo Estação (Conectado ao Wi-Fi):**
   * O dispositivo conecta-se à rede configurada e fica acessível em `http://<ip-do-dispositivo>` ou `http://<nodeId>.local`.
2. **Modo Ponto de Acesso / Captive Portal:**
   * Se não houver rede configurada, o dispositivo cria o AP `EasyIot-XXXXXX` (ou `ONOFRE_XXXXXX`).
   * Password AP: `bhonofre`
   * Aceder a: `http://192.168.4.1`
   * Credenciais por defeito do Web Panel: `admin` / `xpto`

# Executar especificamente para um modelo de hardware isolado:
node scripts/test-playwright/test_bhonofre_hardware.js --mcu=ESP8266      # OnOfre V5
node scripts/test-playwright/test_bhonofre_hardware.js --mcu=ESP8266-HAN  # Contador HAN
node scripts/test-playwright/test_bhonofre_hardware.js --mcu=ESP32        # OnOfre V6
node scripts/test-playwright/test_bhonofre_hardware.js --mcu=ESP32-C6     # OnOfre Rega
```

### Verificações Especializadas por Modelo de Hardware:

1. **`OnOfre V5 ou anterior` (`ESP8266 / ESP12S`)**:
   * **Dual Relay Controls:** Ativação independente de Relé 1 (`GPIO12`) e Relé 2 (`GPIO13`).
   * **Lógica de Interlock de Estores:** Garante que ao ligar o sentido oposto (subida/descida), o relé contrário desliga automaticamente para proteger o motor tubular.
   * **API de Posicionamento:** Validação do slider de abertura/fecho percentual (`/shutter/position?pos=75`).

2. **`Contador HAN` (`ESP8266-HAN`)**:
   * **Protocolo Modbus Master:** Verificação de integridade de frames UART (`GPIO3` RX, `GPIO1` TX, `GPIO14` RTS).
   * **Negociação de Modelo de Contador:** Deteção automática de perfis Kaifa, Landis+Gyr, Sagemcom, Janz e ZIV.
   * **Telemetria de Rede Elétrica:** Potência ativa de importação/exportação (W), tensão monofásica RMS (230V), corrente L1 (A) e energia acumulada (kWh).
   * **Diagrama Tarifário EDP/E-Redes:** Registo em tempo real de tarifas ativas (Vazio, Cheias, Ponta).

3. **`OnOfre V6` (`ESP32-PICO 8MB`)**:
   * **Cargas de Alta Potência:** Comutação dos canais reforçados (`GPIO19` e `GPIO23`).
   * **Medição de Energia em Tempo Real:** Leitura de potência (W), tensão RMS (V), corrente RMS (A) e fator de potência via driver de hardware.
   * **Deteção de Sobrecarga:** Monitorização de limiar de corte de potência de segurança.

4. **`OnOfre Rega` (`ESP32-C6, 5 zonas`)**:
   * **Matriz de 5 Zonas de Rega:** Acionamento independente das eletroválvulas (`GPIO0`, `GPIO2`, `GPIO4`, `GPIO6`, `GPIO8`).
   * **Auto-Engate de Válvula Mestre:** Acionamento automático da válvula mestre de segurança (`GPIO10`) ao abrir qualquer zona de rega.
   * **Sensor de Chuva com Lockout:** Deteção de precipitação (`GPIO18`) e bloqueio automático imediato do circuito hidráulico.
