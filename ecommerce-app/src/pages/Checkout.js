import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';

const Checkout = () => {
  const [fields, setFields] = useState({
    address1: '',
    address2: '',
    city: '',
    state: '',
    pincode: '',
    contact: ''
  });
  const [errors, setErrors] = useState({});
  const [errorMsg, setErrorMsg] = useState('');
  const [cartItems, setCartItems] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const username = Cookies.get('user');
    if (username) {
      fetch(`http://localhost:5000/cart/${username}`)
        .then(res => res.json())
        .then(items => setCartItems(items));
    }
  }, []);

  const handleChange = (e) => {
    setFields({ ...fields, [e.target.name]: e.target.value });
    setErrors({ ...errors, [e.target.name]: false });
    setErrorMsg('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newErrors = {};
    Object.keys(fields).forEach((key) => {
      if (!fields[key].trim()) newErrors[key] = true;
    });
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      setErrorMsg('Please fill all required fields.');
      return;
    }
    setErrorMsg('');
    // Simulate order details
    const username = Cookies.get('user') || 'aniruddha';
    const totalAmount = cartItems.reduce((sum, item) => sum + (Number(item.price) * item.quantity), 0);
    const deliveryDate = (() => {
      const days = Math.floor(Math.random() * 4) + 2;
      const date = new Date();
      date.setDate(date.getDate() + days);
      return date.toLocaleDateString();
    })();
    const newOrder = {
      id: Date.now(),
      items: cartItems.map(item => ({ name: item.name, quantity: item.quantity, price: item.price })),
      totalAmount,
      status: 'Placed',
      deliveryDate,
      address1: fields.address1,
      address2: fields.address2,
      city: fields.city,
      state: fields.state,
      pincode: fields.pincode,
      contact: fields.contact
    };
    // Save order to backend API
    await fetch(`http://localhost:5000/orders/${username}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newOrder)
    });
    navigate('/order-summary', {
      state: {
        order: {
          cartItems,
          totalAmount,
          personName: fields.contact,
          address1: fields.address1,
          address2: fields.address2,
          city: fields.city,
          state: fields.state,
          pincode: fields.pincode,
          contact: fields.contact,
          deliveryDate
        }
      }
    });
  };

  return (
    <div className="container" style={{ maxWidth: 600, margin: '40px auto', background: '#fff', borderRadius: 8, boxShadow: '0 4px 16px rgba(0,0,0,0.07)', padding: 32 }}>
      <h2 style={{ color: '#d8cb0c', textAlign: 'center', marginBottom: 24 }}>Checkout</h2>
      <form style={{ width: '100%', marginBottom: 24 }} onSubmit={handleSubmit}>
        <label style={{ fontWeight: 600, marginBottom: 8, display: 'block' }}>Address Line 1</label>
        <input name="address1" type="text" placeholder="Flat/House No, Building, Street" value={fields.address1} onChange={handleChange} style={{ marginBottom: 16, width: '100%', border: errors.address1 ? '2px solid red' : undefined }} />
        <label style={{ fontWeight: 600, marginBottom: 8, display: 'block' }}>Address Line 2</label>
        <input name="address2" type="text" placeholder="Area, Locality, Landmark" value={fields.address2} onChange={handleChange} style={{ marginBottom: 16, width: '100%', border: errors.address2 ? '2px solid red' : undefined }} />
        <label style={{ fontWeight: 600, marginBottom: 8, display: 'block' }}>City</label>
        <input name="city" type="text" placeholder="City" value={fields.city} onChange={handleChange} style={{ marginBottom: 16, width: '100%', border: errors.city ? '2px solid red' : undefined }} />
        <label style={{ fontWeight: 600, marginBottom: 8, display: 'block' }}>State</label>
        <input name="state" type="text" placeholder="State" value={fields.state} onChange={handleChange} style={{ marginBottom: 16, width: '100%', border: errors.state ? '2px solid red' : undefined }} />
        <label style={{ fontWeight: 600, marginBottom: 8, display: 'block' }}>Pincode</label>
        <input name="pincode" type="text" placeholder="Pincode" value={fields.pincode} onChange={handleChange} style={{ marginBottom: 16, width: '100%', border: errors.pincode ? '2px solid red' : undefined }} />
        <label style={{ fontWeight: 600, marginBottom: 8, display: 'block' }}>Contact Number</label>
        <input name="contact" type="text" placeholder="Enter your contact number" value={fields.contact} onChange={handleChange} style={{ marginBottom: 16, width: '100%', border: errors.contact ? '2px solid red' : undefined }} />
        {errorMsg && <div style={{ color: 'red', marginBottom: 16, textAlign: 'center', fontWeight: 500 }}>{errorMsg}</div>}
        <button type="submit" style={{ width: '100%', background: '#2563eb', color: 'white', fontWeight: 600, padding: 12, borderRadius: 6, border: 'none', fontSize: 16 }}>Place Order</button>
      </form>
    </div>
  );
};

export default Checkout;
