const express = require('express');
const fs = require('fs');
const cors = require('cors');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const PORT = 5000;
const USERS_FILE = path.join(__dirname, 'users.json');

app.use(cors());
app.use(bodyParser.json());

app.post('/register', (req, res) => {
  const { username, password } = req.body;
  let users = JSON.parse(fs.readFileSync(USERS_FILE, 'utf-8'));

  const exists = users.find(user => user.username === username);
  console.log(password.lenght);
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

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
