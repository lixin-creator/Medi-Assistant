"""Standalone hospital MCP-style HTTP server."""

from fastapi import FastAPI, HTTPException

from mcp_servers.hospital_server.providers.amap_provider import AMapHospitalProvider
from mcp_servers.hospital_server.schemas import (
    NearbyHospitalToolRequest,
    NearbyHospitalToolResponse,
)

app = FastAPI(title='Hospital MCP Server', version='1.0.0')
provider = AMapHospitalProvider()


@app.get('/health')
async def health_check():
    return {'status': 'ok', 'service': 'hospital-mcp-server'}


@app.post('/tools/search_nearby_hospitals', response_model=NearbyHospitalToolResponse)
async def search_nearby_hospitals(request: NearbyHospitalToolRequest):
    try:
        results = provider.search_nearby_hospitals(
            request.latitude,
            request.longitude,
            request.radius_meters,
            request.limit,
        )
    except Exception as exc:
        raise HTTPException(status_code=503, detail='amap_search_failed') from exc

    return NearbyHospitalToolResponse(success=True, results=results)
