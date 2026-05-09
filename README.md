# 🏪 Tienda Concurrencia — Simulación de Race Conditions

Proyecto de programacion paralela y concurrente que demuestra vulnerabilidades de **race condition** en una tienda web. Incluye una versión vulnerable (sin protección) y herramientas para explotarla

---
 
## 📋 Requisitos
 
- [Node.js](https://nodejs.org/) v18 o superior
- [Python 3](https://www.python.org/) 3.8 o superior
- pip
Verifica que los tengas instalados:
 
```bash
node --version
python3 --version
```
 
---

---
 
## ⚙️ Instalación
 
### 1. Clona o descarga el proyecto
 
```bash
git clone https://github.com/tu-usuario/tienda-race.git
cd tienda-race
```
 
### 2. Instala dependencias de Node
 
```bash
npm install
```
 
### 3. Instala dependencias de Python
 
```bash
pip install requests
```
 
---
 
## 🚀 Levantar el servidor
 
```bash
node server.js
```
 
Deberías ver:
 
```
[+] Servidor corriendo en: http://127.0.0.1:8000
[!] Deberia haber una race condition activa
```
 
Abre el navegador en [http://127.0.0.1:8000](http://127.0.0.1:8000) para ver la tienda.
 
---
## 💥 Ejecutar el ataque de Race Condition
 
Con el servidor corriendo, abre **otra terminal** y ejecuta:
 
```bash
python3 raceCondition.py
```
