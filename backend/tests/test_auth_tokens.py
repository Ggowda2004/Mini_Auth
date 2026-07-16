from app.core.security import create_access_token, create_refresh_token
from app.services import auth_service


def test_create_access_token_returns_string():
    token = create_access_token({"sub": "123"})
    assert isinstance(token, str)


def test_create_refresh_token_returns_string():
    token = create_refresh_token({"sub": "123"})
    assert isinstance(token, str)


def test_refresh_token_rotation_returns_new_refresh_token(monkeypatch):
    old_refresh_token = create_refresh_token({"sub": "123"})
    monkeypatch.setattr(auth_service.redis_client, "get", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(auth_service.redis_client, "setex", lambda *args, **kwargs: None)
    monkeypatch.setattr(auth_service, "create_access_token", lambda data: "new-access-token")
    monkeypatch.setattr(auth_service, "create_refresh_token", lambda data: "new-refresh-token")

    result = auth_service.auth_service_refresh_token(old_refresh_token)

    assert result["access_token"] == "new-access-token"
    assert result["refresh_token"] == "new-refresh-token"
    assert result["token_type"] == "bearer"
