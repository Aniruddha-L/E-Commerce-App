import React from 'react';
import products from '../data/products.json';

const Dashboard = () => {
  const username = localStorage.getItem('loggedInUser');

  const addToCart = (product) => {
    const cart = JSON.parse(localStorage.getItem('cart') || '[]');
    cart.push(product);
    localStorage.setItem('cart', JSON.stringify(cart));
    alert('Added to cart');
  };

  return (
    <div className="container">
  <h2>Hello, {username}</h2>
  <h3>Our Products</h3>
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
