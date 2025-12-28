'use client';
import { useState } from 'react';

export default function EvalPage() {
  const [metrics, setMetrics] = useState<any>(null);
  const load = async () => {
    const res = await fetch(process.env.NEXT_PUBLIC_API_BASE + '/eval/latest?workspace_id=1');
    const data = await res.json();
    setMetrics(data.metrics);
  };
  return (
    <div>
      <h2>Eval Dashboard</h2>
      <button onClick={load}>Load</button>
      <pre>{JSON.stringify(metrics, null, 2)}</pre>
    </div>
  );
}
