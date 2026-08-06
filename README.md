# 🎬 YouTube Gesture Control

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/OpenCV-4.10.0-brightgreen.svg" alt="OpenCV">
  <img src="https://img.shields.io/badge/MediaPipe-0.10.21-ff69b4.svg" alt="MediaPipe">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</p>

<p align="center">
  <strong>Controle o YouTube usando apenas gestos das mãos através da sua webcam! 🖐️</strong>
</p>

---

## 📋 Sobre o Projeto

**YouTube Gesture Control** é um sistema de visão computacional que permite controlar a reprodução de vídeos do YouTube através de gestos manuais detectados pela webcam. O projeto utiliza **OpenCV** para captura de vídeo, **MediaPipe** para rastreamento preciso das mãos e **PyAutoGUI** para enviar comandos de teclado ao navegador.

## ✨ Funcionalidades

| Gesto | Ação no YouTube | Tecla |
|-------|----------------|-------|
| ✊ **Punho fechado** | Play / Pausa | `K` |
| 👉 **Deslizar para direita** | Avançar 5 segundos | `L` |
| 👈 **Deslizar para esquerda** | Voltar 5 segundos | `J` |
| 👍 **Polegar para cima** | Aumentar volume | `↑` |
| 👎 **Polegar para baixo** | Diminuir volume | `↓` |
| 🖐️ **Mão aberta** | Tela cheia | `F` |
| 🤏 **Pinça (polegar + indicador)** | Ativar/desativar legendas | `C` |
| ✌️ **Paz (V)** | Mutar / Desmutar | `M` |

### 🎥 Feedback Visual

- O gesto detectado é exibido em tempo real na tela
- Indicador de **cooldown** para evitar comandos acidentais
- Desenho dos 21 pontos da mão com conexões

---

## 🛠️ Tecnologias Utilizadas

### Linguagem
- **Python 3.8+**

### Bibliotecas e APIs
| Biblioteca | Versão | Finalidade |
|------------|--------|------------|
| **OpenCV** | 4.10.0+ | Captura da webcam e processamento de vídeo |
| **MediaPipe** | 0.10.21+ | Rastreamento da mão e detecção de landmarks |
| **NumPy** | 1.24.0+ | Cálculos matemáticos e manipulação de arrays |
| **PyAutoGUI** | 0.9.54+ | Simulação de teclas para controlar o YouTube |
| **Keyboard** | 0.13.5+ | Detecção de teclas (opcional) |

---

## 📁 Estrutura do Projeto
youtube_gesture_control/
│
├── main.py # Loop principal da aplicação
├── hand_tracker.py # Detecção e rastreamento da mão
├── gesture_detector.py # Reconhecimento e classificação dos gestos
├── gesture_controller.py # Mapeamento gesto → comando com cooldown
├── youtube_controller.py # Envio dos comandos para o YouTube
├── requirements.txt # Dependências do projeto
├── README.md # Este arquivo
└── LICENSE # Licença MIT


---

## 🚀 Como Usar

### Pré-requisitos

- Python 3.8 ou superior
- Webcam funcionando
- Navegador com YouTube aberto

### Instalação

1. **Clone o repositório**
     ```bash
        git clone https://github.com/seu-usuario/youtube-gesture-control.git
        cd youtube-gesture-control
2. **Crie um ambiente virtual (recomendado)**
     ```bash
         python -m venv venv
         source venv/bin/activate  # Linux/Mac
         venv\Scripts\activate     # Windows
3. **Instale as dependências**
    ```bash
         pip install -r requirements.txt
4. **Execute o programa**
    ```bash
         python main.py
### Como Utilizar
1. Abra o YouTube no seu navegador e inicie um vídeo

2. Execute python main.py

3. Certifique-se de que a janela do navegador está em foco (clique nela)

4. Faça os gestos na frente da webcam

5. Pressione q para sair do programa
         
