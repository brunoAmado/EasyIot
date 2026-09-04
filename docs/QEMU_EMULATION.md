# 🌐 Espressif QEMU ESP32 Emulation & Virtual Networking

O EasyIot suporta emulação completa de binários ESP32 com rede virtual usando o **Espressif QEMU (`qemu-system-xtensa`)**. Ao contrário do Renode (focado em ciclo de CPU e GPIOs), o QEMU da Espressif inclui uma placa de rede virtual **OpenETH (OpenCores Ethernet MAC)** e encaminhamento de portas TCP para o sistema operativo anfitrião.

---

## 1. 🚀 Como Funciona a Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│  Host OS (Browser do seu Computador)                       │
│  http://localhost:8080                                      │
└──────────────────────────────┬──────────────────────────────┘
                               │ Encaminhamento de Portas (8080 -> 80)
┌──────────────────────────────▼──────────────────────────────┐
│  Espressif QEMU (qemu-system-xtensa)                        │
│  - Máquina Virtual: ESP32 (Xtensa LX6 Dual-Core 240MHz)     │
│  - Placa de Rede Virtual: OpenETH (OpenCores Ethernet)      │
│  - Rede do Emulador: Pilha Slirp User-Mode (DHCP/DNS)       │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│  Firmware EasyIot compilado (qemu_flash.bin)               │
│  - Pilha TCP/IP LwIP                                        │
│  - ESPAsyncWebServer escutando no porto 80                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 📦 Instalação do Espressif QEMU

O repositório inclui um instalador automatizado para todas as plataformas:

### Windows (PowerShell):
```powershell
.\install_qemu.ps1
# Ou diretamente:
py -3.11 tools/install_qemu.py
```

### Linux / macOS:
```bash
chmod +x install_qemu.sh
./install_qemu.sh
```

---

## 3. ⚙️ Como Executar a Emulação

### A. Comando Rápido (Compilação + Junção de Flash + QEMU)
```powershell
py -3.11 tools/run_qemu.py --build
```

### B. Opções Disponíveis no Runner:
```text
--env ENV       Ambiente PlatformIO a compilar (por defeito: ESP32_DEBUG)
--port PORT     Porta HTTP no computador anfitrião (por defeito: 8080)
--build         Força a recompilação do firmware antes de iniciar
--install       Descarrega e instala o QEMU automaticamente se não estiver presente
```

---

## 4. 🌐 Aceder ao Web Panel no Navegador

Após o arranque do QEMU e inicialização do servidor web do firmware, abra o navegador:

👉 **[http://localhost:8080](http://localhost:8080)**

---

## 5. ⌨️ Controlos do Terminal QEMU

* **Sair do QEMU:** Pressione `Ctrl + A` e depois `X`.
* **Ajuda do Monitor QEMU:** Pressione `Ctrl + A` e depois `C`.
