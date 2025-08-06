# 🚀 LLM-Powered Projectile Simulator

A smart, interactive projectile motion simulator that combines physics, numerical computation, and local language models using [Ollama](https://ollama.com/) and [Streamlit](https://streamlit.io/).

Enter real-world scenarios in plain English (e.g. _"Launch a ball at 50 m/s from 2 meters at 45 degrees with 0.1 drag"_), and the app will:
- Extract parameters using a local LLM
- Simulate motion (with or without air resistance)
- Plot the projectile trajectory
- Compute time of flight, range, and max height

---

## 🖼️ Demo

<img width="975" height="420" alt="image" src="https://github.com/user-attachments/assets/6a5d1ef9-67e4-4e58-a93b-80a9e88410c7" />
<img width="975" height="467" alt="image" src="https://github.com/user-attachments/assets/242b093a-7ed3-4d10-a807-a54ee3d97f0a" />


---

## 🧠 How It Works

1. **User enters a natural language scenario**
2. **Ollama LLM** (e.g. `llama3` or `mistral`) parses the input into structured parameters
3. **Physics engine** (NumPy + SciPy) simulates the projectile's path
4. **Matplotlib** visualizes the results in a Streamlit web app

---

## 🔧 Features

- 🧠 Natural language input powered by LLM (Ollama)
- 📈 Visual trajectory plotting with `matplotlib`
- 🌍 Supports air resistance (drag coefficient)
- 📐 Calculates time of flight, max height, and range
- 💻 Runs 100% locally (no internet required)

---

## 📦 Requirements

Install Python 3.8+ and then run:

```bash
pip install streamlit numpy matplotlib scipy

