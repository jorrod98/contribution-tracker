import json
from pathlib import Path
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from unittest.mock import patch

from contribution_tracker.cli import _parser, main
from contribution_tracker.viewer import render_html


class ContributionTrackerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_file = Path(self.temp_dir.name) / "tracker.json"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_default_data_file_is_in_project_directory(self) -> None:
        args = _parser().parse_args(["list"])
        project_dir = Path(__file__).resolve().parents[1]

        self.assertEqual(args.data_file, project_dir / ".contribution-tracker.json")

    def run_cli(self, *args: str) -> tuple[int, str]:
        output = StringIO()
        with redirect_stdout(output):
            result = main(["--data-file", str(self.data_file), *args])
        return result, output.getvalue()

    def test_add_and_list_entry(self) -> None:
        result, output = self.run_cli(
            "add",
            "--repo",
            "owner/project",
            "--url",
            "https://github.com/owner/project/issues/1",
            "--title",
            "Fix a typo",
        )
        self.assertEqual(result, 0)
        self.assertIn("Added ", output)

        result, output = self.run_cli("list")
        self.assertEqual(result, 0)
        self.assertIn("[planned]  owner/project  Fix a typo", output)

    def test_update_changes_status_and_notes(self) -> None:
        self.run_cli(
            "add",
            "--repo",
            "owner/project",
            "--url",
            "https://github.com/owner/project/issues/1",
            "--title",
            "Fix a typo",
        )
        entry_id = json.loads(self.data_file.read_text(encoding="utf-8"))[0]["id"]

        result, _ = self.run_cli(
            "update", entry_id, "--status", "in-progress", "--notes", "Started"
        )
        self.assertEqual(result, 0)
        entry = json.loads(self.data_file.read_text(encoding="utf-8"))[0]
        self.assertEqual(entry["status"], "in-progress")
        self.assertEqual(entry["notes"], "Started")

    def test_corrupt_data_file_reports_error(self) -> None:
        self.data_file.write_text("{", encoding="utf-8")
        error_output = StringIO()
        with redirect_stdout(StringIO()), redirect_stderr(error_output):
            result = main(["--data-file", str(self.data_file), "list"])

        self.assertEqual(result, 1)
        self.assertIn("Data file is not valid JSON", error_output.getvalue())

    def test_view_writes_html_and_opens_browser(self) -> None:
        self.run_cli(
            "add",
            "--repo",
            "owner/project",
            "--url",
            "https://github.com/owner/project/issues/1",
            "--title",
            "Fix a typo",
        )
        viewer_path = self.data_file.parent / ".contribution-tracker.html"

        with patch("contribution_tracker.cli.webbrowser.open", return_value=True) as open_browser:
            result, output = self.run_cli("view")

        self.assertEqual(result, 0)
        self.assertIn("Opened tracker viewer", output)
        self.assertIn("Fix a typo", viewer_path.read_text(encoding="utf-8"))
        open_browser.assert_called_once_with(viewer_path.resolve().as_uri())

    def test_viewer_escapes_content_and_does_not_link_unsafe_urls(self) -> None:
        page = render_html(
            [
                {
                    "id": "123",
                    "repo": "owner/project",
                    "url": "javascript:alert(1)",
                    "title": "<script>alert(1)</script>",
                    "status": "planned",
                    "notes": "<b>private note</b>",
                }
            ]
        )

        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", page)
        self.assertIn("&lt;b&gt;private note&lt;/b&gt;", page)
        self.assertNotIn('href="javascript:', page)


if __name__ == "__main__":
    unittest.main()

