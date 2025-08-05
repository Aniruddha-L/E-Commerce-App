import React, { useEffect, useRef } from 'react';

const Checkout = () => {
  const mapRef = useRef(null);

  useEffect(() => {
    // Load Google Maps script
    const script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=YOUR_GOOGLE_MAPS_API_KEY`;
    script.async = true;
    script.onload = () => {
      if (window.google) {
        new window.google.maps.Map(mapRef.current, {
          center: { lat: 28.6139, lng: 77.209 }, // Default to New Delhi
          zoom: 12,
        });
      }
    };
    document.body.appendChild(script);
    return () => {
      document.body.removeChild(script);
    };
  }, []);

  return (
    <div className="container" style={{ maxWidth: 600, margin: '40px auto', background: '#fff', borderRadius: 8, boxShadow: '0 4px 16px rgba(0,0,0,0.07)', padding: 32 }}>
      <h2 style={{ color: '#d8cb0c', textAlign: 'center', marginBottom: 24 }}>Checkout</h2>
      <form style={{ width: '100%', marginBottom: 24 }}>
        <label style={{ fontWeight: 600, marginBottom: 8, display: 'block' }}>Delivery Address</label>
        <input type="text" placeholder="Enter your address" style={{ marginBottom: 16, width: '100%' }} />
        <label style={{ fontWeight: 600, marginBottom: 8, display: 'block' }}>Contact Number</label>
        <input type="text" placeholder="Enter your contact number" style={{ marginBottom: 16, width: '100%' }} />
        <button type="submit" style={{ width: '100%', background: '#2563eb', color: 'white', fontWeight: 600, padding: 12, borderRadius: 6, border: 'none', fontSize: 16 }}>Place Order</button>
      </form>
      <div style={{ height: 400, width: '100%', borderRadius: 8, overflow: 'hidden', boxShadow: '0 2px 8px rgba(0,0,0,0.08)', marginBottom: 16 }} ref={mapRef} />
      <p style={{ color: '#324994', textAlign: 'center', fontWeight: 500 }}>Use the map above to confirm your delivery location.</p>
    </div>
  );
};

export default Checkout;
