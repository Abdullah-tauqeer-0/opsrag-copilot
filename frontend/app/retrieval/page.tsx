'use client';
import { useState } from 'react';

export default function RetrievalPage() {
  const [items, setItems] = useState<any[]>([]);
  const run = async () => {
    const res = await fetch(process.env.NEXT_PUBLIC_API_BASE + '/retrieval/debug?workspace_id=1&query=RMF%20govern', { method: 'POST' });
    const data = await res.json();
    setItems(data);
  };
  return (
    <div>
      <h2>Retrieval Debug</h2>
      <button onClick={run}>Run</button>
      <ul>{items.map((i, idx) => (<li key={idx}>{i.title} score={i.score}</li>))}</ul>
    </div>
  );
}
