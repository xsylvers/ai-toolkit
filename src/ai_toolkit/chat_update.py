import os
import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = PROJECT_ROOT / "src"

print("AI Website Assistant")
print("Type a message to update the site. Type 'exit' to quit.\n")

while True:
    user_input = input("You: ").strip()

    if user_input.lower() == "exit":
        break

    if not user_input:
        continue

    print("\nAI: Updating website...\n")

    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(SRC_PATH) + (os.pathsep + existing if existing else "")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "ai_toolkit.main",
            "update-site",
            user_input,
        ],
        cwd=str(PROJECT_ROOT),
        env=env,
        text=True,
    )

    if result.returncode == 0:
        print("\nAI: Website updated. Refresh the site.\n")
    else:
        print("\nAI: Update failed. Check the error above.\n")