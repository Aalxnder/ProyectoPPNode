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
git clone https://github.com/Aalxnder/ProyectoPPNode.git
cd ProyectoPPNode
```
 
### 2. Instala dependencias de Node
 
```bash
npm install
npm install express
npm install nunjucks
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
python3 raceConditionNode.py
```

O puedes ir a la carpeta scripts

```bash
cd scripts
```

veras dos tipos de archivos con extension `.sh`

dales permiso de ejecucion 

```bash
chmod +x execute_linux.sh
chmod +x multiple_thread.sh
```
y con esto se levantara solo el servidor, se lanzara el script y se mostrara la version con y sin proteccion 
contra race condition, solo que aqui al final el server se apaga, si quieres ver la pagina corriendo, hazlo de 
la primer manera


## Habilitar o desactivar proteccion 

Primero abre el archivo `server.js` que deberia estar en la carpeta raiz 

```bash
nvim server.js
```

y donde veas algo como 

```js
const USE_LOCKS = process.argv[process.argv.length - 1]
    ? parseInt(process.argv[process.argv.length - 1])
    : false;
```

solo cambia false por true y guarda y vuelve a levantar el server

## Modo de ataque secuencial o Hilos

para esto igual en la raiz veras un archivo llamado `raceConditionNode.py`
abrelo igual que el archivo del server y donde veas algo como 

```python
USAR_HILOS = True
```

ponle False y deberias estar usando el modo secuencial, aunque es probable que no se den las race condition de este modo
