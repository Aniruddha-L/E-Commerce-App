import React, { useEffect, useState } from 'react';

const Cart = () => {
  const [cartItems, setCartItems] = useState([]);
  const [showInvoice, setShowInvoice] = useState(false);

  useEffect(() => {
    const items = JSON.parse(localStorage.getItem('cart') || '[]');
    setCartItems(items);
  }, []);

  const removeFromCart = (indexToRemove) => {
    const updatedCart = cartItems.filter((_, index) => index !== indexToRemove);
    setCartItems(updatedCart);
    localStorage.setItem('cart', JSON.stringify(updatedCart));
  };

  const clearCart = () => {
    setCartItems([]);
    localStorage.removeItem('cart');
    setShowInvoice(false);
  };

  const totalCost = cartItems.reduce((sum, item) => sum + Number(item.price), 0);

  return (
    <div className="container">
      <h2>Your Cart</h2>
      {cartItems.length === 0 ? (
        <p>No items in cart.</p>
      ) : (
        <>
          {cartItems.map((item, index) => (
            <div key={index} style={{ marginBottom: '10px' }}>
              <h4>{item.name} - ₹{item.price}</h4>
              <button onClick={() => removeFromCart(index)}>Remove</button>
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
                <th style={{ borderBottom: '1px solid #ccc', textAlign: 'right' }}>Price (₹)</th>
              </tr>
            </thead>
            <tbody>
              {cartItems.map((item, index) => (
                <tr key={index}>
                  <td style={{ padding: '6px 0' }}>{item.name}</td>
                  <td style={{ padding: '6px 0', textAlign: 'right' }}>{item.price}</td>
                </tr>
              ))}
              <tr>
                <td style={{ paddingTop: '10px', fontWeight: 'bold' }}>Total</td>
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
