from fastapi import status

from .utils import *
from ..routers.users import get_current_user, get_db
from ..main import app

app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db


# def test_return_user(test_user):
#     response = client.get("users/user")
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json()["username"] == "codingwithPrince"
#     assert response.json()["email"] == "codingwithPrince@tech.io"
#     assert response.json()["role"] == "admin"
#     assert response.json()["first_name"] == "Prince"
#     assert response.json()["last_name"] == "Asante"
#     assert response.json()["phone_number"] == "0033320034"
