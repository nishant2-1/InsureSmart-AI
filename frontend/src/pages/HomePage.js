import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { systemAPI } from '../utils/api';

export default function HomePage() {
  const [backendMessage, setBackendMessage] = useState('Connecting to backend...');

  useEffect(() => {
    const fetchHello = async () => {
      try {
        const response = await systemAPI.getHello();
        setBackendMessage(response.data.message);
      } catch (error) {
        setBackendMessage('Backend not reachable. Start Flask on port 5000.');
      }
    };

    fetchHello();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 to-blue-800 text-white">
      <div className="max-w-7xl mx-auto px-4 py-16 text-center">
        <h1 className="text-5xl font-bold mb-4">InsureSmart AI</h1>
        <p className="text-xl mb-8">Your intelligent insurance advisor powered by AI</p>
        <p className="text-sm bg-white/20 rounded-lg inline-block px-4 py-2">
          API Connection: {backendMessage}
        </p>
        
        <div className="grid md:grid-cols-3 gap-8 mt-16">
          <div className="bg-white bg-opacity-20 p-6 rounded-lg backdrop-blur">
            <h3 className="text-2xl font-bold mb-2">🤖 AI Powered</h3>
            <p>Get personalized policy recommendations using advanced AI</p>
          </div>
          
          <div className="bg-white bg-opacity-20 p-6 rounded-lg backdrop-blur">
            <h3 className="text-2xl font-bold mb-2">📊 Smart Dashboard</h3>
            <p>Track all your policies and claims in one place</p>
          </div>
          
          <div className="bg-white bg-opacity-20 p-6 rounded-lg backdrop-blur">
            <h3 className="text-2xl font-bold mb-2">🔒 Secure</h3>
            <p>Your data is safe with enterprise-grade security</p>
          </div>
        </div>
        
        <div className="mt-16 space-x-4">
          <Link to="/login" className="btn-primary">
            Login
          </Link>
          <Link to="/register" className="btn-secondary">
            Register
          </Link>
        </div>
      </div>
    </div>
  );
}
