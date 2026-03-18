# 🌊 Analisador de Nível de Barragem - PDI

Este projeto faz parte da disciplina de **Processamento Digital de Imagens** e implementa uma interface gráfica em Python para analisar vídeos de uma barragem, medindo a altura da água ao longo do tempo com base em segmentação por cor e seleção de pontos.

---

## 🎯 Descrição

O objetivo principal é permitir que o usuário realize o monitoramento hídrico de forma semimanual e automatizada, seguindo o fluxo:

1. **Carregamento:** Importação de um vídeo da barragem.
2. **Definição de ROI:** Seleção da Área de Interesse (*Region of Interest*).
3. **Calibração:** Conversão de pixels em centímetros através de uma referência real.
4. **Análise Multi-ponto:** Escolha de múltiplos pontos de análise vertical.
5. **Processamento:** Detecção da linha d'água frame a frame via segmentação por cor no espaço **HSV**.
6. **Visualização:** Geração de um vídeo com marcações e um gráfico da variação de altura da água ao longo do tempo.

O programa foi desenvolvido em **Python**, utilizando bibliotecas como `tkinter` (Interface Gráfica), `OpenCV` (Processamento de Vídeo) e `Matplotlib` (Geração de Gráficos).

---

## 🛠️ Funcionalidades

* ✔️ Interface gráfica intuitiva para carregar e configurar a análise.
* ✔️ Seleção dinâmica de área de análise (ROI).
* ✔️ Calibração de escala (conversão de pixels para centímetros).
* ✔️ Seleção de múltiplos pontos de interesse (mínimo 4) ao longo da largura.
* ✔️ Processamento de vídeo com filtro por cor (Espaço HSV).
* ✔️ Geração automática de gráfico de altura da água vs. tempo.
* ✔️ Exportação de vídeo processado com marcações de pontos e alturas detectadas.

---

## 📦 Pré-requisitos

Antes de rodar o projeto, certifique-se de ter o **Python 3.8** ou superior instalado e as seguintes dependências:

```bash
pip install opencv-python pillow matplotlib numpy
```
---
## 🚀 Como Rodar

Siga os comandos abaixo no seu terminal para configurar e executar o projeto:

```bash
# 1. Clone o repositório
git clone [https://github.com/maduromana/Processamento-Digital-de-Imagens-.git](https://github.com/maduromana/Processamento-Digital-de-Imagens-.git)

# 2. Entre na pasta do trabalho
cd "Processamento-Digital-de-Imagens-/trabalho1 - analise de barragem"

# 3. Instale as bibliotecas necessárias
pip install opencv-python pillow matplotlib numpy

# 4. Execute o analisador
python analise_barragem.py
```

### 📝 Passo a Passo na Interface

Para realizar a análise corretamente, siga estas etapas dentro do software:

1. **Passo 1:** Clique em **Abrir vídeo** e selecione o arquivo `.mp4`.
2. **Passo 2:** Selecione a área de análise (**ROI**) na janela pop-up que será aberta.
3. **Passo 3:** Insira a **altura conhecida** (em cm) para calibrar a escala de pixels para unidades reais.
4. **Passo 4:** Selecione no mínimo **4 linhas de análise** vertical sobre a imagem da barragem.
5. **Passo 5:** Clique em **Processar** e aguarde a geração automática das saídas (vídeo e gráfico).

---

### 📁 Conteúdo da Pasta

| Arquivo | Descrição |
| :--- | :--- |
| `analise_barragem.py` | Código principal do analisador com interface gráfica (GUI). |
| `video_barragem.mp4` | Exemplo de vídeo para teste de detecção. |

---

### 🧠 Como Funciona

O núcleo do processamento segue esta lógica algorítmica baseada em Visão Computacional:

* **Filtro HSV:** O frame é convertido para o espaço de cor HSV para isolar a tonalidade da água, ignorando reflexos e variações de iluminação que costumam atrapalhar no espaço RGB.
* **Varredura Vertical:** Para cada linha selecionada, o algoritmo busca o primeiro pixel que satisfaz o critério de cor (máscara) da água.
* **Cálculo de Altura:** A posição do pixel detectado é convertida em centímetros baseando-se na constante de calibração definida no início.
* **Análise Temporal:** Os dados de cada frame são compilados para gerar o gráfico final de variação de nível ao longo do tempo.

---



### ✨ Autor

**Maria Eduarda S. Romana** 
*Trabalho desenvolvido para a disciplina de Processamento Digital de Imagens — Engenharia de Computação.*


