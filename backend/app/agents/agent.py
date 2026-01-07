from app.retrieval.hybrid import hybrid_retrieve


def is_action_request(message: str) -> bool:
    verbs = ["create", "post", "file", "open", "send", "notify", "update", "ticket", "jira", "slack", "github"]
    m = message.lower()
    return any(v in m for v in verbs)


def propose_tools(message: str):
    tools = []
    if "jira" in message.lower() or "ticket" in message.lower():
        tools.append({"tool": "jira.create_issue", "input": {"title": "GenAI risk", "body": message}})
    if "slack" in message.lower() or "notify" in message.lower():
        tools.append({"tool": "slack.post_message", "input": {"channel": "#general", "text": message}})
    if "github" in message.lower():
        tools.append({"tool": "github.create_issue", "input": {"repo": "demo/repo", "title": "Issue", "body": message}})
    return tools


def answer_from_context(question: str, contexts):
    snippets = [c["text"] for c in contexts]
    joined = "\n".join(snippets)
    return f"Answer (extractive):\n{joined[:800]}"


def run_agent(db, workspace_id: int, message: str):
    contexts = hybrid_retrieve(db, workspace_id, message, k=5)
    citations = [
        {
            "document": c["title"],
            "chunk_id": c["chunk_id"],
            "snippet": c["text"][:200],
        }
        for c in contexts
    ]

    if is_action_request(message):
        tool_calls = propose_tools(message)
        return {"mode": "proposal", "tool_calls": tool_calls, "citations": citations}

    answer = answer_from_context(message, contexts)
    return {"mode": "answer", "answer": answer, "citations": citations}
