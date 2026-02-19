'use client';
import { useState } from 'react';

export default function ChatPage() {
  const [answer, setAnswer] = useState('');
  const [citations, setCitations] = useState<any[]>([]);

  const send = async () => {
    const res = await fetch(process.env.NEXT_PUBLIC_API_BASE + '/chat?workspace_id=1&message=What%20is%20RMF%20Govern%20vs%20Map', { method: 'POST' });
    const data = await res.json();
    setAnswer(data.answer || JSON.stringify(data));
    setCitations(data.citations || []);
  };

  return (
    <div>
      <h2>Chat</h2>
      <button onClick={send}>Send Sample</button>
      <pre>{answer}</pre>
      <h3>Citations</h3>
      <ul>{citations.map((c, i) => (<li key={i}>{c.document} #{c.chunk_id}: {c.snippet}</li>))}</ul>
    </div>
  );
}
