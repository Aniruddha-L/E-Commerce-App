import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Login = ({ setIsLoggedIn }) => {
  const [credentials, setCredentials] = useState({ username: '', password: '' });
  const navigate = useNavigate();
  const [msg, setMsg] = useState()
  const [password, showPassword] = useState(false);

  const handleLogin = async () => {
    try {
      if (credentials.password.length === 0) return setMsg("Password is empty");
      if (credentials.password.length < 6) return setMsg("Minimum password length should be 6")
      const res = await axios.post('http://localhost:5000/login', credentials);
      localStorage.setItem('loggedInUser', res.data.username);
      setIsLoggedIn(true);
      navigate('/dashboard');
    } catch (err) {
      setMsg(err.response?.data?.message || 'Login failed');
    }
  };

  return (
    <div className="container">
      <h2>Login</h2>
      <input placeholder="Username" onChange={e => setCredentials({ ...credentials, username: e.target.value })} />
      <input type={password ? "text" : "password"} placeholder="Password" onChange={e => setCredentials({ ...credentials, password: e.target.value })} />
      <button onClick={() => showPassword(!password)}>Show Password</button>
      <button onClick={handleLogin}>Login</button>
      <button onClick={() => navigate('/register')}>Register</button>
      <p>{msg}</p>
    </div>
  );
};

export default Login;
