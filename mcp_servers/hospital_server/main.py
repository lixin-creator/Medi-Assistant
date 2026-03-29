"""Entry point for the hospital MCP server."""

import uvicorn

from mcp_servers.hospital_server.config import (
    HOSPITAL_MCP_SERVER_HOST,
    HOSPITAL_MCP_SERVER_PORT,
)


if __name__ == '__main__':
    uvicorn.run(
        'mcp_servers.hospital_server.server:app',
        host=HOSPITAL_MCP_SERVER_HOST,
        port=HOSPITAL_MCP_SERVER_PORT,
        reload=False,
    )
