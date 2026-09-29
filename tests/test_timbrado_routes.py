from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.modules.timbrados.deps import get_timbrado_service
from app.modules.timbrados.exceptions import InvoiceNotFoundException
from app.modules.timbrados.schemas import TimbradoResponse


@pytest.fixture
def service_mock():
    return AsyncMock()


@pytest_asyncio.fixture
async def client(service_mock):
    app.dependency_overrides[get_timbrado_service] = lambda: service_mock

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_create_timbrado_success(client, service_mock):
    uuid_fiscal = uuid4()

    service_mock.create.return_value = (
        TimbradoResponse(
            status="timbrada",
            external_id="req-abc-123",
            uuid_fiscal=uuid_fiscal,
            error=None,
        ),
        True,
    )

    response = await client.post(
        "/api/v1/timbrados",
        json={
            "external_id": "req-abc-123",
            "invoice_id": 1,
            "amount": 100,
        },
    )

    assert response.status_code == 201
    assert response.json()["status"] == "timbrada"
    assert response.json()["external_id"] == "req-abc-123"
    assert response.json()["uuid_fiscal"] == str(uuid_fiscal)

    service_mock.create.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_timbrado_duplicate(client, service_mock):
    uuid_fiscal = uuid4()

    service_mock.create.return_value = (
        TimbradoResponse(
            status="timbrada",
            external_id="req-abc-123",
            uuid_fiscal=uuid_fiscal,
            error=None,
        ),
        False,
    )

    response = await client.post(
        "/api/v1/timbrados",
        json={
            "external_id": "req-abc-123",
            "invoice_id": 1,
            "amount": 100,
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "timbrada"
    assert response.json()["external_id"] == "req-abc-123"
    assert response.json()["uuid_fiscal"] == str(uuid_fiscal)

    service_mock.create.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_timbrado_pac_failure(client, service_mock):
    service_mock.create.return_value = (
        TimbradoResponse(
            status="fallida",
            external_id="req-fail-123",
            uuid_fiscal=None,
            error="timeout",
        ),
        True,
    )

    response = await client.post(
        "/api/v1/timbrados",
        json={
            "external_id": "req-fail-123",
            "invoice_id": 1,
            "amount": 100,
        },
    )

    assert response.status_code == 422
    assert response.json()["status"] == "fallida"
    assert response.json()["external_id"] == "req-fail-123"
    assert response.json()["error"] == "timeout"

    service_mock.create.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_timbrado_invoice_not_found(client, service_mock):
    service_mock.create.side_effect = InvoiceNotFoundException(
        invoice_id=999
    )

    response = await client.post(
        "/api/v1/timbrados",
        json={
            "external_id": "req-not-found",
            "invoice_id": 999,
            "amount": 1500.50,
        },
    )

    assert response.status_code == 404

    service_mock.create.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_timbrado_invalid_payload(client, service_mock):
    response = await client.post(
        "/api/v1/timbrados",
        json={
            "external_id": "",
            "invoice_id": -1,
            "amount": -100,
        },
    )

    assert response.status_code == 400

    # Pydantic debe rechazar el payload antes de llegar al service.
    service_mock.create.assert_not_awaited()
