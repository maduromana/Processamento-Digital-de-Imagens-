# 📦 Detecção de Código de Barras — Trabalho 2 

Este projeto faz parte da disciplina de **Processamento Digital de Imagens** e implementa um algoritmo em **Python** para detectar e localizar um **código de barras** em uma imagem estática, utilizando operações morfológicas e transformadas de linhas.

---

## 🎯 Descrição

O objetivo do trabalho é identificar de forma automática a posição de um código de barras em uma imagem, destacando visualmente o seu contorno. Para isso, o programa:

1. Lê uma imagem que contém um código de barras.
2. Converte a imagem para escala de cinza.
3. Detecta bordas e linhas verticais com a transformada de Hough.
4. Binariza e aplica operações morfológicas (dilatação e erosão) para melhorar a separação dos traços.
5. Localiza o maior contorno (que representa o código de barras).
6. Desenha um retângulo ao redor deste código.
7. Exibe os principais passos do processamento. :contentReference[oaicite:1]{index=1}

---

## 🛠️ Tecnologias Utilizadas

✔️ Linguagem: Python  
✔️ Bibliotecas:  
* `OpenCV` – leitura e processamento de imagens  
* `NumPy` – manipulação de matrizes  
* `Matplotlib` – visualização gráfica :contentReference[oaicite:2]{index=2}

---

## 📁 Conteúdo da Pasta

| Arquivo | Descrição |
|---------|-----------|
| `codigo_de_barras.py` | Código principal com o algoritmo de detecção de código de barras |
| `barcode2.jpg` | Imagem de exemplo utilizada para teste da detecção | :contentReference[oaicite:3]{index=3}

---

## 📦 Pré‑requisitos

Antes de rodar o projeto, instale as dependências:

```bash
pip install opencv-python matplotlib numpy
```
---

## ▶️ Como Executar

1. Certifique‑se de que a imagem barcode2.jpg esteja no mesmo diretório do script.
2. Execute o script Python:
```bash
python codigo_de_barras.py
```
3. O programa abrirá uma janela com um imagens que mostram o processamento passo a passo e destaca o código de barras identificado na imagem.

---

## 📌 O que o Código Faz

O algoritmo segue um pipeline estruturado para garantir a precisão na detecção:

* **Leitura e Conversão para Cinza:** A imagem é carregada e convertida para tons de cinza, o que reduz a complexidade dos dados e facilita as operações subsequentes de detecção de bordas.
* **Detecção de Bordas e Linhas:** Através da combinação do algoritmo **Canny** com a **Transformada de Hough Probabilística (HoughLinesP)**, as linhas verticais da imagem são realçadas para identificar a estrutura característica das barras.
* **Operações Morfológicas:** Aplicam-se técnicas de **dilatação** e **erosão**. Essas operações servem para unir os traços verticais próximos e reforçar a massa de pixels, eliminando pequenos ruídos antes de localizar o contorno principal.
* **Extração do Maior Contorno:** O algoritmo identifica todos os contornos da imagem processada. O **maior contorno** é filtrado e considerado como a região que contém o código de barras, sendo então desenhado um retângulo verde ao redor dele na imagem original.

---

## 📸 Visualização

Ao executar o script, o programa gera uma interface gráfica que exibe o progresso do processamento em cinco etapas principais:

1. **Imagem Original:** A entrada bruta sem modificações.
2. **Linhas Verticais Detectadas:** O mapa de bordas focado na estrutura do código.
3. **Após Dilatação:** O preenchimento dos espaços entre as barras.
4. **Após Erosão:** O refinamento da área de interesse.
5. **Resultado Final:** A imagem original com o retângulo destacando o código identificado com sucesso.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **OpenCV:** Para manipulação de imagens e visão computacional.
* **Matplotlib:** Para a exibição dos resultados e etapas do processo.
* **NumPy:** Para operações matemáticas e matriciais.

---

## ✨ Autor

**Maria Eduarda S. Romana** — RA: 2408830  
*Trabalho desenvolvido para a disciplina de Processamento Digital de Imagens — Engenharia de Computação.*
