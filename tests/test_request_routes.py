# import pytest

# from httpx import AsyncClient
# from code.main import app
# from os import getenv

# @pytest.mark.apitest
# @pytest.mark.anyio
# async def test_ini():
#     async with AsyncClient(app=app , base_url=getenv('URL_API_TO_TEST')) as ac:
#         response = await ac.post('/', json={"phone": "teste", "token": "teste"})
#         # response = await ac.post('/run-browser', data={"phone": "teste", "token": "teste"})
#     print(response.json())
#     # assert response.json() == ["teste"]
