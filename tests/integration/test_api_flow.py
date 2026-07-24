import pytest
from fastapi import status
from starlette.testclient import TestClient


@pytest.mark.integration
def test_health_and_tweet_flow(
    api_client: TestClient,
    tweets_url: str,
    users_url: str,
) -> None:
    resp = api_client.get("/health")
    assert resp.status_code == status.HTTP_200_OK

    resp = api_client.get(users_url + "/me")
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    headers = {"api-key": "test"}

    resp = api_client.post(
        tweets_url,
        json={
            "tweet_data": "Integration test tweet",
            "tweet_media_ids": None,
        },
        headers=headers,
    )
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    assert data["result"] is True
    assert "tweet_id" in data

    resp = api_client.get(tweets_url, headers=headers)
    assert resp.status_code == status.HTTP_200_OK
    tweets = resp.json()["tweets"]
    assert isinstance(tweets, list)
