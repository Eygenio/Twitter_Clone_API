from fastapi import status
from starlette.testclient import TestClient


def test_health_check(api_client: TestClient, health_url: str) -> None:
    response = api_client.get(health_url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy"}


def test_get_tweets_unauthorized(api_client: TestClient, tweets_url: str) -> None:
    response = api_client.get(tweets_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_users_unauthorized(api_client: TestClient, users_url: str) -> None:
    response = api_client.get(f"{users_url}/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
