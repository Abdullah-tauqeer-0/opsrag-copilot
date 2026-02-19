def run_tool(db, workspace_id: int, tool_name: str, payload: dict):
    return {"id": f"mock-{tool_name}-001", "payload": payload}
