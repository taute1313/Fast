const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = 3000; 
const FASTAPI_URL = 'http://127.0.0.1:8000/api/v1'; // Ajustado a la base de la API

app.use(cors());
app.use(express.json());

// 1️⃣ SERVIR EL FRONTEND
app.use(express.static(path.join(__dirname, 'app/static')));

// 2️⃣ HELPER: PROXY CON AUTENTICACIÓN
// Ahora acepta un cuarto parámetro 'authHeader'
async function forwardRequest(method, endpoint, body = null, authHeader = null) {
    const url = `${FASTAPI_URL}${endpoint}`;
    
    const options = {
        method: method,
        headers: { 
            'Content-Type': 'application/json' 
        }
    };

    if (body) options.body = JSON.stringify(body);
    
    // Si recibimos token del navegador, se lo pasamos a Python
    if (authHeader) {
        options.headers['Authorization'] = authHeader;
    }

    try {
        const response = await fetch(url, options);
        
        // Manejar respuestas sin contenido (204 No Content)
        if (response.status === 204) return null;

        // Si la API devuelve error (400, 401, etc), lanzamos error con el mensaje
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: response.statusText }));
            throw { status: response.status, ...errorData };
        }

        return await response.json();
    } catch (error) {
        throw error; // Re-lanzar para manejarlo en el route handler
    }
}

// --- RUTAS DE AUTENTICACIÓN ---

app.post('/api/v1/auth/register', async (req, res) => {
    try {
        console.log('🔐 Registrando usuario...');
        const data = await forwardRequest('POST', '/auth/register', req.body);
        res.json(data);
    } catch (error) {
        res.status(error.status || 500).json(error);
    }
});

app.post('/api/v1/auth/login', async (req, res) => {
    try {
        console.log('🔑 Iniciando sesión...');
        const data = await forwardRequest('POST', '/auth/login', req.body);
        res.json(data);
    } catch (error) {
        res.status(error.status || 500).json(error);
    }
});

// --- RUTAS PROTEGIDAS (TAREAS) ---

app.get('/api/v1/tasks', async (req, res) => {
    try {
        // Capturamos el header Authorization que envía el navegador
        const auth = req.headers.authorization; 
        const data = await forwardRequest('GET', '/tasks/', null, auth);
        res.json(data);
    } catch (error) {
        res.status(error.status || 500).json(error);
    }
});

app.post('/api/v1/tasks', async (req, res) => {
    try {
        const auth = req.headers.authorization;
        const data = await forwardRequest('POST', '/tasks/', req.body, auth);
        res.status(201).json(data);
    } catch (error) {
        res.status(error.status || 500).json(error);
    }
});

app.patch('/api/v1/tasks/:id', async (req, res) => {
    try {
        const { id } = req.params;
        const auth = req.headers.authorization;
        const data = await forwardRequest('PATCH', `/tasks/${id}`, req.body, auth);
        res.json(data);
    } catch (error) {
        res.status(error.status || 500).json(error);
    }
});

app.delete('/api/v1/tasks/:id', async (req, res) => {
    try {
        const { id } = req.params;
        const auth = req.headers.authorization;
        await forwardRequest('DELETE', `/tasks/${id}`, null, auth);
        res.status(204).send();
    } catch (error) {
        res.status(error.status || 500).json(error);
    }
});

// Arrancar servidor
app.listen(PORT, () => {
    console.log(`\n🛡️  SAOAPI Middleware corriendo en: http://localhost:${PORT}`);
});
