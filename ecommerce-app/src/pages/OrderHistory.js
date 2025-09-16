import React, { useEffect, useState } from 'react';
import Cookies from 'js-cookie';

const OrderHistory = () => {
  const [orders, setOrders] = useState([]);
  const username = (Cookies.get('user') || 'aniruddha').toLowerCase(); // fallback for demo

  useEffect(() => {
    fetch(`http://localhost:5000/orders/${username}`)
      .then(res => res.json())
      .then(data => {
        setOrders(data || []);
      });
  }, [username]);

  return (
    <div className="container" style={{ maxWidth: 800, margin: '40px auto', background: '#fff', borderRadius: 8, boxShadow: '0 4px 16px rgba(0,0,0,0.07)', padding: 32 }}>
      <h2 style={{ color: '#d8cb0c', textAlign: 'center', marginBottom: 24 }}>Order History</h2>
      {orders.length === 0 ? (
        <p style={{ color: 'gray', textAlign: 'center' }}>No orders found.</p>
      ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <th style={{ color: '#2563eb', textAlign: 'left', padding: '8px' }}>Order ID</th>
              <th style={{ color: '#2563eb', textAlign: 'left', padding: '8px' }}>Items</th>
              <th style={{ color: '#2563eb', textAlign: 'right', padding: '8px' }}>Total Amount</th>
              <th style={{ color: '#2563eb', textAlign: 'center', padding: '8px' }}>Status</th>
              <th style={{ color: '#2563eb', textAlign: 'center', padding: '8px' }}>Delivery Date</th>
            </tr>
          </thead>
          <tbody>
            {orders.map(order => (
              <tr key={order.id}>
                <td style={{ color: 'black', padding: '8px' }}>{order.id}</td>
                <td style={{ color: 'black', padding: '8px' }}>
                  {order.items.map(item => (
                    <div key={item.name}>{item.name} x{item.quantity} (₹{item.price})</div>
                  ))}
                </td>
                <td style={{ color: 'black', textAlign: 'right', padding: '8px' }}>₹{order.totalAmount}</td>
                <td style={{ color: order.status === 'Delivered' ? 'green' : '#f97316', textAlign: 'center', fontWeight: 600, padding: '8px' }}>{order.status}</td>
                <td style={{ color: 'black', textAlign: 'center', padding: '8px' }}>{order.deliveryDate}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default OrderHistory;
