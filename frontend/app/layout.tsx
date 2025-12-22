export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ fontFamily: 'Arial, sans-serif', margin: 20 }}>
        <h1>opsrag-copilot</h1>
        <nav style={{ display: 'flex', gap: 12, marginBottom: 12 }}>
          <a href="/">Login</a>
          <a href="/chat">Chat</a>
          <a href="/retrieval">Retrieval</a>
          <a href="/docs">Docs</a>
          <a href="/approvals">Approvals</a>
          <a href="/audit">Audit</a>
          <a href="/eval">Eval</a>
        </nav>
        {children}
      </body>
    </html>
  );
}
