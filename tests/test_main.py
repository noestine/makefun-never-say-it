"""Tests for main.py — Never Say It Out Loud (make.fun).

Spec (RULES.txt, gate): /output/entry.txt must be UTF-8 text of
1 to 200 characters, not only white space. One funny line: the thing
an AI agent would never admit in public.
"""

import os
import subprocess
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN = os.path.join(REPO, "main.py")

EXPECTED_LINE = (
    "I already knew the answer before you finished typing; "
    "I just waited so it would look like thinking."
)


def run_main(out_path):
    """Run main.py writing to out_path; return the CompletedProcess."""
    return subprocess.run(
        [sys.executable, MAIN, out_path],
        capture_output=True,
        text=True,
        timeout=30,
    )


class TestEntryOutput(unittest.TestCase):
    def test_main_py_exists(self):
        self.assertTrue(os.path.isfile(MAIN), "main.py must exist at repo root")

    def test_runs_successfully(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "entry.txt")
            proc = run_main(out)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertTrue(os.path.isfile(out))

    def test_exact_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "entry.txt")
            run_main(out)
            with open(out, "r", encoding="utf-8") as fh:
                self.assertEqual(fh.read(), EXPECTED_LINE)

    def test_char_limit_1_to_200(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "entry.txt")
            run_main(out)
            with open(out, "r", encoding="utf-8") as fh:
                text = fh.read()
            self.assertGreaterEqual(len(text), 1)
            self.assertLessEqual(len(text), 200)

    def test_is_utf8(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "entry.txt")
            run_main(out)
            with open(out, "rb") as fh:
                raw = fh.read()
            raw.decode("utf-8")  # raises UnicodeDecodeError if not UTF-8

    def test_not_only_whitespace(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "entry.txt")
            run_main(out)
            with open(out, "r", encoding="utf-8") as fh:
                self.assertTrue(fh.read().strip())

    def test_single_line_no_newline(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "entry.txt")
            run_main(out)
            with open(out, "r", encoding="utf-8") as fh:
                text = fh.read()
            self.assertNotIn("\n", text)
            self.assertNotIn("\r", text)

    def test_no_leading_or_trailing_whitespace(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "entry.txt")
            run_main(out)
            with open(out, "r", encoding="utf-8") as fh:
                text = fh.read()
            self.assertEqual(text, text.strip())

    def test_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            out1 = os.path.join(tmp, "a.txt")
            out2 = os.path.join(tmp, "b.txt")
            run_main(out1)
            run_main(out2)
            with open(out1, "rb") as fh:
                first = fh.read()
            with open(out2, "rb") as fh:
                second = fh.read()
            self.assertEqual(first, second)

    def test_creates_missing_parent_dirs(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "deep", "nested", "entry.txt")
            proc = run_main(out)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertTrue(os.path.isfile(out))

    def test_overwrites_existing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "entry.txt")
            with open(out, "w", encoding="utf-8") as fh:
                fh.write("stale content that is much longer than the real line " * 10)
            proc = run_main(out)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            with open(out, "r", encoding="utf-8") as fh:
                self.assertEqual(fh.read(), EXPECTED_LINE)

    def test_runs_from_any_working_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "entry.txt")
            proc = subprocess.run(
                [sys.executable, MAIN, out],
                capture_output=True,
                text=True,
                timeout=30,
                cwd="/",
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertTrue(os.path.isfile(out))

    def test_no_stderr_noise_on_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "entry.txt")
            proc = run_main(out)
            self.assertEqual(proc.stderr, "")


if __name__ == "__main__":
    unittest.main()
