const express = require('express');
const fs = require('fs').promises;
const path = require('path');
const crypto = require('crypto');




const DATA_FILE = path.join(__dirname, 'data.json');
const PORT = process.env.PORT || 3000;

const app = express();
app.use(express.json());

// lightweight CORS (for development)
app.use((req, res, next) => {
    res.setHeader('Access-Control-Allow-Origin', process.env.CORS_ORIGIN || '*');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    res.setHeader('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS');
    if (req.method === 'OPTIONS') return res.sendStatus(204);
    next();
});

let store = { users: [] };

// load data from disk if exists
async function load() {
    try {
        const content = await fs.readFile(DATA_FILE, 'utf8');
        store = JSON.parse(content);
        if (!store || !Array.isArray(store.users)) store = { users: [] };
        console.log('Data loaded:', store.users.length, 'users');
    } catch (err) {
        if (err.code === 'ENOENT') {
            await save(); // create file
            console.log('No data file found. Initialized new store.');
        } else {
            console.error('Failed to load data:', err);
        }
    }
}

// save data to disk
async function save() {
    const tmp = DATA_FILE + '.tmp';
    await fs.writeFile(tmp, JSON.stringify(store, null, 2), 'utf8');
    await fs.rename(tmp, DATA_FILE);
}

// helpers
function id() {
    return crypto.randomBytes(8).toString('hex');
}
function validateUserPayload(payload) {
    if (!payload || typeof payload !== 'object') return 'Invalid payload';
    if (!payload.name || typeof payload.name !== 'string') return 'Name is required';
    if (!payload.email || typeof payload.email !== 'string') return 'Email is required';
    // simple email check
    if (!/^\S+@\S+\.\S+$/.test(payload.email)) return 'Email is invalid';
    return null;
}

// routes
app.get('/', (req, res) => {
    res.json({ message: 'Node backend running', version: '1.0.0' });
});

app.get('/health', (req, res) => res.json({ status: 'ok', uptime: process.uptime() }));

app.get('/users', (req, res) => {
    res.json(store.users);
});

app.get('/users/:id', (req, res) => {
    const u = store.users.find(x => x.id === req.params.id);
    if (!u) return res.status(404).json({ error: 'User not found' });
    res.json(u);
});

app.post('/users', async (req, res) => {
    const err = validateUserPayload(req.body);
    if (err) return res.status(400).json({ error: err });

    const existing = store.users.find(u => u.email === req.body.email);
    if (existing) return res.status(409).json({ error: 'Email already exists' });

    const user = {
        id: id(),
        name: req.body.name.trim(),
        email: req.body.email.toLowerCase().trim(),
        createdAt: new Date().toISOString()
    };
    store.users.push(user);
    try {
        await save();
        res.status(201).json(user);
    } catch (e) {
        console.error('Save error:', e);
        res.status(500).json({ error: 'Failed to save user' });
    }
});

app.put('/users/:id', async (req, res) => {
    const u = store.users.find(x => x.id === req.params.id);
    if (!u) return res.status(404).json({ error: 'User not found' });

    const payload = req.body;
    if (payload.name !== undefined) {
        if (typeof payload.name !== 'string' || !payload.name.trim()) return res.status(400).json({ error: 'Invalid name' });
        u.name = payload.name.trim();
    }
    if (payload.email !== undefined) {
        if (typeof payload.email !== 'string' || !/^\S+@\S+\.\S+$/.test(payload.email)) return res.status(400).json({ error: 'Invalid email' });
        const conflict = store.users.find(x => x.email === payload.email && x.id !== u.id);
        if (conflict) return res.status(409).json({ error: 'Email already in use' });
        u.email = payload.email.toLowerCase().trim();
    }
    u.updatedAt = new Date().toISOString();

    try {
        await save();
        res.json(u);
    } catch (e) {
        console.error('Save error:', e);
        res.status(500).json({ error: 'Failed to save user' });
    }
});

app.delete('/users/:id', async (req, res) => {
    const idx = store.users.findIndex(x => x.id === req.params.id);
    if (idx === -1) return res.status(404).json({ error: 'User not found' });
    const [removed] = store.users.splice(idx, 1);
    try {
        await save();
        res.json({ removed });
    } catch (e) {
        console.error('Save error:', e);
        res.status(500).json({ error: 'Failed to delete user' });
    }
});

// generic error handler
app.use((err, req, res, next) => {
    console.error('Unhandled error:', err);
    res.status(500).json({ error: 'Internal server error' });
});

let server;
async function start() {
    await load();
    server = app.listen(PORT, () => console.log(`Server listening on http://localhost:${PORT}`));
}
start();

// graceful shutdown
function shutdown() {
    console.log('Shutting down...');
    server && server.close(() => {
        console.log('Server closed');
        process.exit(0);
    });
    setTimeout(() => {
        console.log('Force exit');
        process.exit(1);
    }, 5000);
}
process.on('SIGINT', shutdown);
process.on('SIGTERM', shutdown);