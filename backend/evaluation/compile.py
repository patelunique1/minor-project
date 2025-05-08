"""
Responsible for compiling or checking code syntax. 
For Java, it uses javac; for Python, it checks syntax using `py_compile`.
"""

import subprocess
import os

class Compiler:
    def __init__(self):
        pass

    def compile_code(self, code_path: str, language: str = "python") -> bool:
        """
        Attempt to compile or check syntax of code at `code_path`.
        Returns True if compilation/syntax check succeeds, False otherwise.
        """
        try:
            language = language.lower()

            if language == "java":
                # Compile Java using javac
                if not code_path.endswith(".java"):
                    print("[Compiler] Java file must have .java extension.")
                    return False

                cmd = ["javac", code_path]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode != 0:
                    print(f"[Compiler] Java compile error:\n{result.stderr.strip()}")
                    return False
                return True

            elif language == "python":
                # Check Python syntax
                cmd = ["python", "-m", "py_compile", code_path]
                result = subprocess.run(cmd, capture_output=True, text=True)

                if result.returncode != 0:
                    print(f"[Compiler] Python syntax error:\n{result.stderr.strip()}")
                    return False
                return True

            else:
                print(f"[Compiler] Language '{language}' not supported.")
                return False

        except Exception as e:
            print(f"[Compiler] Exception occurred: {str(e)}")
            return False
