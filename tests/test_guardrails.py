from platform_app.guardrails import filter_output, inspect_input, risky_action


def test_personal_data_is_detected():
    assert "personal_data" in inspect_input("invented person demo@example.com")


def test_confidential_markers_are_detected():
    assert "confidential_marker" in inspect_input("CONFIDENTIAL fictional note")


def test_clean_input_passes():
    assert inspect_input("Invented sample case") == []


def test_risky_action_detection():
    assert risky_action("publish this draft")
    assert not risky_action("summarize this draft")


def test_unsafe_output_is_replaced():
    text, flags = filter_output("api_key: dont-repeat")
    assert "withheld" in text and flags == ["unsafe_output"]


def test_safe_output_passes():
    assert filter_output("A short safe draft") == ("A short safe draft", [])
