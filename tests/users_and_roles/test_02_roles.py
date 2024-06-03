import pytest
from httpx import AsyncClient
from ..utils import remove_uuid


def test_app_title(app):
    assert app.title == "testing"


@pytest.mark.asyncio
async def test_get_roles(app):  # Expect empty list as db has just been created
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.get('/api/roles/')
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
# Expect empty list as db has just been created
async def test_create_role(app):
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.post('/api/roles/', json={
            'name': 'admin',
            'description': 'Admin role'
        })
    assert response.status_code == 201
    response_json = remove_uuid(response.json())
    assert response_json == {'id': 1, 'name': 'admin',
                             'description': 'Admin role'}

    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.post('/api/roles/', json={
            'name': 'project_manager',
            'description': 'Project Manager role'
        })
    assert response.status_code == 201
    response_json = remove_uuid(response.json())
    assert response_json == {'id': 2, 'name': 'project_manager',
                             'description': 'Project Manager role'}


@pytest.mark.asyncio
async def test_update_role_name(app):
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.put('/api/roles/1', json={
            'name': 'administrator',
        })
    assert response.status_code == 200
    response_json = remove_uuid(response.json())
    assert response_json == {
        'id': 1, 'name': 'administrator', 'description': 'Admin role'}


@pytest.mark.asyncio
async def test_update_role_description(app):
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.put('/api/roles/1', json={
            'description': 'An important role',
        })
    assert response.status_code == 200
    response_json = remove_uuid(response.json())
    assert response_json == {
        'id': 1, 'name': 'administrator', 'description': 'An important role'}


@pytest.mark.asyncio
async def test_update_role_all(app):
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.put('/api/roles/1', json={
            'name': 'admin', 'description': 'Admin role'
        })
    assert response.status_code == 200
    response_json = remove_uuid(response.json())
    assert response_json == {
        'id': 1, 'name': 'admin', 'description': 'Admin role'}


@pytest.mark.asyncio
async def test_update_role_with_duplicate_name(app):
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.put('/api/roles/1', json={
            'name': 'project_manager', 'description': 'Admin role'
        })
    assert response.status_code == 400
    assert response.json() == {'detail': 'Role with that name already exists'}


@pytest.mark.asyncio
async def test_delete_role(app):
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.delete('/api/roles/2')
    assert response.status_code == 200
    assert response.json() == {'detail': 'Role deleted'}


@pytest.mark.asyncio
async def test_delete_non_existant_role(app):
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.delete('/api/roles/2')
    assert response.status_code == 400
    assert response.json() == {'detail': 'Role not found'}


@pytest.mark.asyncio
async def test_get_non_empty_roles(app):  # Expect list with single item
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.get('/api/roles/')
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_create_duplicate_role(app):
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.post('/api/roles/', json={
            'name': 'admin',
            'description': 'Admin role'
        })
    assert response.status_code == 400
    assert response.json() == {'detail': 'Role with that name already exists'}


@pytest.mark.asyncio
async def test_get_role_by_id(app):
    # Test gettting an existing role by id
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.get('/api/roles/1')
    assert response.status_code == 200
    response_json = remove_uuid(response.json())
    assert response_json == {'id': 1, 'name': 'admin',
                             'description': 'Admin role'}

    # Test gettting a non-existing role by id
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.get('/api/roles/99')
    assert response.status_code == 400
    assert response.json() == {'detail': 'Role not found'}


@pytest.mark.asyncio
async def test_get_role_by_uuid(app):
    # Get role to get uuid
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.get('/api/roles/1')
    test_role = response.json()
    test_uuid = test_role['uuid']

    # Test gettting an existing role by uuid
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.get('/api/roles/uuid/' + test_uuid)
    assert response.status_code == 200
    response_json = remove_uuid(response.json())
    assert response_json == {'id': 1, 'name': 'admin',
                             'description': 'Admin role'}

    # Test gettting a non-existing role by uuid
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.get('/api/roles/uuid/1231230123=102311-132')
    assert response.status_code == 400
    assert response.json() == {'detail': 'Role not found'}
