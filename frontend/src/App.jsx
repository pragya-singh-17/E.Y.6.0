import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './styles.css';

function Badge({ band, value }) {
  if (value == null) return <span className="badge">N/A</span>;
  return <span className={`badge ${band}`}>PCS {value.toFixed(1)} ({band})</span>;
}

function DriftChip({ bucket }) {
  if (!bucket) return <span className="chip">Drift N/A</span>;
  return <span className={`chip drift-${bucket.toLowerCase()}`}>Drift: {bucket}</span>;
}

function Dashboard({ stats }) {
  if (!stats) return null;
  return (
    <div className="card">
      <h2>Dashboard</h2>
      <p>Last run: {stats.latest_run.id ? `#${stats.latest_run.id} (${stats.latest_run.type})` : 'No runs yet'}</p>
      <p>
        Processed: {stats.latest_run.count_processed} | Auto-updates: {stats.latest_run.auto_updates} | Manual reviews: {stats.latest_run.manual_reviews}
      </p>
      <p>Average PCS: {stats.avg_pcs ? stats.avg_pcs.toFixed(1) : 'N/A'}</p>
      <p>
        Drift Distribution - Low: {stats.drift_distribution.Low}, Medium: {stats.drift_distribution.Medium}, High: {stats.drift_distribution.High}
      </p>
    </div>
  );
}

function ProviderList({ providers, onSelect }) {
  return (
    <div className="card">
      <h2>Providers</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Specialty</th>
            <th>PCS</th>
            <th>Drift</th>
          </tr>
        </thead>
        <tbody>
          {providers.map((p) => (
            <tr key={p.id} onClick={() => onSelect(p.id)} className="clickable">
              <td>{p.id}</td>
              <td>{p.name}</td>
              <td>{p.specialty}</td>
              <td><Badge band={p.pcs_band} value={p.pcs} /></td>
              <td><DriftChip bucket={p.drift_bucket} /></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function ProviderDetail({ provider, qa }) {
  if (!provider) return null;
  const score = provider.score || {};
  const drift = provider.drift || {};
  return (
    <div className="card">
      <h2>Provider Detail: {provider.name}</h2>
      <p>{provider.specialty} | {provider.address}</p>
      <Badge band={score.band} value={score.pcs} />
      <DriftChip bucket={drift.bucket} />
      <h3>PCS Breakdown</h3>
      <ul className="pcs-breakdown">
        <li>SRM: {score.srm?.toFixed(2)}</li>
        <li>FR: {score.fr?.toFixed(2)}</li>
        <li>ST: {score.st?.toFixed(2)}</li>
        <li>MB: {score.mb?.toFixed(2)}</li>
        <li>DQ: {score.dq?.toFixed(2)}</li>
        <li>RP: {score.rp?.toFixed(2)}</li>
        <li>LH: {score.lh?.toFixed(2)}</li>
        <li>HA: {score.ha?.toFixed(2)}</li>
      </ul>
      <h3>Field-level confidence</h3>
      <table>
        <thead>
          <tr>
            <th>Field</th>
            <th>Confidence</th>
            <th>Sources</th>
          </tr>
        </thead>
        <tbody>
          {qa.map((c, idx) => (
            <tr key={idx}>
              <td>{c.field_name}</td>
              <td>{c.confidence.toFixed(2)}</td>
              <td>{(c.sources || []).join(', ')}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <h3>Audit log</h3>
      <ul>
        {provider.audit_log.map((l, idx) => (
          <li key={idx}>
            [{l.created_at}] {l.action} {l.field_name}: {l.old_value} → {l.new_value}
          </li>
        ))}
      </ul>
    </div>
  );
}

function ManualReview({ items, onAction }) {
  return (
    <div className="card">
      <h2>Manual Review Queue</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Provider</th>
            <th>Field</th>
            <th>Current</th>
            <th>Suggested</th>
            <th>Reason</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {items.map((i) => (
            <tr key={i.id}>
              <td>{i.id}</td>
              <td>{i.provider_id}</td>
              <td>{i.field_name}</td>
              <td>{i.current_value}</td>
              <td>{i.suggested_value}</td>
              <td>{i.reason}</td>
              <td>{i.status}</td>
              <td>
                <button onClick={() => onAction(i.id, 'approve')}>Approve</button>
                <button onClick={() => {
                  const value = window.prompt('Override value', i.suggested_value || '');
                  if (value != null) onAction(i.id, 'override', value);
                }}>Override</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default function App() {
  const [stats, setStats] = useState(null);
  const [providers, setProviders] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [providerDetail, setProviderDetail] = useState(null);
  const [qa, setQa] = useState([]);
  const [manualItems, setManualItems] = useState([]);

  const loadAll = async () => {
    const [s, p, m] = await Promise.all([
      axios.get('/stats'),
      axios.get('/providers'),
      axios.get('/manual-review'),
    ]);
    setStats(s.data);
    setProviders(p.data);
    setManualItems(m.data);
  };

  useEffect(() => {
    loadAll();
  }, []);

  useEffect(() => {
    if (selectedId == null) return;
    (async () => {
      const [pd, q] = await Promise.all([
        axios.get(`/providers/${selectedId}`),
        axios.get(`/providers/${selectedId}/qa`),
      ]);
      setProviderDetail(pd.data);
      setQa(q.data);
    })();
  }, [selectedId]);

  const runBatch = async () => {
    await axios.post('/run-batch?type=daily');
    await loadAll();
  };

  const handleManualAction = async (id, action, value) => {
    if (action === 'approve') {
      await axios.post(`/manual-review/${id}/approve`);
    } else {
      await axios.post(`/manual-review/${id}/override?value=${encodeURIComponent(value)}`);
    }
    await loadAll();
    if (selectedId != null) {
      const [pd, q] = await Promise.all([
        axios.get(`/providers/${selectedId}`),
        axios.get(`/providers/${selectedId}/qa`),
      ]);
      setProviderDetail(pd.data);
      setQa(q.data);
    }
  };

  return (
    <div className="layout">
      <header>
        <h1>Provider Data Validation & Directory (Agentic AI)</h1>
        <button onClick={runBatch}>Run Daily Batch</button>
      </header>
      <div className="grid">
        <Dashboard stats={stats} />
        <ProviderList providers={providers} onSelect={setSelectedId} />
        <ProviderDetail provider={providerDetail} qa={qa} />
        <ManualReview items={manualItems} onAction={handleManualAction} />
      </div>
    </div>
  );
}
