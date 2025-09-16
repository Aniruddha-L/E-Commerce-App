const express = require('express');
const fs = require('fs');
const cors = require('cors');
const bodyParser = require('body-parser');
const path = require('path');

console.log('Starting server...');

const app = express();
const PORT = 5000;
const USERS_FILE = path.join(__dirname, 'users.json');
const CARTS_FILE = path.join(__dirname, 'carts.json');
const ORDERS_FILE = path.join(__dirname, 'orders.json');

console.log('Files:', { USERS_FILE, CARTS_FILE, ORDERS_FILE });

app.use(cors());
app.use(bodyParser.json());

// Initialize carts.json if it doesn't exist
if (!fs.existsSync(CARTS_FILE)) {
  console.log('Creating carts.json file...');
  fs.writeFileSync(CARTS_FILE, JSON.stringify({}, null, 2));
}

// Initialize orders.json if it doesn't exist
if (!fs.existsSync(ORDERS_FILE)) {
  console.log('Creating orders.json file...');
  fs.writeFileSync(ORDERS_FILE, JSON.stringify({}, null, 2));
}

app.post('/register', (req, res) => {
  if (!req.body || !req.body.username || !req.body.password) {
    return res.status(400).json({ message: 'Invalid request body', data: req.body });
  }
  const { username, password } = req.body;
  let users = JSON.parse(fs.readFileSync(USERS_FILE, 'utf-8'));

  const exists = users.find(user => user.username === username);
  console.log(password.length);
  if (exists) return res.status(400).json({ message: 'User already exists' });
  users.push({ username, password });
  fs.writeFileSync(USERS_FILE, JSON.stringify(users, null, 2));
  return res.json({ message: 'User registered successfully' });
});

app.post('/login', (req, res) => {
  const { username, password } = req.body;
  let users = JSON.parse(fs.readFileSync(USERS_FILE, 'utf-8'));

  const match = users.find(user => user.username === username && user.password === password);
  if (!match) return res.status(401).json({ message: 'Invalid credentials' });

  res.json({ message: 'Login successful', username });
});

// Get user's cart
app.get('/cart/:username', (req, res) => {
  const { username } = req.params;
  let carts = JSON.parse(fs.readFileSync(CARTS_FILE, 'utf-8'));
  
  if (!carts[username]) {
    carts[username] = [];
    
  }
  
  res.json(carts[username]);
});

// Add item to cart
app.post('/cart/:username/add', (req, res) => {
  const { username } = req.params;
  const { product, quantity = 1 } = req.body;
  
  let carts = JSON.parse(fs.readFileSync(CARTS_FILE, 'utf-8'));
  
  if (!carts[username]) {
    carts[username] = [];
  }
  
  // Check if product already exists in cart
  const existingItemIndex = carts[username].findIndex(item => item.id === product.id);
  
  if (existingItemIndex !== -1) {
    // Update quantity of existing item
    carts[username][existingItemIndex].quantity += quantity;
  } else {
    // Add new item with quantity
    carts[username].push({
      ...product,
      quantity: quantity
    });
  }
  
  fs.writeFileSync(CARTS_FILE, JSON.stringify(carts, null, 2));
  res.json(carts[username]);
});

// Update item quantity in cart
app.put('/cart/:username/update', (req, res) => {
  const { username } = req.params;
  const { productId, quantity } = req.body;
  
  let carts = JSON.parse(fs.readFileSync(CARTS_FILE, 'utf-8'));
  
  if (!carts[username]) {
    return res.status(404).json({ message: 'Cart not found' });
  }
  
  const itemIndex = carts[username].findIndex(item => item.id === productId);
  
  if (itemIndex === -1) {
    return res.status(404).json({ message: 'Item not found in cart' });
  }
  
  if (quantity <= 0) {
    // Remove item if quantity is 0 or negative
    carts[username].splice(itemIndex, 1);
  } else {
    // Update quantity
    carts[username][itemIndex].quantity = quantity;
  }
  
  fs.writeFileSync(CARTS_FILE, JSON.stringify(carts, null, 2));
  res.json(carts[username]);
});

// Remove item from cart
app.delete('/cart/:username/remove/:productId', (req, res) => {
  const { username, productId } = req.params;
  
  let carts = JSON.parse(fs.readFileSync(CARTS_FILE, 'utf-8'));
  
  if (!carts[username]) {
    return res.status(404).json({ message: 'Cart not found' });
  }
  
  carts[username] = carts[username].filter(item => item.id !== parseInt(productId));
  
  fs.writeFileSync(CARTS_FILE, JSON.stringify(carts, null, 2));
  res.json(carts[username]);
});

// Clear user's cart
app.delete('/cart/:username/clear', (req, res) => {
  const { username } = req.params;
  
  let carts = JSON.parse(fs.readFileSync(CARTS_FILE, 'utf-8'));
  
  if (carts[username]) {
    carts[username] = [];
    fs.writeFileSync(CARTS_FILE, JSON.stringify(carts, null, 2));
  }
  
  res.json({ message: 'Cart cleared successfully' });
});

// Get user's order history
app.get('/orders/:username', (req, res) => {
  const { username } = req.params;
  let orders = {};
  if (fs.existsSync(ORDERS_FILE)) {
    orders = JSON.parse(fs.readFileSync(ORDERS_FILE, 'utf-8'));
  }
  res.json(orders[username] || []);
});

// Add new order for user
app.post('/orders/:username', (req, res) => {
  const { username } = req.params;
  const newOrder = req.body;
  let orders = {};
  if (fs.existsSync(ORDERS_FILE)) {
    orders = JSON.parse(fs.readFileSync(ORDERS_FILE, 'utf-8'));
  }
  if (!orders[username]) {
    orders[username] = [];
  }
  orders[username].push(newOrder);
  fs.writeFileSync(ORDERS_FILE, JSON.stringify(orders, null, 2));
  res.json({ message: 'Order saved', order: newOrder });
});

app.get('/', (req, res) => {
  res.send('E-commerce Backend is running');
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
