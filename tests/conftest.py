"""Pytest fixtures."""
import pytest


@pytest.fixture
def isolated_registry(monkeypatch, tmp_path):
    """Redirect ~/.saois to tmp_path so tests do not touch the developer machine."""
    from saois.core import config as cfg_mod

    d = tmp_path / ".saois"
    d.mkdir()
    monkeypatch.setattr(cfg_mod.config, "CONFIG_DIR", d)
    monkeypatch.setattr(cfg_mod.config, "PROJECTS_FILE", d / "projects.json")
    monkeypatch.setattr(cfg_mod.config, "SETTINGS_FILE", d / "settings.json")
    monkeypatch.setattr(cfg_mod.config, "TOOLS_FILE", d / "tools_config.json")
    (d / "projects.json").write_text("{}")

    monkeypatch.setattr(cfg_mod.config, "get_ai_projects_path", lambda: None)

    from saois.core.registry import Registry

    return Registry()
