# 🎬 YouTube Gesture Control

**Controle o YouTube usando apenas gestos das mãos através da sua webcam! 🖐️**

[![Licença MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.10.0+-red.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.21+-yellow.svg)](https://mediapipe.dev/)

---

## 📋 Sobre o Projeto

**YouTube Gesture Control** é um sistema de visão computacional que permite controlar a reprodução de vídeos do YouTube através de gestos manuais detectados pela webcam. O projeto utiliza **OpenCV** para captura de vídeo, **MediaPipe** para rastreamento preciso das mãos e **PyAutoGUI** para enviar comandos de teclado ao navegador.

O sistema foi otimizado para oferecer **detecção precisa** e **experiência fluida** com um cooldown de 2 segundos entre comandos, evitando execuções acidentais.

---

## ✨ Funcionalidades

| Gesto | Ação no YouTube | Tecla |
|-------|----------------|-------|
| ✊ **Punho fechado** | Play / Pausa | `K` |
| 🖐️ **Mão aberta** | Tela cheia | `F` |
| 👍 **Polegar para cima** | Aumentar volume | `↑` |
| 👎 **Polegar para baixo** | Diminuir volume | `↓` |
| 🤏 **Pinça (polegar + indicador)** | Ativar/desativar legendas | `C` |
| ✌️ **Paz (V)** | Mutar / Desmutar | `M` |

### 🎥 Feedback Visual em Tempo Real

- **Gesto detectado** exibido na tela com ícone e nome
- **Indicador de cooldown** mostrando o tempo restante para próximo comando
- **Status do sistema** ("Pronto para comando" / "Aguarde cooldown")
- **Desenho dos 21 pontos da mão** com conexões
- **Status de detecção** (mão detectada/não detectada)


### ⚡ Melhorias de Estabilidade

- **Cooldown de 2 segundos** entre comandos para evitar execuções acidentais
- **Suavização de detecção** com filtro de consistência
- **Thresholds ajustados** para melhor precisão na detecção de gestos
- **Verificação de ângulo** para thumbs up/down (mais preciso)
- **Prevenção de spam** com verificação de comandos duplicados
- **Tratamento de erros** robusto para webcam e processamento

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

---

## 📁 Estrutura do Projeto
YoutubeGestureControl/
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
   git clone https://github.com/Crively/YoutubeGestureControl.git
   cd YoutubeGestureControl
2. **Crie um Ambiente Virtual**
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

## Como Utilizar
1. **Abra o YouTube no seu navegador e inicie um vídeo**

2. **Execute python main.py**

3. **Certifique-se de que a janela do navegador está em foco (clique nela)**

4. **Faça os gestos na frente da webcam**

5. **Aguarde o indicador de cooldown (2 segundos) entre comandos**

6. **Pressione q para sair do programa**

## 🎯 Dicas para Melhor Precisão
- Iluminação adequada: Certifique-se de ter boa iluminação no ambiente

- Fundo simples: Fundo com poucas texturas melhora a detecção

- Distância correta: Mantenha a mão entre 30-50cm da webcam

- Movimentos lentos: Faça gestos de forma clara e pausada

- Mão visível: Mantenha toda a mão visível dentro do frame

#🤝 Contribuindo
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

1. Faça um fork do projeto

2. Crie sua branch de feature (git checkout -b feature/nova-funcionalidade)

3. Commit suas mudanças (git commit -m 'Adiciona nova funcionalidade')

4. Push para a branch (git push origin feature/nova-funcionalidade)

5. Abra um Pull Request

#📄 Licença
Distribuído sob a licença MIT. Veja LICENSE para mais informações.

# ✉️ Contato
- Crively - GitHub
- Felipe Crivelli - Linkedin

Link do Projeto: https://github.com/Crively/YoutubeGestureControl
