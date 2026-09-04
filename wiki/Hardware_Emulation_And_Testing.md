# 🚀 Emulação de Hardware e Testes com Renode

O EasyIot suporta **emulação real de hardware** e **simulação interativa de interface web**, permitindo desenvolver, compilar e testar código sem necessidade de placas físicas ESP32 ou ESP8266 conectadas.

---

## 1. 🌐 Emulação de Hardware com Renode (Open-Source)

[Renode](https://renode.io/) é uma framework open-source de emulação de processadores e periféricos (desenvolvida pela Antmicro). Ao contrário de simuladores de alto nível, o Renode executa as **instruções de máquina reais do firmware compilado (.elf)** nos núcleos virtuais Xtensa do ESP32.

### Ficheiros de Configuração:
* **[`emulation/platforms/easyiot_esp32.repl`](file:///c:/Users/bruno/CLionProjects/EasyIot/emulation/platforms/easyiot_esp32.repl):** Descreve o mapeamento de periféricos do EasyIot (relés em GPIO 12 e 14, válvulas de fonte em GPIO 27, 26, 25, 33 e consola UART).
* **[`emulation/easyiot_esp32.resc`](file:///c:/Users/bruno/CLionProjects/EasyIot/emulation/easyiot_esp32.resc):** Script de execução que cria a máquina virtual ESP32, carrega o binário PlatformIO `.pio/build/ESP32_DEBUG/firmware.elf` e abre a consola de monitorização série.
* **[`emulation/tests/easyiot_boot.robot`](file:///c:/Users/bruno/CLionProjects/EasyIot/emulation/tests/easyiot_boot.robot):** Teste automatizado em Robot Framework para validação contínua em CI/CD.

### Instalação Automática do Renode:
O EasyIot inclui scripts de instalação automatizada para todas as plataformas:

* **Windows (PowerShell):**
  ```powershell
  .\install_renode.ps1
  # Ou via winget diretamente:
  winget install Renode.Renode
  ```
* **Linux (Ubuntu / Debian / Fedora / Arch):**
  ```bash
  chmod +x install_renode.sh
  ./install_renode.sh
  ```
* **macOS (Homebrew):**
  ```bash
  ./install_renode.sh
  # Ou via brew diretamente:
  brew install --cask renode
  ```

### Como Executar Localmente:
```powershell
# Compilar e iniciar no emulador Renode com consola série interativa
.\.venv\Scripts\python tools/run_renode.py --build

# Executar testes automatizados sem interface gráfica
.\.venv\Scripts\python tools/run_renode.py --test
```

---

## 2. 🖥️ Simulador Web Interativo (Python Mock Server)

Para desenvolvimento rápido de interfaces web, painéis de controlo e testes do AquaDance:

```powershell
.\.venv\Scripts\python tools/esp_simulator.py
```

* Abre um servidor local em **`http://localhost:8080`**.
* Serve a interface `webpanel/` real e emula todos os endpoints REST (`/config`, `/state`, `/aquadance`, `/control`) e Server-Sent Events (SSE).
* Permite compor partituras musicais e testar o **Simulador 2D do Lago** sem tempos de compilação C++.

---

## 3. 🤖 Integração Contínua em GitHub Actions (CI)

O workflow de CI ([`.github/workflows/ci.yml`](file:///c:/Users/bruno/CLionProjects/EasyIot/.github/workflows/ci.yml)) executa automaticamente:

1. **Validação de Sintaxe:** Verificação de scripts Python e código JavaScript.
2. **Minificação de Assets Web:** Compilação do painel web para ficheiros PROGMEM (`include/IndexHtml.h`, etc.).
3. **Compilação Cruzada:** `pio run -e ESP8266_DEBUG` e `pio run -e ESP32_DEBUG`.
4. **Testes Unitários:** Execução de testes de contrato e regras de negócio.
5. **Emulação de Hardware Renode:** `antmicro/renode-test-action@v5` testa o arranque do firmware na máquina virtual ESP32.

---

## 4. 🎭 Testes E2E de Hardware & Portal Web com Playwright

O EasyIot e o ecossistema BHonofre contam com uma suite de testes End-to-End (E2E) com **Playwright** para validar o portal de gravação web ([CloudIO Flasher](https://cloudio.bhonofre.pt/flash/)) e os fluxos de firmware para todos os 4 modelos de hardware oficiais.

### Ficheiro de Teste:
* **`scripts/test-playwright/test_bhonofre_hardware.js`**

### Modos de Execução:

#### **Modo A: Simulação Local / Pipeline CI (Default)**
Inicia um servidor mock interno na porta `8989` que espelha as APIs do portal CloudIO (`/firmware/all-versions/:mcu` e `/firmware/webflash/:mcu/manifest.json`):
```powershell
# Execução direta com Node.js
node scripts/test-playwright/test_bhonofre_hardware.js

# Ou via npm:
cd scripts/test-playwright
npm run test:bhonofre
```

#### **Modo B: Validação com Dispositivo Físico / IP Local**
Permite apontar os testes para um módulo BHonofre em execução na rede local:
```powershell
# Windows (PowerShell)
$env:BHONOFRE_URL="http://192.168.1.185"; node scripts/test-playwright/test_bhonofre_hardware.js

# Linux / macOS (Bash)
BHONOFRE_URL="http://192.168.1.185" node scripts/test-playwright/test_bhonofre_hardware.js
```

#### **Modo C: Validação contra o Portal CloudIO em Produção**
Executa os testes diretamente contra o portal oficial `https://cloudio.bhonofre.pt/flash/`:
```powershell
# Windows (PowerShell)
$env:BHONOFRE_URL="https://cloudio.bhonofre.pt/flash/"; node scripts/test-playwright/test_bhonofre_hardware.js

# Linux / macOS (Bash)
BHONOFRE_URL="https://cloudio.bhonofre.pt/flash/" node scripts/test-playwright/test_bhonofre_hardware.js
```

#### **Modo D: Emulador de Hardware Interativo & Suites Específicas por MCU**
Inicia e valida um emulador interativo do dispositivo OnOfre / EasyIot (porta `8080`), executando verificações especializadas para cada arquitetura de hardware:
```powershell
# Executar a suite completa para todas as 4 arquiteturas de hardware:
node scripts/test-playwright/test_bhonofre_hardware.js --emulator

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
