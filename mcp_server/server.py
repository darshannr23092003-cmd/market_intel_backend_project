from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mcp_server import tools

app = FastAPI(title="MCP Tool Server")


class ToolRequest(BaseModel):
    args: dict


@app.post("/tool/{tool_name}")
def call_tool(tool_name: str, req: ToolRequest):
    if not hasattr(tools, tool_name):
        raise HTTPException(status_code=404, detail="Tool not found")

    tool_func = getattr(tools, tool_name)

    try:
        result = tool_func(**req.args)
    except TypeError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "tool": tool_name,
        "result": result
    }


@app.get("/health")
def health():
    return {"status": "mcp server healthy"}
