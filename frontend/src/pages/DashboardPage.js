import React, { useState, useEffect } from 'react';
import { policyAPI, aiAPI } from '../utils/api';

export default function DashboardPage() {
  const [policies, setPolicies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [aiResponse, setAiResponse] = useState('');
  const [userInput, setUserInput] = useState('');
  const [showAdvisor, setShowAdvisor] = useState(false);

  useEffect(() => {
    fetchPolicies();
  }, []);

  const fetchPolicies = async () => {
    try {
      setLoading(true);
      const response = await policyAPI.getPolicies();
      setPolicies(response.data);
    } catch (err) {
      console.error('Failed to fetch policies:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAiAdvisor = async (e) => {
    e.preventDefault();
    try {
      const response = await aiAPI.getPolicyRecommendations(userInput);
      setAiResponse(response.data);
      setUserInput('');
    } catch (err) {
      console.error('AI advisor error:', err);
    }
  };

  return (
    <div className="max-w-7xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-8">Dashboard</h1>
      
      {/* Active Policies Section */}
      <div className="grid md:grid-cols-2 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-2xl font-bold mb-4">Active Policies</h2>
          {loading ? (
            <p>Loading...</p>
          ) : policies.length === 0 ? (
            <p className="text-gray-500">No active policies</p>
          ) : (
            <div className="space-y-4">
              {policies.map((policy) => (
                <div key={policy.id} className="border p-4 rounded-lg">
                  <h3 className="font-bold">{policy.policy_type}</h3>
                  <p>Coverage: ₹{policy.coverage_amount}</p>
                  <p>Premium: ₹{policy.monthly_premium}/month</p>
                  <p className="text-sm text-gray-600">Status: {policy.status}</p>
                </div>
              ))}
            </div>
          )}
        </div>
        
        {/* AI Policy Advisor Section */}
        <div className="bg-blue-50 p-6 rounded-lg shadow">
          <h2 className="text-2xl font-bold mb-4">AI Policy Advisor</h2>
          <form onSubmit={handleAiAdvisor} className="space-y-4">
            <textarea
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              placeholder="Describe your insurance needs..."
              className="w-full p-3 border border-blue-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600"
              rows={3}
              required
            />
            <button type="submit" className="btn-primary w-full">
              Get Recommendations
            </button>
          </form>
          
          {aiResponse && (
            <div className="mt-6 bg-white p-4 rounded-lg">
              <p className="text-sm text-gray-600 mb-2">{aiResponse.message}</p>
              <div className="space-y-3">
                {aiResponse.recommendations?.map((rec) => (
                  <div key={rec.id} className="border-l-4 border-blue-600 pl-4">
                    <h4 className="font-bold">{rec.name}</h4>
                    <p>₹{rec.monthly} / month</p>
                    <p className="text-sm text-gray-600">{rec.description}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
