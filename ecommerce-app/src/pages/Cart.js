import React, { useEffect, useState } from 'react';
import Cookies from 'js-cookie';

const Cart = () => {
  const [cartItems, setCartItems] = useState([]);
  const [showInvoice, setShowInvoice] = useState(false);
  const username = Cookies.get('user');

  useEffect(() => {
    if (username) {
      fetchCartItems();
    }
  }, [username]);

  const fetchCartItems = async () => {
    try {
      const response = await fetch(`http://localhost:5000/cart/${username}`);
      const items = await response.json();
      setCartItems(items);
    } catch (error) {
      console.error('Error fetching cart items:', error);
    }
  };

  const updateQuantity = async (productId, newQuantity) => {
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
      }
    } catch (error) {
      console.error('Error updating quantity:', error);
    }
  };

  const removeFromCart = async (productId) => {
    try {
      const response = await fetch(`http://localhost:5000/cart/${username}/remove/${productId}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        const updatedCart = await response.json();
        setCartItems(updatedCart);
      }
    } catch (error) {
      console.error('Error removing item:', error);
    }
  };

  const clearCart = async () => {
    try {
      const response = await fetch(`http://localhost:5000/cart/${username}/clear`, {
        method: 'DELETE',
      });

      if (response.ok) {
        setCartItems([]);
        setShowInvoice(false);
      }
    } catch (error) {
      console.error('Error clearing cart:', error);
    }
  };

  const incrementQuantity = (item) => {
    updateQuantity(item.id, item.quantity + 1);
  };

  const decrementQuantity = (item) => {
    if (item.quantity > 1) {
      updateQuantity(item.id, item.quantity - 1);
    } else {
      removeFromCart(item.id);
    }
  };

  const totalCost = cartItems.reduce((sum, item) => sum + (Number(item.price) * item.quantity), 0);

  return (
    <div className="container">
      <h2>Your Cart</h2>
      {cartItems.length === 0 ? (
        <p>YOUR CART IS EMPTY</p>
      ) : (
        <>
          {cartItems.map((item) => (
            <div key={item.id} className="cart-item">
              <div className="cart-item-content">
                <img 
                  src={item.image} 
                  alt={item.name} 
                  className="cart-item-image"
                />
                <div className="cart-item-details">
                  <h4 className="cart-item-title">{item.name}</h4>
                  <p className="cart-item-price">₹{item.price} each</p>
                  <p className="cart-item-total">
                    Total: ₹{item.price * item.quantity}
                  </p>
                  
                  <div className="cart-item-controls">
                    <div className="quantity-controls">
                      <button
                        onClick={() => decrementQuantity(item)}
                        className="quantity-btn decrease"
                      >
                        -
                      </button>
                      <span className="quantity-display">
                        {item.quantity}
                      </span>
                      <button
                        onClick={() => incrementQuantity(item)}
                        className="quantity-btn increase"
                      >
                        +
                      </button>
                    </div>
                    <button 
                      onClick={() => removeFromCart(item.id)}
                      className="remove-btn"
                    >
                      Remove
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}

          <hr />
          <h3>Total Cost: ₹{totalCost}</h3>

          <button
            onClick={clearCart}
            style={{ marginTop: '10px', backgroundColor: '#f97316' }}
          >
            Clear All
          </button>

          {/* ✅ Generate Invoice Button */}
          <button
            onClick={() => setShowInvoice(true)}
            style={{
              marginTop: '20px',
              marginLeft: '10px',
              backgroundColor: '#2563eb'
            }}
          >
            Generate Invoice
          </button>
        </>
      )}

      {/* ✅ Invoice Section */}
      {showInvoice && cartItems.length > 0 && (
        <div
          style={{
            marginTop: '30px',
            padding: '20px',
            border: '2px solid #ddd',
            borderRadius: '8px',
            backgroundColor: '#f8f8f8',
            color: 'black'
          }}
        >
          <h3 style={{ textAlign: 'center' }}>Invoice</h3>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th style={{ borderBottom: '1px solid #ccc', textAlign: 'left' }}>Item</th>
                <th style={{ borderBottom: '1px solid #ccc', textAlign: 'center' }}>Quantity</th>
                <th style={{ borderBottom: '1px solid #ccc', textAlign: 'right' }}>Price (₹)</th>
                <th style={{ borderBottom: '1px solid #ccc', textAlign: 'right' }}>Total (₹)</th>
              </tr>
            </thead>
            <tbody>
              {cartItems.map((item) => (
                <tr key={item.id}>
                  <td style={{ padding: '6px 0' }}>{item.name}</td>
                  <td style={{ padding: '6px 0', textAlign: 'center' }}>{item.quantity}</td>
                  <td style={{ padding: '6px 0', textAlign: 'right' }}>{item.price}</td>
                  <td style={{ padding: '6px 0', textAlign: 'right' }}>{item.price * item.quantity}</td>
                </tr>
              ))}
              <tr>
                <td colSpan="3" style={{ paddingTop: '10px', fontWeight: 'bold' }}>Total</td>
                <td style={{ paddingTop: '10px', textAlign: 'right', fontWeight: 'bold' }}>
                  ₹{totalCost}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default Cart;
