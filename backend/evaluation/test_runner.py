"""
Runs tests to check if the code is 'plausible' (i.e. all tests pass).
For Java, uses Maven; for Python, uses pytest.
If no tests are discovered, it is considered a plausible patch (returns True).
"""

import subprocess
from pathlib import Path


class TestRunner:
    def __init__(self) -> None:
        pass

    # ------------------------------------------------------------------ #
    #  PUBLIC METHOD                                                     #
    # ------------------------------------------------------------------ #
    def run_tests(self, project_path: str, language: str = "python") -> bool:
        """
        Runs test suite depending on the language.

        Returns:
            True  → all tests passed (or no tests exist)
            False → test failures or test runner error
        """
        try:
            language = language.lower()

            if language == "python":
                return self._run_pytest(Path(project_path))

            elif language == "java":
                return self._run_maven(project_path)

            print(f"[TestRunner] Language '{language}' not supported.")
            return False

        except Exception as exc:
            print(f"[TestRunner] Exception while running tests: {exc}")
            return False

    # ------------------------------------------------------------------ #
    #  PRIVATE HELPERS                                                   #
    # ------------------------------------------------------------------ #
    @staticmethod
    def _run_pytest(file_path: Path) -> bool:
        """
        For Python:
        - First collects test items using pytest
        - If no tests found, return True
        - Otherwise, run pytest and return result
        """

        # Step 1: Test discovery
        collect = subprocess.run(
            ["pytest", "--quiet", "--collect-only", str(file_path)],
            capture_output=True,
            text=True,
        )
        if collect.returncode != 0:
            print("[TestRunner] Pytest collection error:\n", collect.stderr.strip())
            return False

        if "collected 0 items" in collect.stdout:
            print("[TestRunner] No pytest tests found – marking as PASS.")
            return True

        # Step 2: Actual test run
        run = subprocess.run(
            ["pytest", "-q", str(file_path)],
            capture_output=True,
            text=True,
        )
        if run.returncode == 0:
            return True

        print("[TestRunner] Pytest test failures:\n", run.stdout or run.stderr)
        return False

    @staticmethod
    def _run_maven(pom_or_dir: str) -> bool:
        """
        For Java:
        - Compile and detect test classes
        - If no test classes found, return True
        - Otherwise, run `mvn test`
        """

        # Step 1: Compile tests
        collect = subprocess.run(
            ["mvn", "-q", "test-compile", "-f", pom_or_dir],
            capture_output=True,
            text=True,
        )
        if collect.returncode != 0:
            print("[TestRunner] Maven test-compile error:\n", collect.stderr.strip())
            return False

        if "No tests to run" in collect.stdout:
            print("[TestRunner] No JUnit tests found – marking as PASS.")
            return True

        # Step 2: Run tests
        run = subprocess.run(
            ["mvn", "-q", "test", "-f", pom_or_dir],
            capture_output=True,
            text=True,
        )
        if run.returncode == 0:
            return True

        print("[TestRunner] Maven test failures:\n", run.stdout or run.stderr)
        return False
