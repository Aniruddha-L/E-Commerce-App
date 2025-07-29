import React, {useState, useEffect} from 'react';
import { Link } from 'react-router-dom';
import Cookies from 'js-cookie'

const Navbar = ({ isLoggedIn, setIsLoggedIn }) => {
  const [cartItems, setCartItems] = useState(0);
  const [cartTotalItems, setCartTotalItems] = useState(0);
  const handleLogout = () => {
    localStorage.removeItem('cart');
    setIsLoggedIn(false);
    window.location.href = '/';
    Cookies.remove('user')
  };
  useEffect(() => {
    const cartTotalItems = Cookies.get('cart_total_quantity');
    setCartItems(cartTotalItems);
  }, []);
  
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
          <Link to="/cart">Cart{cartTotalItems ? `(${cartTotalItems})` : ''}</Link> 
          <button onClick={handleLogout}>Logout</button>
        </>}
      </div>
    </nav>
  );
};

export default Navbar;
