# ⛲ AquaDance & Fonte Musical (Fontaine Mod)

O modo **AquaDance (Fonte Musical)** transforma as válvulas de rega e focos de iluminação do EasyIot num sistema avançado de coreografia aquática sincronizada (*Son et Lumière* / Águas Dançantes), controlado graficamente através de uma matriz de partição musical e um simulador 2D do lago.

---

## 🎼 1. Matriz de Partição Musical (Piano Roll)

A interface na aba **REGA ➔ FONTE AQUADANCE** apresenta uma matriz gráfica inspirada em estações de trabalho de áudio digital (DAW / Piano Roll):

* **Linhas (Eixo Y):** Cada linha representa uma válvula de água (`GARDEN_VALVE`), foco de luz dimmer (`LIGHT_DIMMER`) ou iluminação colorida RGBW.
* **Colunas (Eixo X):** Passos temporais configuráveis (16, 24, 32, 48 ou 64 passos) organizados em **compassos de 4 tempos** (ex: `1.1`, `2.1`, `3.1`, etc.).
* **Desenho Interativo:** Clique ou arraste com o rato ou toque no telemóvel para "pintar" notas onde a água é disparada e as luzes se acendem.
* **Tempo Ajustável:** Duração por passo de 100 ms (muito rápido) a 1000 ms (lento).
* **Loop Contínuo:** Opção de repetição contínua para espetáculos permanentes de fontes.

---

## 💡 2. Controlo de Iluminação, Potência e Cores RGBW

Ao contrário de sistemas convencionais que apenas abrem e fecham água, o AquaDance integra controlo dinâmico de iluminação:

* **Válvulas de Água (⛲):** Notas binárias de abertura e fecho de jatos de água com animação de spray e ondas de impacto.
* **Dimmer e Potência de Luz (💡):** Clique nas notas de dimmer para ajustar a intensidade de iluminação (`25%`, `50%`, `75%`, `100%`).
* **Paleta de Cores RGBW (🎨):** Seletor interativo com amostras de cores (*Ciano, Azul Profundo, Esmeralda, Âmbar, Laranja, Vermelho Fogo, Magenta, Roxo, Branco Quente e Branco Frio*). Ao pintar notas na faixa RGBW, a célula brilha na cor selecionada.

---

## 🌊 3. Simulador 2D do Lago / Piscina

Acima da matriz de partição encontra-se o **Simulador 2D em Tempo Real**:

* **Mapeamento de Coordenadas (X, Y):** Cada bico de água e projetor de luz pode ser arrastado pelo lago para corresponder à disposição física real da sua piscina ou fonte.
* **Disposições Geométricas Rápidas:**
  - **Círculo (Ring):** Distribuição radial simétrica de jatos.
  - **Linha Reta (Linear):** Alinhamento horizontal de cortina de água.
  - **Cruz Dupla (Cross):** Padrão cruzado concêntrico.
  - **Arco (Arc):** Curva parabólica decorativa.
* **Física e Animação ao Vivo:**
  - Durante a reprodução, o cursor percorre a partição e o simulador 2D dispara partículas de água com ondulação física e halos luminosos na cor exata de cada foco.

---

## 🏠 4. Integração com Home Assistant

### Descoberta Automática MQTT
O EasyIot publica automaticamente no Home Assistant:
* `binary_sensor.<chipId>_aquadance_running` (Indica se uma coreografia está a decorrer).
* `button.<chipId>_aquadance_stop` (Paragem de emergência de todas as válvulas).
* `button.<chipId>_aquadance_show_<id>` (Disparo direto de cada coreografia gravada).

### Cartão 2D Lovelace (Picture-Elements)
Na interface web, o botão **"Copiar Cartão Home Assistant (2D)"** gera o código YAML pronto a colar no painel Lovelace do Home Assistant com as coordenadas percentuais `(top, left)` exatas de cada bico de água e luz.

---

## 📡 5. Endpoints REST da API

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/aquadance` | Obtém todas as coreografias e estado de reprodução em tempo real. |
| `POST` | `/aquadance` | Valida e grava a lista de coreografias no sistema de ficheiros LittleFS (`/aquadance.json`). |
| `POST` | `/aquadance/run` / `/aquadance-run` | Inicia a reprodução da coreografia indicada no corpo JSON `{"showId": 1}`. |
| `POST` | `/aquadance/stop` / `/aquadance-stop` | Interrompe a reprodução e fecha todas as válvulas imediatamente. |
