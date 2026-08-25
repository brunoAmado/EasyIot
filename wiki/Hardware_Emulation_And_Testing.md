# 🚀 Emulação de Hardware e Testes com Renode

O EasyIot suporta **emulação real de hardware** e **simulação interativa de interface web**, permitindo desenvolver, compilar e testar código sem necessidade de placas físicas ESP32 ou ESP8266 conectadas.

---

## 1. 🌐 Emulação de Hardware com Renode (Open-Source)

[Renode](https://renode.io/) é uma framework open-source de emulação de processadores e periféricos (desenvolvida pela Antmicro). Ao contrário de simuladores de alto nível, o Renode executa as **instruções de máquina reais do firmware compilado (.elf)** nos núcleos virtuais Xtensa do ESP32.

### Ficheiros de Configuração:
* **[`renode/platforms/easyiot_esp32.repl`](file:///c:/Users/bruno/CLionProjects/EasyIot/renode/platforms/easyiot_esp32.repl):** Descreve o mapeamento de periféricos do EasyIot (relés em GPIO 12 e 14, válvulas de fonte em GPIO 27, 26, 25, 33 e consola UART).
* **[`renode/easyiot_esp32.resc`](file:///c:/Users/bruno/CLionProjects/EasyIot/renode/easyiot_esp32.resc):** Script de execução que cria a máquina virtual ESP32, carrega o binário PlatformIO `.pio/build/ESP32_DEBUG/firmware.elf` e abre a consola de monitorização série.
* **[`renode/tests/easyiot_boot.robot`](file:///c:/Users/bruno/CLionProjects/EasyIot/renode/tests/easyiot_boot.robot):** Teste automatizado em Robot Framework para validação contínua em CI/CD.

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
5. **Emulação de Hardware Renode:** `antmicro/renode-test-action@v1` testa o arranque do firmware na máquina virtual ESP32.
