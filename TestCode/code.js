// Generic Node.js Backend Mock
const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(morgan('combined'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Mock Database
const mockData = {
  users: [
    { id: 1, name: 'John Doe', email: 'john@example.com' },
    { id: 2, name: 'Jane Smith', email: 'jane@example.com' }
  ],
  posts: [
    { id: 1, userId: 1, title: 'First Post', content: 'Hello World' },
    { id: 2, userId: 2, title: 'Second Post', content: 'Another Post' }
  ]
};

// Health Check Route
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'Server is running' });
});

// Users Routes
app.get('/api/users', (req, res) => {
  res.status(200).json(mockData.users);
});

app.get('/api/users/:id', (req, res) => {
  const user = mockData.users.find(u => u.id === parseInt(req.params.id));
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  res.status(200).json(user);
});

app.post('/api/users', (req, res) => {
  const { name, email } = req.body;
  if (!name || !email) {
    return res.status(400).json({ error: 'Name and email are required' });
  }
  const newUser = {
    id: mockData.users.length + 1,
    name,
    email
  };
  mockData.users.push(newUser);
  res.status(201).json(newUser);
});

app.put('/api/users/:id', (req, res) => {
  const user = mockData.users.find(u => u.id === parseInt(req.params.id));
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  const { name, email } = req.body;
  if (name) user.name = name;
  if (email) user.email = email;
  res.status(200).json(user);
});

app.delete('/api/users/:id', (req, res) => {
  const index = mockData.users.findIndex(u => u.id === parseInt(req.params.id));
  if (index === -1) {
    return res.status(404).json({ error: 'User not found' });
  }
  const deletedUser = mockData.users.splice(index, 1);
  res.status(200).json(deletedUser[0]);
});

// Posts Routes
app.get('/api/posts', (req, res) => {
  res.status(200).json(mockData.posts);
});

app.get('/api/posts/:id', (req, res) => {
  const post = mockData.posts.find(p => p.id === parseInt(req.params.id));
  if (!post) {
    return res.status(404).json({ error: 'Post not found' });
  }
  res.status(200).json(post);
});

app.post('/api/posts', (req, res) => {
  const { userId, title, content } = req.body;
  if (!userId || !title || !content) {
    return res.status(400).json({ error: 'userId, title, and content are required' });
  }
  const newPost = {
    id: mockData.posts.length + 1,
    userId,
    title,
    content
  };
  mockData.posts.push(newPost);
  res.status(201).json(newPost);
});

// Error Handling Middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Internal Server Error' });
});

// 404 Handler
app.use((req, res) => {
  res.status(404).json({ error: 'Route not found' });
});

// Start Server
if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
  });
}

module.exports = app;
