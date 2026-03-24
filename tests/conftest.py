import pytest
import os
import shutil
import json
from difflib import unified_diff

@pytest.fixture
def sample_capture_dir(tmp_path):
    # Create a temporary directory structure for a capture
    capture_dir = tmp_path / "captures" / "test_target" / "1234567890"
    capture_dir.mkdir(parents=True)

    # Mock HTML file
    html_content = "<html><body><h1>Hello Old</h1></body></html>"
    html_path = capture_dir / "content.html"
    html_path.write_text(html_content)

    # Mock screenshot files
    screenshot_path1 = capture_dir / "screenshot1.png"
    screenshot_path2 = capture_dir / "screenshot2.jpg"
    screenshot_path1.write_text("mock_image_data_1")
    screenshot_path2.write_text("mock_image_data_2")

    # Mock summary.json
    summary_data = {
        "changed_text": "old",
        "importance_score": 0.5,
        "category": "content_change"
    }
    summary_path = capture_dir / "summary.json"
    summary_path.write_text(json.dumps(summary_data))

    # Yield the paths for tests
    yield {
        "html_path": html_path,
        "screenshot_paths": [screenshot_path1, screenshot_path2],
        "summary_path": summary_path,
        "html_content": html_content,
        "target_url": "http://example.com/test_target"
    }
    # Teardown (tmp_path handles cleanup)

@pytest.fixture
def sample_diff():
    old_html = "<html><body><h1>Hello Old</h1><p>Some text</p></body></html>"
    new_html = "<html><body><h1>Hello New</h1><p>Some text updated</p></body></html>"
    
    # Generate a proper unified diff for consistency
    diff_generator = unified_diff(
        old_html.splitlines(),
        new_html.splitlines()
    )
    diff_text = '\n'.join(list(diff_generator)) # Join with newline to match expected output

    return {
        "capture_old": old_html,
        "capture_new": new_html,
        "diff_text": diff_text
    }
