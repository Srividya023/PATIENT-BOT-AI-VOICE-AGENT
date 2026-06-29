from src.config import Settings


def test_settings_load_from_environment(monkeypatch) -> None:
    monkeypatch.setenv("DRY_RUN", "true")
    monkeypatch.setenv("ALLOWED_TARGET_NUMBER", "+1-805-439-8008")
    settings = Settings()
    assert settings.dry_run is True
    assert settings.allowed_target_number == "+18054398008"

