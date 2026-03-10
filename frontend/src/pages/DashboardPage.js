import React, { useEffect, useMemo, useState } from 'react';
import { policyAPI, aiAPI } from '../utils/api';

export default function DashboardPage() {
  const [policies, setPolicies] = useState([]);
  const [historyEntries, setHistoryEntries] = useState([]);
  const [chatTranscript, setChatTranscript] = useState([]);
  const [advisorInput, setAdvisorInput] = useState('');
  const [advisorProvider, setAdvisorProvider] = useState('');
  const [advisorReason, setAdvisorReason] = useState('');
  const [advisorNotice, setAdvisorNotice] = useState('');
  const [loadingPolicies, setLoadingPolicies] = useState(true);
  const [loadingHistory, setLoadingHistory] = useState(true);
  const [advisorLoading, setAdvisorLoading] = useState(false);
  const [advisorError, setAdvisorError] = useState('');

  useEffect(() => {
    fetchPolicies();
    fetchHistory();
  }, []);

  const fetchPolicies = async () => {
    try {
      setLoadingPolicies(true);
      const response = await policyAPI.getPolicies();
      setPolicies(response.data);
    } catch (err) {
      console.error('Failed to fetch policies:', err);
    } finally {
      setLoadingPolicies(false);
    }
  };

  const fetchHistory = async () => {
    try {
      setLoadingHistory(true);
      const response = await aiAPI.getChatHistory();
      setHistoryEntries(response.data);
    } catch (err) {
      console.error('Failed to fetch AI history:', err);
    } finally {
      setLoadingHistory(false);
    }
  };

  const handleAiAdvisor = async (e) => {
    e.preventDefault();
    if (!advisorInput.trim()) {
      return;
    }

    setAdvisorError('');
    setAdvisorProvider('');
    setAdvisorReason('');
    setAdvisorNotice('');
    const prompt = advisorInput.trim();
    setChatTranscript((prev) => [...prev, { role: 'user', content: prompt }]);
    setAdvisorInput('');

    try {
      setAdvisorLoading(true);
      const response = await aiAPI.getPolicyRecommendations(prompt);
      const provider = response.data.provider || 'fallback';
      const reason = response.data.reason || '';
      setAdvisorProvider(provider);
      setAdvisorReason(reason);
      if (provider === 'fallback') {
        setAdvisorNotice(response.data.message || 'AI advisor is running in fallback mode.');
      }

      const topRecommendation = response.data.recommendations?.[0]?.name;
      const advisorMessage = topRecommendation
        ? `${response.data.message} Best match: ${topRecommendation}.`
        : response.data.message;

      setChatTranscript((prev) => [
        ...prev,
        { role: 'assistant', content: advisorMessage }
      ]);
      await fetchHistory();
    } catch (err) {
      setAdvisorError('Advisor is currently unavailable. Please retry in a moment.');
      console.error('AI advisor error:', err);
    } finally {
      setAdvisorLoading(false);
    }
  };

  const activePolicies = useMemo(
    () => policies.filter((policy) => policy.status === 'active'),
    [policies]
  );

  const totalMonthlyPremium = useMemo(
    () => activePolicies.reduce((total, policy) => total + Number(policy.monthly_premium || 0), 0),
    [activePolicies]
  );

  const formatGBP = (amount) => `GBP ${Number(amount).toLocaleString('en-GB')}`;
  const websiteLink = typeof window !== 'undefined' ? window.location.origin : '';

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto grid max-w-7xl gap-6 p-4 md:grid-cols-[240px_1fr] md:p-8">
        <aside className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
          <h2 className="text-lg font-semibold tracking-wide">InsureSmart Console</h2>
          <p className="mt-1 text-sm text-slate-400">Risk and policy operations</p>
          <nav className="mt-8 space-y-2">
            <button className="w-full rounded-lg bg-cyan-500/20 px-3 py-2 text-left text-cyan-300">
              Dashboard
            </button>
            <button className="w-full rounded-lg px-3 py-2 text-left text-slate-300 hover:bg-slate-800">
              My Policies
            </button>
            <button className="w-full rounded-lg px-3 py-2 text-left text-slate-300 hover:bg-slate-800">
              Claims
            </button>
            <button className="w-full rounded-lg px-3 py-2 text-left text-slate-300 hover:bg-slate-800">
              AI Advisor
            </button>
          </nav>

          <div className="mt-8 rounded-lg border border-cyan-500/30 bg-cyan-500/10 p-3">
            <p className="text-xs uppercase tracking-wide text-cyan-300">Website Link</p>
            <a
              href={websiteLink}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-2 block break-all text-sm text-cyan-200 underline hover:text-cyan-100"
            >
              {websiteLink || 'Link will appear after page loads'}
            </a>
          </div>
        </aside>

        <main className="space-y-6">
          <header className="rounded-2xl border border-slate-800 bg-gradient-to-r from-slate-900 to-slate-800 p-6">
            <h1 className="text-3xl font-bold">Insurance Intelligence Dashboard</h1>
            <p className="mt-2 text-slate-300">
              Track your portfolio and consult the AI advisor for policy decisions.
            </p>
          </header>

          <section className="grid gap-4 sm:grid-cols-3">
            <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
              <p className="text-sm text-slate-400">Active Policies</p>
              <p className="mt-2 text-2xl font-semibold">{activePolicies.length}</p>
            </div>
            <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
              <p className="text-sm text-slate-400">Monthly Premium</p>
              <p className="mt-2 text-2xl font-semibold">{formatGBP(totalMonthlyPremium)}</p>
            </div>
            <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
              <p className="text-sm text-slate-400">Advisor Sessions</p>
              <p className="mt-2 text-2xl font-semibold">{historyEntries.length}</p>
            </div>
          </section>

          <section className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
            <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
              <h2 className="text-xl font-semibold">My Active Policies</h2>
              {loadingPolicies ? (
                <p className="mt-4 text-slate-400">Loading policies...</p>
              ) : activePolicies.length === 0 ? (
                <p className="mt-4 text-slate-400">No active policies yet.</p>
              ) : (
                <div className="mt-4 grid gap-4 md:grid-cols-2">
                  {activePolicies.map((policy) => (
                    <article
                      key={policy.id}
                      className="rounded-xl border border-slate-700 bg-slate-950 p-4 shadow"
                    >
                      <p className="text-xs uppercase tracking-wider text-cyan-300">{policy.policy_type}</p>
                      <p className="mt-2 text-lg font-semibold">Coverage: {formatGBP(policy.coverage_amount)}</p>
                      <p className="mt-1 text-sm text-slate-300">
                        Premium: {formatGBP(policy.monthly_premium)} / month
                      </p>
                      <p className="mt-2 inline-block rounded-full bg-emerald-500/20 px-2 py-1 text-xs text-emerald-300">
                        {policy.status}
                      </p>
                    </article>
                  ))}
                </div>
              )}
            </div>

            <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
              <h2 className="text-xl font-semibold">Consult AI Advisor</h2>
              <form onSubmit={handleAiAdvisor} className="mt-4 space-y-3">
                <textarea
                  value={advisorInput}
                  onChange={(event) => setAdvisorInput(event.target.value)}
                  placeholder="Example: I need travel insurance for a 10-day trip in Europe."
                  className="w-full rounded-lg border border-slate-700 bg-slate-950 p-3 text-sm text-slate-100 outline-none focus:border-cyan-400"
                  rows={4}
                  required
                />
                <button
                  type="submit"
                  disabled={advisorLoading}
                  className="w-full rounded-lg bg-cyan-500 px-4 py-2 font-medium text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {advisorLoading ? 'Consulting...' : 'Get Recommendation'}
                </button>
              </form>

              {advisorError && (
                <p className="mt-3 rounded-lg bg-rose-500/20 px-3 py-2 text-sm text-rose-300">{advisorError}</p>
              )}

              {advisorProvider === 'fallback' && (
                <div className="mt-3 rounded-lg border border-amber-500/40 bg-amber-500/15 px-3 py-2 text-sm text-amber-200">
                  <p className="font-medium">{advisorNotice || 'AI advisor is currently in fallback mode.'}</p>
                  {advisorReason && <p className="mt-1 text-amber-100">{advisorReason}</p>}
                </div>
              )}

              <div className="mt-5 space-y-3 rounded-xl border border-slate-800 bg-slate-950 p-3">
                <p className="text-sm font-medium text-slate-300">Chat Window</p>
                {chatTranscript.length === 0 ? (
                  <p className="text-sm text-slate-500">No messages yet.</p>
                ) : (
                  chatTranscript.map((item, index) => (
                    <div
                      key={`${item.role}-${index}`}
                      className={`rounded-lg px-3 py-2 text-sm ${
                        item.role === 'user'
                          ? 'bg-cyan-500/20 text-cyan-100'
                          : 'bg-slate-800 text-slate-100'
                      }`}
                    >
                      {item.content}
                    </div>
                  ))
                )}
              </div>

              <div className="mt-4">
                <p className="text-sm font-medium text-slate-300">Recent Advisor History</p>
                {loadingHistory ? (
                  <p className="mt-2 text-sm text-slate-500">Loading history...</p>
                ) : historyEntries.length === 0 ? (
                  <p className="mt-2 text-sm text-slate-500">No previous consultations.</p>
                ) : (
                  <ul className="mt-2 space-y-2 text-sm text-slate-300">
                    {historyEntries.slice(0, 4).map((entry) => (
                      <li key={entry.id} className="rounded-lg border border-slate-800 bg-slate-950 p-2">
                        <p className="font-medium">{entry.recommended_policy_name || 'No exact match'}</p>
                        <p className="text-slate-400">{entry.user_prompt}</p>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </div>
          </section>
        </main>
      </div>
    </div>
  );
}
