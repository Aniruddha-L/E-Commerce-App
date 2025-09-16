import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const OrderSummary = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const order = location.state?.order;

  if (!order) {
    return (
      <div className="container" style={{ maxWidth: 600, margin: '40px auto', background: '#fff', borderRadius: 8, boxShadow: '0 4px 16px rgba(0,0,0,0.07)', padding: 32 }}>
        <h2 style={{ color: '#d8cb0c', textAlign: 'center', marginBottom: 24 }}>No Order Found</h2>
        <button onClick={() => navigate('/dashboard')} style={{ width: '100%', background: '#2563eb', color: 'white', fontWeight: 600, padding: 12, borderRadius: 6, border: 'none', fontSize: 16 }}>Go to Dashboard</button>
      </div>
    );
  }

  return (
    <div className="container" style={{ maxWidth: 600, margin: '40px auto', background: '#fff', borderRadius: 8, boxShadow: '0 4px 16px rgba(0,0,0,0.07)', padding: 32 }}>
      <h2 style={{ color: '#d8cb0c', textAlign: 'center', marginBottom: 24 }}>Order Summary</h2>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
        <div>
          <span style={{ color: '#2563eb', fontWeight: 600 }}>Items in Cart:</span>
          <div style={{ marginLeft: 8 }}>
            {order.cartItems && order.cartItems.length > 0 ? (
              <table style={{ width: '100%', marginTop: 8, marginBottom: 8, borderCollapse: 'collapse' }}>
                <thead>
                  <tr>
                    <th style={{ color: '#2563eb', textAlign: 'left', padding: '4px' }}>Name</th>
                    <th style={{ color: '#2563eb', textAlign: 'center', padding: '4px' }}>Qty</th>
                    <th style={{ color: '#2563eb', textAlign: 'right', padding: '4px' }}>Price</th>
                    <th style={{ color: '#2563eb', textAlign: 'right', padding: '4px' }}>Total</th>
                  </tr>
                </thead>
                <tbody>
                  {order.cartItems.map(item => (
                    <tr key={item.id}>
                      <td style={{ color: 'black', padding: '4px' }}>{item.name}</td>
                      <td style={{ color: 'black', textAlign: 'center', padding: '4px' }}>{item.quantity}</td>
                      <td style={{ color: 'black', textAlign: 'right', padding: '4px' }}>₹{item.price}</td>
                      <td style={{ color: 'black', textAlign: 'right', padding: '4px' }}>₹{item.price * item.quantity}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <span style={{ color: 'gray' }}>No items in cart.</span>
            )}
          </div>
        </div>
        <div>
          <span style={{ color: '#2563eb', fontWeight: 600 }}>Total Amount:</span>
          <span style={{ color: 'black', marginLeft: 8 }}>₹{order.totalAmount}</span>
        </div>
        <div>
          <span style={{ color: '#2563eb', fontWeight: 600 }}>Person Name:</span>
          <span style={{ color: 'black', marginLeft: 8 }}>{order.personName}</span>
        </div>
        <div>
          <span style={{ color: '#2563eb', fontWeight: 600 }}>Delivery Address:</span>
          <span style={{ color: 'black', marginLeft: 8 }}>
            {order.address1}<br />
            {order.address2}<br />
            {order.city}, {order.state} - {order.pincode}
          </span>
        </div>
        <div>
          <span style={{ color: '#2563eb', fontWeight: 600 }}>Contact Number:</span>
          <span style={{ color: 'black', marginLeft: 8 }}>{order.contact}</span>
        </div>
        <div>
          <span style={{ color: '#2563eb', fontWeight: 600 }}>Expected Delivery Date:</span>
          <span style={{ color: 'black', marginLeft: 8 }}>{order.deliveryDate}</span>
        </div>
      </div>
      <button onClick={() => navigate('/dashboard')} style={{ width: '100%', background: '#2563eb', color: 'white', fontWeight: 600, padding: 12, borderRadius: 6, border: 'none', fontSize: 16, marginTop: 24 }}>Go to Dashboard</button>
    </div>
  );
};

export default OrderSummary;
