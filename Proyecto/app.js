const URL_API = 'https://jsonplaceholder.typicode.com/todos?_limit=5';
let inventario = JSON.parse(localStorage.getItem('mis_datos')) || [];
let idEdicion = null;

const rejilla = document.getElementById('itemsGrid');
const formulario = document.getElementById('itemForm');
const cajaBusqueda = document.getElementById('busqueda');


async function cargarDatosIniciales() {
    if (inventario.length === 0) {
        try {
            document.getElementById('loader').classList.remove('hidden');
            const respuesta = await fetch(URL_API);
            if (!respuesta.ok) throw new Error('Error al conectar');
            const datosBrutos = await respuesta.json();
            
            inventario = datosBrutos.map(tarea => ({
                id: Date.now() + Math.random(),
                titulo: tarea.title,
                descripcion: "Importado de la nube",
                categoria: "General",
                estado: tarea.completed ? 'completado' : 'pendiente',
                fecha: "2024-01-01"
            }));
            guardarYRefrescar();
        } catch (error) {
            document.getElementById('loader').classList.remove('hidden');

            console.error("Hubo un fallo en la red:", error);
        }
    } else {
        document.getElementById('loader').classList.remove('hidden');
        dibujarInventario();
    }
}

formulario.addEventListener('submit', (evento) => {
    evento.preventDefault();
    
    const nuevoElemento = {
        id: idEdicion ? idEdicion : Date.now(),
        titulo: document.getElementById('titulo').value,
        descripcion: document.getElementById('descripcion').value,
        categoria: document.getElementById('categoria').value,
        estado: 'pendiente',
        fecha: document.getElementById('fecha').value
    };

    if (nuevoElemento.titulo.length < 3) {
        alert("El título es muy corto");
        return;
    }

    if (idEdicion) {
        inventario = inventario.map(el => el.id === idEdicion ? nuevoElemento : el);
        idEdicion = null;
        document.getElementById('submitBtn').textContent = "Guardar";
    } else {
        inventario.push(nuevoElemento);
    }

    formulario.reset();
    guardarYRefrescar();
});

function dibujarInventario() {
    rejilla.innerHTML = '';
    
    const textoBuscado = cajaBusqueda.value.toLowerCase();
    const filtro = document.getElementById('filtroEstado').value;

    const listaFiltrada = inventario.filter(item => {
        const coincideTexto = item.titulo.toLowerCase().includes(textoBuscado);
        const coincideEstado = filtro === 'todos' || item.estado === filtro;
        return coincideTexto && coincideEstado;
    });

    listaFiltrada.forEach(item => {
        const tarjeta = document.createElement('div');
        tarjeta.className = `tarjeta ${item.estado}`;
        tarjeta.innerHTML = `
            <h3 >${item.titulo}</h3>
            <p>${item.descripcion}</p>
            <div class="botones">
                <button onclick="cambiarEstado(${item.id})">✔️</button>
                <button onclick="prepararEdicion(${item.id})">✏️</button>
                <button onclick="borrarElemento(${item.id})">🗑️</button>
            </div>
        `;
        rejilla.appendChild(tarjeta);
    });
    
    actualizarContador();
}

function guardarYRefrescar() {
    localStorage.setItem('mis_datos', JSON.stringify(inventario));
    dibujarInventario();
}

window.borrarElemento = (id) => {
    if (confirm('¿Quieres borrar este elemento?')) {
        inventario = inventario.filter(el => el.id !== id);
        guardarYRefrescar();
    }
};

window.cambiarEstado = (id) => {
    inventario = inventario.map(el => {
        if (el.id === id) {
            el.estado = (el.estado === 'pendiente') ? 'completado' : 'pendiente';
        }
        return el;
    });
    guardarYRefrescar();
};

window.prepararEdicion = (id) => {
    const encontrado = inventario.find(el => el.id === id);
    document.getElementById('titulo').value = encontrado.titulo;
    document.getElementById('descripcion').value = encontrado.descripcion;
    idEdicion = id;
    document.getElementById('submitBtn').textContent = "Actualizar";
};

cajaBusqueda.addEventListener('input', dibujarInventario);
document.getElementById('filtroEstado').addEventListener('change', dibujarInventario);

function actualizarContador() {
    const total = inventario.length;
    const listos = inventario.filter(i => i.estado === 'completado').length;
    document.getElementById('contador').textContent = `${listos} de ${total} completados`;
}

cargarDatosIniciales();