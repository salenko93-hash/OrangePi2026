"""Keep release discovery, server metadata and installer on the same repository."""

from pathlib import Path
import unittest

import github_releases as github

ROOT = Path(__file__).resolve().parents[1]


class RepositoryIdentityTests(unittest.TestCase):
    def test_release_source_is_orangepi2026(self):
        self.assertEqual(github.REPOSITORY, "salenko93-hash/OrangePi2026")
        source = "https://github.com/" + github.REPOSITORY
        for name in ("server/app.py", "INSTALL_RELEASE_ORANGEPI.ps1"):
            with self.subTest(file=name):
                self.assertIn('"' + source + '"', (ROOT / name).read_text(encoding="utf-8"))

    def test_previous_repository_assets_are_rejected(self):
        asset = "/releases/download/v3.7.5/LyceumTV-3.7.5-ORANGEPI-PC.zip"
        accepted = "https://github.com/" + github.REPOSITORY + asset
        self.assertEqual(github.official_asset(accepted), accepted)
        with self.assertRaises(ValueError):
            github.official_asset("https://github.com/salenko93-hash/OrangePi" + asset)
