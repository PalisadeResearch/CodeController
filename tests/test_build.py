"""Exercise bundle packaging without Swift, macOS, or input-device permissions."""

import os
from pathlib import Path
import plistlib
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
RESOURCES = (
    "icon.png",
    "icon.icns",
    "README.md",
    "marked.min.js",
    "readme_template.html",
    "codecontroller_triggers.bttpreset",
)


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="codecontroller-build-")
        self.addCleanup(self.temporary.cleanup)
        self.work = Path(self.temporary.name)
        for name in ("build.sh", "CodeController.swift", *RESOURCES):
            shutil.copyfile(ROOT / name, self.work / name)

        tools = self.work / "tools"
        tools.mkdir()
        compiler = tools / "swiftc"
        compiler.write_text(
            "#!/bin/sh\n"
            "printf '%s\\n' \"$@\" > compiler-args.txt\n"
            "if [ \"${CC_TEST_COMPILER_STATUS:-0}\" != 0 ]; then\n"
            "    exit \"$CC_TEST_COMPILER_STATUS\"\n"
            "fi\n"
            "printf 'compiled fixture\\n' > CodeController\n"
            "chmod +x CodeController\n"
        )
        compiler.chmod(0o755)
        self.environment = {"PATH": str(tools) + os.pathsep + os.defpath}

    def build(self, compiler_status=0):
        return subprocess.run(
            ["bash", "build.sh"],
            cwd=self.work,
            env={**self.environment, "CC_TEST_COMPILER_STATUS": str(compiler_status)},
            capture_output=True,
            text=True,
            timeout=10,
        )

    def test_success_packages_binary_resources_and_plist(self):
        result = self.build()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Built CodeController.app", result.stdout)
        self.assertEqual(
            (self.work / "compiler-args.txt").read_text().splitlines(),
            ["CodeController.swift", "-o", "CodeController"],
        )
        contents = self.work / "CodeController.app/Contents"
        executable = contents / "MacOS/CodeController"
        self.assertEqual(executable.read_text(), "compiled fixture\n")
        self.assertTrue(os.access(executable, os.X_OK))
        for name in RESOURCES:
            self.assertEqual(
                (contents / "Resources" / name).read_bytes(),
                (ROOT / name).read_bytes(),
            )
        with (contents / "Info.plist").open("rb") as source:
            plist = plistlib.load(source)
        self.assertEqual(plist["CFBundleExecutable"], "CodeController")
        self.assertEqual(plist["CFBundleIdentifier"], "com.local.codecontroller")

    def test_failed_compilation_does_not_create_bundle_or_report_success(self):
        result = self.build(compiler_status=23)
        self.assertEqual(result.returncode, 23, result.stdout + result.stderr)
        self.assertNotIn("Built CodeController.app", result.stdout)
        self.assertFalse((self.work / "CodeController.app").exists())

    def test_failed_compilation_does_not_package_stale_executable(self):
        stale = self.work / "CodeController"
        stale.write_bytes(b"stale loose binary")
        bundle = self.work / "CodeController.app"
        (bundle / "Contents/MacOS").mkdir(parents=True)
        previous = bundle / "Contents/MacOS/CodeController"
        previous.write_bytes(b"previous bundle binary")
        result = self.build(compiler_status=23)
        self.assertEqual(result.returncode, 23, result.stdout + result.stderr)
        self.assertNotIn("Built CodeController.app", result.stdout)
        self.assertEqual(stale.read_bytes(), b"stale loose binary")
        self.assertEqual(previous.read_bytes(), b"previous bundle binary")
        self.assertFalse((bundle / "Contents/Info.plist").exists())

    def test_missing_resource_fails_without_reporting_success(self):
        (self.work / "icon.png").unlink()
        result = self.build()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("Built CodeController.app", result.stdout)
        self.assertFalse((self.work / "CodeController.app/Contents/Info.plist").exists())


if __name__ == "__main__":
    unittest.main()
