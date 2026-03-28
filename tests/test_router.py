"""Router launch modes (desktop vs browser)."""
import sys
from unittest.mock import MagicMock

import pytest

from saois.core.config import LAUNCH_BROWSER, LAUNCH_DESKTOP
from saois.core.router import Router


@pytest.fixture
def project_with_brain(tmp_path):
    p = tmp_path / "proj"
    p.mkdir()
    (p / "docs").mkdir()
    (p / "docs" / "project_brain.md").write_text("**Task Type:** code\n", encoding="utf-8")
    return p


def test_launch_tool_browser_when_not_installed(monkeypatch, project_with_brain):
    r = Router()
    monkeypatch.setattr(r.config, "is_tool_installed", lambda _tid: False)
    open_b = MagicMock()
    monkeypatch.setattr("saois.core.router.webbrowser.open", open_b)
    ok, msg, mode = r.launch_tool("windsurf", project_with_brain)
    assert ok
    assert mode == LAUNCH_BROWSER
    assert "browser" in msg.lower()
    open_b.assert_called_once()


def test_launch_tool_desktop_when_installed(monkeypatch, project_with_brain):
    r = Router()
    monkeypatch.setattr(r.config, "is_tool_installed", lambda _tid: True)
    monkeypatch.setattr(
        r.config,
        "get_tool_launch_command",
        lambda _tid, pp: (sys.executable, ["-c", "pass"]),
    )
    popen = MagicMock()
    monkeypatch.setattr("saois.core.router.subprocess.Popen", popen)
    ok, msg, mode = r.launch_tool("windsurf", project_with_brain)
    assert ok
    assert mode == LAUNCH_DESKTOP
    popen.assert_called_once()


def test_launch_for_project_returns_five_tuple(monkeypatch, project_with_brain):
    r = Router()
    monkeypatch.setattr(r.config, "is_tool_installed", lambda _tid: False)
    monkeypatch.setattr("saois.core.router.webbrowser.open", MagicMock())
    out = r.launch_for_project(project_with_brain)
    assert len(out) == 5
    success, message, tool_name, task_type, mode = out
    assert success
    assert task_type == "code"
    assert mode == LAUNCH_BROWSER
