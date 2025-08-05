import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import products from '../data/products.json';
import Cookies from 'js-cookie';
import ToastMsg from '../components/Toast';
import 'bootstrap/dist/css/bootstrap.min.css';

const Dashboard = ({ status }) => {
  const username = Cookies.get('user');
  const navigate = useNavigate();
  const [cart, setCart] = useState(false);
  const [cartItems, setCartItems] = useState([]);
  const [productQuantities, setProductQuantities] = useState({});
  // Track which product's description is visible (store product ID or null)
  const [visibleDescId, setVisibleDescId] = useState(null);
  const [showToast, setShowToast] = useState(false);
  const [toastMessage, setToastMessage] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState(products);
  const [searchLoading, setSearchLoading] = useState(false);
  const searchTimeout = useRef(null);

  // Fetch cart items from backend when component mounts
  useEffect(() => {
    if (status && username) {
      fetchCartItems();
    }
  }, [status, username]);

  const fetchCartItems = async () => {
    try {
      const response = await fetch(`http://localhost:5000/cart/${username}`);
      const items = await response.json();
      setCartItems(items);
      const totalQuantity = items.reduce((sum, item) => sum + (item.quantity || 0), 0);
      Cookies.set('cart_total_quantity', totalQuantity, { expires: 7 });
      const quantities = {};
      items.forEach(item => {
        quantities[item.id] = item.quantity;
      });
      setProductQuantities(quantities);
    } catch (error) {
      console.error('Error fetching cart items:', error);
    }
  };

  const addToCart = async (product) => {
    // Remove login redirect from addToCart
    if (!status) {
      setToastMessage('Please login to add items to cart.');
      setShowToast(true);
      setTimeout(() => setShowToast(false), 3000);
      return;
    }

    try {
      const response = await fetch(`http://localhost:5000/cart/${username}/add`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ product, quantity: 1 }),
      });

      if (response.ok) {
        const updatedCart = await response.json();
        setCartItems(updatedCart);
        
        // Update product quantities
        const quantities = { ...productQuantities };
        quantities[product.id] = (quantities[product.id] || 0) + 1;
        setProductQuantities(quantities);
        
        // Show toast notification
        setToastMessage(product.name);
        setShowToast(true);
        setTimeout(() => setShowToast(false), 3000); // Hide toast after 3 seconds
        
        setCart(true);
        setTimeout(() => setCart(false), 2000); // Hide message after 2 seconds
      }
    } catch (error) {
      console.error('Error adding to cart:', error);
    }
  };

  const updateQuantity = async (productId, newQuantity) => {
    if (!status || !username) return;

    try {
      const response = await fetch(`http://localhost:5000/cart/${username}/update`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ productId, quantity: newQuantity }),
      });

      if (response.ok) {
        const updatedCart = await response.json();
        setCartItems(updatedCart);
        
        // Update product quantities
        const quantities = { ...productQuantities };
        if (newQuantity <= 0) {
          delete quantities[productId];
        } else {
          quantities[productId] = newQuantity;
        }
        setProductQuantities(quantities);
      }
    } catch (error) {
      console.error('Error updating quantity:', error);
    }
  };

  const incrementQuantity = (productId) => {
    const currentQuantity = productQuantities[productId] || 0;
    updateQuantity(productId, currentQuantity + 1);
  };

  const decrementQuantity = (productId) => {
    const currentQuantity = productQuantities[productId] || 0;
    if (currentQuantity > 0) {
      updateQuantity(productId, currentQuantity - 1);
    }
  };

  // Show description for product id
  const showDescription = (id) => {
    setVisibleDescId(id);
  };

  // Hide description
  const hideDescription = () => {
    setVisibleDescId(null);
  };

  const renderQuantityControls = (product) => {
    const quantity = productQuantities[product.id] || 0;
    
    if (quantity === 0) {
      return (
        <button 
          onClick={() => addToCart(product)}
          className="add-to-cart-btn"
        >
          Add to Cart
        </button>
      );
    }

    return (
      <div className="quantity-controls">
        <button
          onClick={() => decrementQuantity(product.id)}
          className="quantity-btn decrease"
          style={{textAlign: 'center'}}
        >
          -
        </button>
        <span className="quantity-display">
          {quantity}
        </span>
        <button
          onClick={() => incrementQuantity(product.id)}
          className="quantity-btn increase"
        >
          +
        </button>
      </div>
    );
  };

  useEffect(() => {
    if (searchTimeout.current) clearTimeout(searchTimeout.current);
    setSearchLoading(true);
    searchTimeout.current = setTimeout(() => {
      if (searchTerm.length < 4) {
        setSearchResults(products);
        setSearchLoading(false);
        return;
      }
      // Simulate async search
      new Promise((resolve) => {
        setTimeout(() => {
          resolve(products.filter(product => product.name.toLowerCase().includes(searchTerm.toLowerCase())));
        }, 400); // Simulate network delay
      }).then(results => {
        setSearchResults(results);
        setSearchLoading(false);
      });
    }, 350);
    return () => clearTimeout(searchTimeout.current);
  }, [searchTerm, products]);

  return (
    <div className="container" style={{ position: 'relative' }}>
      {/* Search Bar */}
      <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', zIndex: 10, background: 'white', boxShadow: '0 2px 8px rgba(0,0,0,0.07)', padding: '16px 0' }}>
        <input
          type="text"
          placeholder="Search products (min 4 letters)"
          value={searchTerm}
          onChange={e => setSearchTerm(e.target.value)}
          style={{ width: '100%', padding: '8px', fontSize: '16px', marginBottom: 0 }}
        />
      </div>
      <div style={{ height: 70 }} /> {/* Spacer for search bar */}
      {status ? <h2>Hello, {username}</h2> : <h2>Please login to continue</h2>}
      <h3>Our Products</h3>
      {cart && <h3 style={{ color: '#28a745' }}>Item added to cart</h3>}
      
      {/* Toast Notification */}
      <div style={{ position: 'fixed', top: '20px', right: '20px', zIndex: 1000 }}>
        <ToastMsg 
          msg={toastMessage} 
          show={showToast}
          onClose={() => setShowToast(false)}
        />
      </div>
      
      <div className="product-grid">
        {searchLoading && (
          <p style={{ color: '#2563eb', gridColumn: '1/-1', textAlign: 'center', width: '100%' }}>Searching...</p>
        )}
        {searchResults.length < products.length && searchTerm.length < 4 && !searchLoading && (
          <p style={{ color: 'red' }}>Enter at least 4 letters to search.</p>
        )}
        {searchResults.length === 0 && searchTerm.length >= 4 && !searchLoading && (
          <p style={{ color: 'gray', gridColumn: '1/-1', textAlign: 'center', width: '100%' }}>No products found</p>
        )}
        {searchResults.map((product) => (
          <div key={product.id} className="product-card">
            <img
              src="/info.png"
              className="info"
              tabIndex={0} // Make focusable
              onFocus={() => showDescription(product.id)}
              onBlur={hideDescription}
              onMouseEnter={() => showDescription(product.id)}
              onMouseLeave={hideDescription}
              alt="Info"
              style={{ cursor: 'pointer' }}
            />
            {visibleDescId === product.id && (
              <p className="description">{product.Description}</p>
            )}
            <img src={product.image} alt={product.name} width="150" height="150" />
            <h4>{product.name}</h4>
            <p>₹{product.price}</p>
            <p>{product.category}</p>
            {renderQuantityControls(product)}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
