import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import products from '../data/products.json';

const Dashboard = ({status}) => {
  const username = localStorage.getItem('loggedInUser');
  const navigate = useNavigate();
  const [cart, setCart] = useState(false);
  const addToCart = async (product) => {
    if (!status) {
      localStorage.setItem('pendingProduct', JSON.stringify(product));
      navigate('/login');
      return;
    }
    const pendingProduct = JSON.parse(localStorage.getItem('pendingProduct'));
    let cart = JSON.parse(localStorage.getItem('cart') || '[]');
  
    if (pendingProduct) {
      cart.push(pendingProduct);
      localStorage.removeItem('pendingProduct'); 
    }
    if (!pendingProduct || pendingProduct.id !== product.id) {
      cart.push(product);
    }
  
    localStorage.setItem('cart', JSON.stringify(cart));
    setCart(true);
  };
  

  return (
    <div className="container">
  {status ? <h2>Hello, {username}</h2> : <h2>Please login to continue</h2>}
  <h3>Our Products</h3>
  {cart && <h3>Item added to cart</h3>}
  <div className="product-grid">
    {products.map(product => (
      <div key={product.id} className="product-card">
        <img src={product.image} alt={product.name} width="150" height='150' />
        <h4>{product.name}</h4>
        <p>₹{product.price}</p>
        <button onClick={() => addToCart(product)}>Add to Cart</button>
      </div>
    ))}
  </div>
</div>

  );
};

export default Dashboard;
