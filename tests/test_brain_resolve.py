"""Brain path resolution."""
from pathlib import Path

from saois.core.brain import Brain, resolve_brain_file


def test_resolve_prefers_docs_project_brain(tmp_path):
    proj = tmp_path / "myapp"
    proj.mkdir()
    (proj / "docs").mkdir()
    canonical = proj / "docs" / "project_brain.md"
    canonical.write_text("**Task Type:** plan\n", encoding="utf-8")
    assert resolve_brain_file(proj) == canonical


def test_resolve_finds_nested_brain(tmp_path):
    proj = tmp_path / "myapp"
    proj.mkdir()
    nested = proj / "meta"
    nested.mkdir()
    nb = nested / "project_brain.md"
    nb.write_text("**Task Type:** research\n", encoding="utf-8")
    assert resolve_brain_file(proj) == nb


def test_brain_normalizes_task_type(tmp_path):
    proj = tmp_path / "x"
    proj.mkdir()
    (proj / "docs").mkdir()
    (proj / "docs" / "project_brain.md").write_text(
        "**Task Type:** coding\n", encoding="utf-8"
    )
    b = Brain(proj)
    assert b.get_task_type() == "code"


def test_is_tool_installed_vscode_via_code(monkeypatch):
    import saois.core.config as cfg

    monkeypatch.setattr(
        cfg.shutil,
        "which",
        lambda name: "/usr/bin/code" if name == "code" else None,
    )
    c = cfg.Config()
    assert c.is_tool_installed("vscode") is True
