import pytest
import pytest_asyncio
from httpx import AsyncClient


def test_app_title(app):
    assert app.title == "testing"


@pytest_asyncio.fixture
async def prepare_users_and_roles(app):

    # Check if there are users in the database
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.get('/api/users/')

    # If there are no users, create a user
    if response.status_code == 200 and len(response.json()) == 0:
        async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
            response = await client.post('/api/users/', json={
                'username': 'testuser1',
                'email': 'testuser1@example.com',
                'full_name': 'First Test User'
            })

    # Check if there are roles in the database
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.get('/api/roles/')

    # If there are no roles, create a role
    if response.status_code == 200 and len(response.json()) == 0:
        async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
            response = await client.post('/api/roles/', json={
                'name': 'Super User',
                'description': 'A very busy user!'
            })


@pytest.mark.asyncio
@pytest.mark.usefixtures('prepare_users_and_roles')
async def test_add_user_to_role(app):
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.get('/api/users/1')
    user = response.json()

    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.get('/api/roles/1')
    role = response.json()

    role_with_user = role.copy()
    role_with_user.update({'users': [user]})

    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.post(f'/api/roles/{role["id"]}/user/{user["id"]}')
    assert response.status_code == 201
    assert response.json() == role_with_user


@pytest.mark.asyncio
async def test_add_duplicate_user_to_role(app):

    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.post(f'/api/roles/1/user/1')
    assert response.status_code == 400
    assert response.json() == {
        "detail": "User -> Role association already exists"
    }


@pytest.mark.asyncio
async def test_add_user_to_nonexsitant_role(app):
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.post(f'/api/roles/99/user/1')
    assert response.status_code == 400
    assert response.json() == {"detail": "Role not found"}


@pytest.mark.asyncio
async def test_add_nonexistant_user_to_role(app):
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.post(f'/api/roles/1/user/99')
    assert response.status_code == 400
    assert response.json() == {"detail": "User not found"}


@pytest.mark.asyncio
async def test_add_role_for_user(app):
    # vs adding a user to a role
    # create new role in database
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.post('/api/users/', json={
            'username': 'testuser2',
            'email': 'testuser2@example.com',
            'full_name': 'Second Test User'
        })
    assert response.status_code == 201
    user = response.json()

    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.post('/api/roles/', json={
            'name': 'super_user',
            'desription': 'Super User'
        })
    assert response.status_code == 201
    role = response.json()

    # add role to user
    user_with_role = user.copy()
    user_with_role.update({'roles': [role]})

    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.post(f'/api/users/{user["id"]}/role/{role["id"]}')
    assert response.status_code == 201
    assert response.json() == user_with_role


@pytest.mark.asyncio
async def test_add_nonexistant_role_for_user(app):
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.post(f'/api/users/1/role/99')
    assert response.status_code == 400
    assert response.json() == {"detail": "Role not found"}


@pytest.mark.asyncio
async def test_add_role_for_nonexistant_user(app):
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.post(f'/api/users/99/role/1')
    assert response.status_code == 400
    assert response.json() == {"detail": "User not found"}


@pytest.mark.asyncio
async def test_remove_user_from_role(app):
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.delete(f'/api/roles/1/user/1')
    assert response.status_code == 200
    assert response.json() == {"detail": "User removed from role"}


@pytest.mark.asyncio
async def test_remove_nonexistant_user_role(app):
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.delete(f'/api/roles/1/user/1')
    assert response.status_code == 400
    assert response.json() == {
        "detail": "User - Role association does not exist"}


@pytest.mark.asyncio
async def test_remove_nonexistant_user_from_role(app):
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.delete(f'/api/roles/1/user/88')
    assert response.status_code == 400
    assert response.json() == {"detail": "User not found"}


@pytest.mark.asyncio
async def test_remove_user_from_nonexistant_role(app):
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.delete(f'/api/roles/88/user/1')
    assert response.status_code == 400
    assert response.json() == {"detail": "Role not found"}


@pytest.mark.asyncio
async def test_remove_user_from_nonexistant_role(app):
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.delete(f'/api/users/1/role/88')
    assert response.status_code == 400
    assert response.json() == {"detail": "Role not found"}


@pytest.mark.asyncio
async def test_remove_nonexistant_user_from_role(app):
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.delete(f'/api/users/88/role/1')
    assert response.status_code == 400
    assert response.json() == {"detail": "User not found"}
