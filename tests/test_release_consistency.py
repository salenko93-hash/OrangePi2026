"""Release metadata contracts without importing app or touching runtime data."""

import ast
from contextlib import redirect_stdout
import io
from pathlib import Path
import re
import runpy
import types
import unittest
from unittest.mock import MagicMock

ROOT = Path(__file__).resolve().parents[1]
VERSION = runpy.run_path(str(ROOT / "server/version.py"))["VERSION"]


class ReleaseConsistencyTests(unittest.TestCase):
    def test_startup_event_and_console_follow_version_source(self):
        tree = ast.parse((ROOT / "server/app.py").read_text(encoding="utf-8"))
        main = next(
            node for node in tree.body
            if isinstance(node, ast.FunctionDef) and node.name == "main"
        )
        code = compile(ast.Module(body=[main], type_ignores=[]), "app.main", "exec")
        # A changed version must propagate too, without importing app's globals.
        for version in (VERSION, "99.8.7"):
            with self.subTest(version=version):
                event = MagicMock()
                server = MagicMock()
                namespace = {
                    "VERSION": version,
                    "CONFIG": types.SimpleNamespace(load=lambda: {"port": 8765}),
                    "write_event": event,
                    "TELEGRAM": MagicMock(),
                    "ENGINE": MagicMock(),
                    "_OPS_MONITOR_STOP": MagicMock(),
                    "_ops_monitor_loop": MagicMock(),
                    "threading": MagicMock(),
                    "signal": MagicMock(),
                    "BoundedHTTPServer": MagicMock(return_value=server),
                    "Handler": object(),
                }
                exec(code, namespace)
                with redirect_stdout(io.StringIO()) as output:
                    namespace["main"]()
                event.assert_called_once_with(
                    "service.start",
                    f"LyceumTV {version} Smart Information Display запущено",
                    {"host": "127.0.0.1", "port": 8765},
                )
                self.assertEqual(
                    output.getvalue().strip(),
                    f"LyceumTV {version} Smart Information Display "
                    "listening on http://127.0.0.1:8765",
                )

    def test_current_documentation_matches_runtime_version(self):
        for name in ("README.md", "CHANGELOG.md"):
            with self.subTest(file=name):
                heading = (ROOT / name).read_text(encoding="utf-8").splitlines()[0]
                self.assertEqual(
                    re.search(r"\d+\.\d+\.\d+(?:-rc\.\d+)?", heading)[0], VERSION
                )

    def test_readme_has_no_stale_release_links(self):
        source = (ROOT / "README.md").read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)]+)\)", source):
            with self.subTest(target=target):
                if target.startswith("https://"):
                    for version in re.findall(r"\d+\.\d+\.\d+(?:-rc\.\d+)?", target):
                        self.assertEqual(version, VERSION)
                else:
                    self.assertTrue((ROOT / target.split("#", 1)[0]).is_file(), target)

    def test_docs_do_not_promise_tls_renewal_by_reinstalling(self):
        source = (ROOT / "docs/INSTALL_ORANGEPI.md").read_text(encoding="utf-8")
        self.assertNotIn("повторний повний установник оновлює його", source)
        self.assertIn("Транзакційне оновлення застосунку не поновлює TLS", source)

    def test_operator_instructions_do_not_pin_an_unconfirmed_release(self):
        for name in (
            "README.md", "docs/INSTALL_ORANGEPI.md", "docs/GITHUB_RELEASE_UPDATES.md"
        ):
            with self.subTest(file=name):
                source = (ROOT / name).read_text(encoding="utf-8")
                self.assertNotRegex(source, r"(?:-Tag|--tag)\s+v?\d+\.\d+\.\d+")
                self.assertNotRegex(source, r"https://\S+/download-\d+\.\d+\.\d+")
                self.assertNotRegex(source, r"повний установник \d+\.\d+\.\d+")


if __name__ == "__main__":
    unittest.main()
