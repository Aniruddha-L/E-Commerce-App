import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import React, { useState } from 'react';
import Register from './pages/Register';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Cart from './pages/Cart';
import Checkout from './pages/Checkout';
import OrderSummary from './pages/OrderSummary';
import OrderHistory from './pages/OrderHistory';
import Navbar from './components/Navbar';
import './App.css';
import Cookies from 'js-cookie'

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(!!Cookies.get('user'));

  return (
    <div>
      <Router>
        <Navbar isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn} />
        <Routes>
          <Route path="/" element={<Dashboard status={isLoggedIn}/>} />
          <Route path="/register" element={<Register setIsLoggedIn={setIsLoggedIn} />} />
          <Route path="/login" element={<Login setIsLoggedIn={setIsLoggedIn} />} />
          <Route path="/dashboard" element={<Dashboard status={isLoggedIn}/>} />
          <Route path="/cart" element={isLoggedIn ? <Cart /> : <Navigate to="/login" />} />
          <Route path="/checkout" element={isLoggedIn ? <Checkout /> : <Navigate to="/login" />} />
          <Route path="/order-summary" element={<OrderSummary />} />
        </Routes>
      </Router>
    </div>
  );
};

export default App;
