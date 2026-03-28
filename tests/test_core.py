"""
SAOIS Core Tests
Tests for config, registry, brain, and router modules.
"""
import pytest
import tempfile
import json
from pathlib import Path
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from saois.core.config import Config
from saois.core.registry import Registry
from saois.core.brain import Brain


class TestConfig:
    """Tests for Config class."""
    
    def test_config_initialization(self):
        """Config should initialize without errors."""
        config = Config()
        assert config is not None
    
    def test_get_os(self):
        """Should detect operating system."""
        config = Config()
        os_type = config.get_os()
        assert os_type in ["windows", "macos", "linux"]
    
    def test_tool_routing_defaults(self):
        """Should have default tool routing."""
        config = Config()
        assert "code" in config.DEFAULT_TOOL_ROUTING
        assert "research" in config.DEFAULT_TOOL_ROUTING
        assert "plan" in config.DEFAULT_TOOL_ROUTING
    
    def test_get_best_tool_for_task(self):
        """Should return a tool for any task type."""
        config = Config()
        
        # Test all task types
        for task in ["code", "coding", "research", "plan", "planning", "debugging"]:
            tool = config.get_best_tool_for_task(task)
            assert tool is not None
            assert isinstance(tool, str)
    
    def test_tool_urls_exist(self):
        """All tools should have URLs."""
        config = Config()
        for tool_id in config.TOOL_NAMES.keys():
            assert tool_id in config.TOOL_URLS


class TestRegistry:
    """Tests for Registry class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_project = Path(self.temp_dir) / "test_project"
        self.test_project.mkdir()
    
    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_registry_initialization(self):
        """Registry should initialize without errors."""
        registry = Registry()
        assert registry is not None
    
    def test_add_and_get_project(self, isolated_registry):
        """Should add and retrieve projects."""
        registry = isolated_registry

        # Add project
        registry.add("test_project", self.test_project)
        
        # Get project
        path = registry.get("test_project")
        assert path is not None
        assert path.name == "test_project"
    
    def test_project_exists(self, isolated_registry):
        """Should check if project exists."""
        registry = isolated_registry
        registry.add("test_project", self.test_project)
        
        assert registry.exists("test_project") == True
        assert registry.exists("nonexistent") == False
    
    def test_remove_project(self, isolated_registry):
        """Should remove projects."""
        registry = isolated_registry
        registry.add("test_project", self.test_project)
        
        assert registry.exists("test_project") == True
        registry.remove("test_project")
        assert registry.exists("test_project") == False
    
    def test_import_projects_counts_new_and_existing(self, isolated_registry):
        """import_projects returns (new_count, already_registered_count)."""
        registry = isolated_registry
        registry.add("existing", self.test_project)
        found = {
            "existing": str(self.test_project),
            "brand_new": str(Path(self.temp_dir) / "brand_new"),
        }
        (Path(self.temp_dir) / "brand_new").mkdir()
        new_ct, skip_ct = registry.import_projects(found)
        assert new_ct == 1
        assert skip_ct == 1

    def test_scan_folder(self):
        """Should scan folder for projects."""
        registry = Registry()
        
        # Create some test projects
        (Path(self.temp_dir) / "project1").mkdir()
        (Path(self.temp_dir) / "project2").mkdir()
        (Path(self.temp_dir) / ".hidden").mkdir()  # Should be ignored
        
        found = registry.scan_folder(Path(self.temp_dir))
        
        assert "project1" in found
        assert "project2" in found
        assert ".hidden" not in found
    
    def test_search_projects(self, isolated_registry):
        """Should search projects by name."""
        registry = isolated_registry
        registry.add("my_app", self.test_project)
        registry.add("my_website", self.test_project)
        registry.add("other", self.test_project)
        
        results = registry.search("my")
        assert "my_app" in results
        assert "my_website" in results
        assert "other" not in results
    
    def test_validate_projects(self, isolated_registry):
        """Should validate project paths."""
        registry = isolated_registry
        registry.add("valid", self.test_project)
        registry.add("invalid", Path("/nonexistent/path"))
        
        valid, missing = registry.validate()
        
        assert "valid" in valid
        assert "invalid" in missing


class TestBrain:
    """Tests for Brain class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)
    
    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_brain_initialization(self):
        """Brain should initialize without errors."""
        brain = Brain(self.project_path)
        assert brain is not None
    
    def test_brain_not_exists_initially(self):
        """Brain should not exist before creation."""
        brain = Brain(self.project_path)
        assert brain.exists() == False
    
    def test_create_brain(self):
        """Should create brain file."""
        brain = Brain(self.project_path)
        brain.create("code")
        
        assert brain.exists() == True
        assert brain.brain_file.exists() == True
    
    def test_get_task_type_default(self):
        """Should return default task type."""
        brain = Brain(self.project_path)
        task_type = brain.get_task_type()
        
        assert task_type == "code"  # Default
    
    def test_get_task_type_from_brain(self):
        """Should read task type from brain file."""
        brain = Brain(self.project_path)
        brain.create("research")
        
        # Reload brain
        brain2 = Brain(self.project_path)
        assert brain2.get_task_type() == "research"
    
    def test_is_template(self):
        """Should detect template brain."""
        brain = Brain(self.project_path)
        
        # No brain = template
        assert brain.is_template() == True
        
        # Created brain is still template (has placeholders)
        brain.create("code")
        assert brain.is_template() == True
    
    def test_detect_run_command_nodejs(self):
        """Should detect Node.js run command."""
        # Create package.json
        pkg = {"scripts": {"dev": "next dev", "start": "next start"}}
        (self.project_path / "package.json").write_text(json.dumps(pkg))
        
        brain = Brain(self.project_path)
        cmd = brain._detect_run_command()
        
        assert cmd == "npm run dev"
    
    def test_detect_run_command_python(self):
        """Should detect Python run command."""
        (self.project_path / "requirements.txt").write_text("flask")
        (self.project_path / "app.py").write_text("# app")
        
        brain = Brain(self.project_path)
        cmd = brain._detect_run_command()
        
        assert cmd == "python app.py"
    
    def test_detect_run_command_docker(self):
        """Should detect Docker run command."""
        (self.project_path / "docker-compose.yml").write_text("version: '3'")
        
        brain = Brain(self.project_path)
        cmd = brain._detect_run_command()
        
        assert cmd == "docker-compose up"


class TestIntegration:
    """Integration tests for full workflows."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir) / "my_project"
        self.project_path.mkdir()
    
    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_full_workflow(self, isolated_registry):
        """Test complete workflow: add project, create brain, get tool."""
        from saois.core.brain import Brain
        from saois.core.router import Router

        registry = isolated_registry
        registry.add("my_project", self.project_path)
        
        # Create brain
        brain = Brain(self.project_path)
        brain.create("code")
        
        # Get tool
        router = Router()
        tool_id, task_type = router.get_tool_for_project(self.project_path)
        
        assert tool_id is not None
        assert task_type == "code"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
