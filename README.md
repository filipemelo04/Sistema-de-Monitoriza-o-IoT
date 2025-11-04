# 🌱 Sistema de Monitorização Inteligente com IoT e Web Dashboard

---

## 📘 Introdução

Este projeto consiste na implementação de um **sistema full-stack de monitorização ambiental** que integra sensores físicos, comunicação IoT, base de dados de séries temporais, API e interface web.  

O sistema foi concebido para **ler dados de sensores (temperatura e humidade)**, transmitir essas informações para um **servidor central (Raspberry Pi)** e **armazená-las em tempo real numa base de dados InfluxDB**. Através de uma **API construída em FastAPI**, os dados são disponibilizados para uma **página web interativa** desenvolvida em **HTML, CSS e JavaScript**, que apresenta as medições em formato de texto e gráficos dinâmicos com *Chart.js*.  

---

## 🧩 Arquitetura do Sistema

O sistema foi desenhado de forma modular e integrada:

- **ESP32:** efetua a leitura dos sensores de temperatura e humidade (DHT22, DS18B20) e envia os dados via **MQTT** para o Raspberry Pi.  
- **Raspberry Pi:** atua como servidor central, recebendo dados, armazenando-os na **InfluxDB** e servindo a **API FastAPI**.  
- **Frontend Web:** permite ao utilizador visualizar os dados e médias diárias/mensais, com navegação interativa e design responsivo.  

---

## ⚙️ Tecnologias Utilizadas

| Componente | Tecnologia / Ferramenta |
|-------------|--------------------------|
| Microcontrolador | ESP32 |
| Servidor | Raspberry Pi |
| Protocolo de Comunicação | MQTT |
| Base de Dados | InfluxDB |
| Linguagem de Backend | Python |
| Framework de API | FastAPI |
| Frontend | HTML, CSS, JavaScript |
| Biblioteca de Gráficos | Chart.js |
| Protocolo Web | HTTP |

---

## 🧠 Funcionalidades Principais

- Leitura e transmissão de dados de sensores em tempo real via MQTT  
- Armazenamento de medições em série temporal na InfluxDB  
- Cálculo automático de médias diárias e mensais  
- Criação de API REST com endpoints GET documentados via Swagger  
- Interface web para visualização interativa de dados e gráficos  

---

## 📂 Estrutura do Projeto
```
📁 Trabalho_LTW/
│
├── 📁 client1/              # Código do ESP32 (Arduino)
├── 📁 FAST-API/             # API desenvolvida em FastAPI (working.py)
├── 📁 ScriptPython/         # Script para ligação MQTT e inserção na InfluxDB
├── 📁 WEB_page/             # Interface Web (HTML, CSS, JS)
    ├── 📁 css/
    ├── 📁 img/
    ├── 📄 app.js
    └── 📄 index.html
```

## 👤 Autor

**Filipe Araújo Melo**  
📧 Email: [melofilipe4@hotmail.com]  
💼 LinkedIn: [linkedin.com/in/teu-perfil](#)
