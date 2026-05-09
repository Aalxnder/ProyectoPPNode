const express = require('express');
const nunjucks = require('nunjucks');
const app = express();

nunjucks.configure('views', {
    autoescape: true,
    express: app
});

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static('public'));

// Datos estaticosa para no usar base de datos 
 let USUARIO = { nombre: "Levi", saldo: 10000 };

let PRODUCTOS = [
    { id: 1, nombre: "Rines Honda",     precio: 5000, stock: 10, descripcion: "Medida 225/60/r17", imagen: "honda.jpeg" },
    { id: 2, nombre: "Rines Chevrolet", precio: 4500, stock: 8,  descripcion: "Medida 295/50/r15", imagen: "chevy.jpeg" },
    { id: 3, nombre: "Rines Dodge",     precio: 6000, stock: 5,  descripcion: "Medida 275/40/r20", imagen: "dodge.jpeg" },
];

// Rutas
app.get('/', (req, res) => {
    res.render('index.html', { productos: PRODUCTOS, usuario: USUARIO });
});

app.get('/saldo', (req, res) => {
    res.render('saldo.html', { usuario: USUARIO });
});

app.get('/estado', (req, res) => {
    res.json({ usuario: USUARIO, productos: PRODUCTOS });
});

// Aqui es donde ocurre la race condition, al querer comprar
app.get('/buy/:id', async (req, res) => {
    const producto = PRODUCTOS.find(p => p.id === parseInt(req.params.id));

    if (!producto) {
        return res.status(404).send("Producto no encontrado");
    }
    // leer valores de usuario y producto
    const saldoLeido  = USUARIO.saldo;
    const stockLeido  = producto.stock;

    // meter un sleep para que al lanzar muchos hilos todas las peticiones vean lo mismo antes que se actualice y se rompa
    await sleep(150);       
  
    if (saldoLeido >= producto.precio && stockLeido > 0) {

        await sleep(50);
        // ya van a estar mal los datos pq ya muchas peticiones leyeron los datos mal y por eso, se confunde        
        USUARIO.saldo  -= producto.precio;
        producto.stock -= 1;

        res.render('buy.html', {
            mensaje: `[+] Compra realizada: ${producto.nombre} por $${producto.precio}`,
            producto,
            usuario: USUARIO
        });
    } else {
        res.render('buy.html', {
            mensaje: `[!] Sin saldo suficiente o producto agotado`,
            producto,
            usuario: USUARIO
        });
    }
});

// Un race condition para añadir saldo(no lo vi como relevante y lo quite, pero aqui esta por si acaso) 
// // app.post('/anadir_saldo', async (req, res) => {
//     const cantidad = parseInt(req.body.cantidad) || 0;
//     const tarjeta  = req.body.tarjeta || "";
//     await sleep(5);
//     USUARIO.saldo += cantidad;
//     res.render('anadir_saldo.html', {
//         usuario: USUARIO,
//         mensaje: `[+] Se añadieron $${cantidad} con tarjeta terminada en ${tarjeta.slice(-4)}`
//     });
// });

// Resetear para poder hacer pruebas
app.post('/reset', (req, res) => {
    USUARIO.saldo = 10000;
    PRODUCTOS[0].stock = 10;
    PRODUCTOS[1].stock = 8;
    PRODUCTOS[2].stock = 5;
    res.json({ ok: true, mensaje: "Estado reseteado" });
});

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

app.listen(8000, () => {
    console.log('[+]Servidor corriendo en: http://127.0.0.1:8000');
    console.log('[!] Deberia haber una race condition activa');
});
