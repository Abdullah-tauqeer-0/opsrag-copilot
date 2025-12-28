'use client';
import { useState } from 'react';

export default function AuditPage() {
  const [items, setItems] = useState<any[]>([]);
  const load = async () => {
    const res = await fetch(process.env.NEXT_PUBLIC_API_BASE + '/audit?workspace_id=1');
    const data = await res.json();
    setItems(data);
  };
  return (
    <div>
      <h2>Audit Logs</h2>
      <button onClick={load}>Load</button>
      <ul>{items.map((i, idx) => (<li key={idx}>{i.event} {i.at}</li>))}</ul>
    </div>
  );
}
