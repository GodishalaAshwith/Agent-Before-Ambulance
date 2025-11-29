from datetime import datetime
from mcp import tool

@tool
def get_current_time() -> dict:
    """
    Simple MCP tool that returns the current timestamp.
    This satisfies the Tools (MCP) requirement with minimal code.
    """
    return {
        "timestamp": datetime.now().isoformat()
    }
