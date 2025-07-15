import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = ({ isLoggedIn, setIsLoggedIn }) => {
  const handleLogout = () => {
    localStorage.removeItem('loggedInUser');
    localStorage.removeItem('cart');
    setIsLoggedIn(false);
    window.location.href = '/';
  };

  return (
    <nav>
      <div>
        <Link to="/">SUNNY</Link>
      </div>
      <div>
        {!isLoggedIn && <>
          <Link to="/register">Register</Link>
          <Link to="/login">Login</Link>
        </>}
        {isLoggedIn && <>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/cart">Cart</Link>
          <button onClick={handleLogout}>Logout</button>
        </>}
      </div>
    </nav>
  );
};

export default Navbar;
