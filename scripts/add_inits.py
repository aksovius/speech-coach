import os

EXCLUDE_DIRS = {
    ".venv",
    "__pycache__",
    "alembic",
    "tests",
    "migrations",
}
for root, dirs, files in os.walk("./src/app"):
    parts = root.split(os.sep)
    if any(part in EXCLUDE_DIRS for part in parts):
        continue
    init_path = os.path.join(root, "__init__.py")
    if "__init__.py" not in files:
        open(init_path, "a").close()

print("All __init__.py files added.")
