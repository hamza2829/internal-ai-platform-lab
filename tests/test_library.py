import json
from pathlib import Path

from platform_app.library import list_entries
from platform_app.tools import run_agent_tools
from platform_app.adapters import MockAdapter, create_adapter


def test_registry_has_prompts_agents_skills_and_all_departments():
    entries = list_entries()
    assert {item["kind"] for item in entries} == {"prompt", "agent", "skill"}
    assert {item["department"] for item in entries} == {"sales", "product-development", "customer-service", "marketing"}
    assert all(item["version"] for item in entries)


def test_agents_call_only_allow_listed_mock_tools():
    assert len(run_agent_tools("sales-coach", "invented scenario")) == 2
    assert len(run_agent_tools("product-discovery", "invented scenario")) == 2
    assert len(run_agent_tools("service-guide", "invented scenario")) == 2
    assert run_agent_tools("unknown", "invented scenario") == []


def test_skill_folders_have_instructions_and_examples():
    root = Path(__file__).parents[1] / "library" / "skills"
    skills = list(root.rglob("SKILL.md"))
    assert len(skills) == 4
    assert all("## Instructions" in p.read_text() and "## Example" in p.read_text() for p in skills)


def test_eval_set_has_a_full_baseline_for_every_skill():
    data = json.loads((Path(__file__).parents[1] / "evals" / "skills.json").read_text())
    assert len(data["skills"]) == 4
    assert all(s["baseline_score"] == s["max_score"] for s in data["skills"])


def test_mock_adapter_is_deterministic_and_is_the_default(monkeypatch):
    monkeypatch.setenv("AI_ADAPTER", "mock")
    adapter = create_adapter()
    assert isinstance(adapter, MockAdapter)
    assert adapter.generate("prompt", "fictional note") == adapter.generate("prompt", "fictional note")
    assert "fictional note" in adapter.generate("prompt", "fictional note")
