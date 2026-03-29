# Nearby Hospital MCP Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a standalone nearby-hospital button flow that gets the user's current location and returns nearby hospitals with normalized level and distance information, without coupling the feature into the chat LangGraph flow.

**Architecture:** Add a dedicated frontend button and result panel, expose a new backend endpoint at `/api/v1/hospitals/nearby`, introduce a service/client abstraction for hospital lookup, and keep the first version provider-compatible with a future MCP server. The backend owns normalization of hospital level and distance formatting so the UI stays simple.

**Tech Stack:** React, Vite, FastAPI, Pydantic, pytest, Vitest/Jest-style frontend tests, future MCP-compatible service abstraction.

---

### Task 1: Define backend schemas for nearby hospital search

**Files:**
- Create: `backend/app/schemas/hospital.py`
- Modify: `backend/app/schemas/__init__.py`
- Test: `backend/tests/test_hospital_schema.py`

**Step 1: Write the failing test**

Add schema tests for:

- request model accepts valid `latitude`, `longitude`, `radius_meters`, `limit`
- request model rejects invalid latitude/longitude ranges
- response model serializes hospital items with normalized fields

**Step 2: Run test to verify it fails**

Run: `pytest backend/tests/test_hospital_schema.py -v`
Expected: FAIL because schema module does not exist.

**Step 3: Write minimal implementation**

Create request/response Pydantic models:

- `NearbyHospitalRequest`
- `HospitalItem`
- `NearbyHospitalResponse`

Validation rules:

- latitude: `-90 <= x <= 90`
- longitude: `-180 <= x <= 180`
- radius_meters: positive, default `5000`
- limit: positive, capped to a reasonable max such as `20`

**Step 4: Run test to verify it passes**

Run: `pytest backend/tests/test_hospital_schema.py -v`
Expected: PASS

### Task 2: Add hospital normalization helpers and service tests

**Files:**
- Create: `backend/app/services/hospital_service.py`
- Test: `backend/tests/test_hospital_service.py`

**Step 1: Write the failing test**

Add tests for:

- hospital level normalization from raw source labels to canonical values
- distance formatting from meters to text
- service returns stable hospital output shape
- service surfaces empty results without crashing

**Step 2: Run test to verify it fails**

Run: `pytest backend/tests/test_hospital_service.py -v`
Expected: FAIL because service does not exist.

**Step 3: Write minimal implementation**

Implement:

- `normalize_hospital_level(raw_level: str | None) -> str`
- `format_distance(distance_meters: int | float | None) -> str`
- `HospitalService.search_nearby(...)`

Service should depend on a client abstraction instead of a concrete provider implementation.

**Step 4: Run test to verify it passes**

Run: `pytest backend/tests/test_hospital_service.py -v`
Expected: PASS

### Task 3: Add hospital client abstraction with MCP-compatible interface

**Files:**
- Create: `backend/app/tools/hospital_client.py`
- Test: `backend/tests/test_hospital_client.py`

**Step 1: Write the failing test**

Add tests for:

- client exposes `search_nearby_hospitals(...)`
- client returns provider data in predictable raw structure
- client raises or returns a controlled error on provider failure

**Step 2: Run test to verify it fails**

Run: `pytest backend/tests/test_hospital_client.py -v`
Expected: FAIL because client module does not exist.

**Step 3: Write minimal implementation**

Implement a thin client with one method:

- `search_nearby_hospitals(latitude, longitude, radius_meters, limit)`

Keep the implementation behind a provider boundary so it can later switch to a real MCP client without changing service or endpoint code.

**Step 4: Run test to verify it passes**

Run: `pytest backend/tests/test_hospital_client.py -v`
Expected: PASS

### Task 4: Add nearby hospital API endpoint

**Files:**
- Create: `backend/app/api/v1/endpoints/hospital.py`
- Modify: `backend/app/api/v1/endpoints/__init__.py`
- Modify: `backend/app/main.py`
- Test: `backend/tests/test_hospital_endpoint.py`

**Step 1: Write the failing test**

Add endpoint tests for:

- valid request returns `200` with `success=true`
- invalid coordinates return validation error
- backend service failure returns controlled API error

**Step 2: Run test to verify it fails**

Run: `pytest backend/tests/test_hospital_endpoint.py -v`
Expected: FAIL because endpoint is not registered.

**Step 3: Write minimal implementation**

Create `POST /api/v1/hospitals/nearby` endpoint that:

- parses request body using schema
- calls `HospitalService.search_nearby(...)`
- returns normalized response payload

Do not couple the endpoint to chat service or LangGraph workflow.

**Step 4: Run test to verify it passes**

Run: `pytest backend/tests/test_hospital_endpoint.py -v`
Expected: PASS

### Task 5: Add frontend API integration for nearby hospital search

**Files:**
- Modify: `frontend/src/App.jsx`
- Test: `frontend/src/App.test.jsx`

**Step 1: Write the failing test**

Add UI tests for:

- the nearby hospital button is rendered
- clicking the button requests browser geolocation
- successful geolocation triggers `POST /api/v1/hospitals/nearby`
- successful response renders hospital cards with name, level, and distance

**Step 2: Run test to verify it fails**

Run: `npm test -- --runInBand frontend/src/App.test.jsx`
Expected: FAIL because button and flow do not exist.

**Step 3: Write minimal implementation**

In `App.jsx` add:

- new translated button labels
- geolocation request handler
- loading and error state for nearby hospital search
- API request to `/api/v1/hospitals/nearby`
- result rendering section

Keep the feature independent from chat send flow.

**Step 4: Run test to verify it passes**

Run: `npm test -- --runInBand frontend/src/App.test.jsx`
Expected: PASS

### Task 6: Add frontend styling for hospital result cards

**Files:**
- Modify: `frontend/src/index.css`
- Test: `frontend/src/App.test.jsx`

**Step 1: Write the failing test**

If the existing frontend tests cover visible labels and cards, extend them to assert:

- hospital result section appears after a successful search
- navigation link/button is visible when provided

**Step 2: Run test to verify it fails**

Run: `npm test -- --runInBand frontend/src/App.test.jsx`
Expected: FAIL because result section lacks implementation/styling hooks.

**Step 3: Write minimal implementation**

Add styles for:

- nearby hospital action button
- loading/error message block
- result list card layout
- responsive spacing aligned with current UI style

**Step 4: Run test to verify it passes**

Run: `npm test -- --runInBand frontend/src/App.test.jsx`
Expected: PASS

### Task 7: Add backend provider configuration and documentation

**Files:**
- Modify: `README.md`
- Modify: `backend/app/core/config.py`
- Modify: `.env.example` (if present; otherwise document in `README.md` only)
- Test: `backend/tests/test_hospital_client.py`

**Step 1: Write the failing test**

If config is test-covered, add a test for hospital provider settings loading. If config is not test-covered, skip new config tests and document the settings in README.

**Step 2: Run test to verify it fails**

Run: `pytest backend/tests/test_hospital_client.py -v`
Expected: FAIL only if config behavior is newly tested.

**Step 3: Write minimal implementation**

Document or add config for:

- hospital provider base URL / API key
- feature enable flag if needed
- MCP endpoint URL for future migration

Keep config minimal and aligned with the current project style.

**Step 4: Run test to verify it passes**

Run: `pytest backend/tests/test_hospital_client.py -v`
Expected: PASS

### Task 8: Verify end-to-end behavior without touching chat flow

**Files:**
- Test: `backend/tests/test_hospital_endpoint.py`
- Test: `frontend/src/App.test.jsx`
- Check: `backend/app/core/langgraph_workflow.py`
- Check: `backend/app/services/chat_service.py`

**Step 1: Run targeted backend tests**

Run: `pytest backend/tests/test_hospital_schema.py backend/tests/test_hospital_service.py backend/tests/test_hospital_client.py backend/tests/test_hospital_endpoint.py -v`
Expected: PASS

**Step 2: Run targeted frontend tests**

Run: `npm test -- --runInBand frontend/src/App.test.jsx`
Expected: PASS

**Step 3: Sanity-check that chat flow is untouched**

Confirm no changes are required in:

- `backend/app/core/langgraph_workflow.py`
- `backend/app/services/chat_service.py`

**Step 4: Optional app smoke test**

Run backend and frontend locally, click the nearby-hospital button, allow geolocation, verify results render correctly.

