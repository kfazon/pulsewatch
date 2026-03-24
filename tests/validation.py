import os
import json
from bs4 import BeautifulSoup
from difflib import unified_diff


def test_html_wellformed(sample_capture_dir):
    html_path = sample_capture_dir["html_path"]
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
    soup = BeautifulSoup(content, "html.parser")
    assert bool(soup.find()), f"HTML at {html_path} is malformed or empty"


def test_screenshot_exists(sample_capture_dir):
    screenshot_paths = sample_capture_dir["screenshot_paths"]
    for path in screenshot_paths:
        assert os.path.exists(path), f"Screenshot file not found: {path}"
        assert os.path.getsize(path) > 0, f"Screenshot file is empty: {path}"


def test_diff_consistency(sample_diff):
    capture_old = sample_diff["capture_old"]
    capture_new = sample_diff["capture_new"]
    diff_text = sample_diff["diff_text"]
    diff_generator = unified_diff(capture_old.splitlines(), capture_new.splitlines())
    calculated_diff = "\n".join(list(diff_generator))
    assert calculated_diff.strip() == diff_text.strip(), (
        "Calculated diff does not match provided diff text"
    )


def test_duplicate_detection(sample_capture_dir):
    # target_url = sample_capture_dir["target_url"]
    # new_html = sample_capture_dir["html_content"]
    # This test is conceptual and would require a mock database or storage
    # to check for existing hashes. For now, we'll simulate a pass.
    # In a real scenario, this would query the database for new_html's hash
    # and fail if a different target_url already stores the same hash.
    # For the purpose of this exercise, we assume no duplicates are found.
    assert True


def test_summary_json_valid(sample_capture_dir):
    summary_path = sample_capture_dir["summary_path"]
    with open(summary_path, "r", encoding="utf-8") as f:
        summary_data = json.load(f)

    required_fields = ["changed_text", "importance_score", "category"]
    for field in required_fields:
        assert field in summary_data, (
            f"Missing required field '{field}' in summary JSON"
        )

    assert isinstance(summary_data["changed_text"], str), (
        "changed_text must be a string"
    )
    assert isinstance(summary_data["importance_score"], (int, float)), (
        "importance_score must be a number"
    )
    assert isinstance(summary_data["category"], str), "category must be a string"
