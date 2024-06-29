# Create cache directories database
cacheDirectories = [
    # Python
    "__pycache__",
    "venv",
    ".venv",
    # Node.js / Node.js compatible
    "node_modules",
    # [ I hope to add more soon! ]
]
# -- -- -- --

# Import APIs/modules
import os
import shutil
from rich.console import Console  # pip install rich
from rich.progress import Progress

# Create console
console = Console()

# Get required inputs
rootPath = console.input("Path to [bright_white bold]sweep[reset]? ")
if not os.path.isdir(rootPath):
    console.print(f"Path is [bright_red bold]not[reset] a directory")
    quit()

# Create empty paths list
paths: list[str] = []

# Exit if no directories were found
if len(paths) < 1:
    console.print("Discovered [bright_red bold]0[reset] cache directories")
    quit()

# Discover all cache directories
for root, dirs, files in os.walk(rootPath):
    for dir in dirs:
        if dir.lower() in cacheDirectories:
            paths.append(os.path.join(root, dir))

# Display discovered
console.print(
    f"Discovered [bright_yellow bold]{str(len(paths))}[reset] cache directories"
)

if console.input("Do you wish to continue? [Y/n]: ").lower() != "y":
    quit()

with Progress(console=console) as progress:
    # Create the progress bar
    tracker = progress.add_task(
        description=f"Deleting [bright_yellow bold]{str(len(paths))}[reset] directories",
        total=len(paths),
        start=True,
    )

    # Iterate over all cachedirectories
    for path in paths:
        # Run operation in try-block
        try:
            shutil.rmtree(path)

            progress.advance(tracker)

            console.print(f"Deleted [bright_red bold]{path}[reset]")

        # Catch shutil errors
        except shutil.Error:
            console.print(f"Failed to delete [bright_red bold]{path}[reset]")

            progress.advance(tracker)

    progress.remove_task(tracker)  # Dispose the tracker

    console.print(f"Completed [bright_white bold]sweeping[reset]!")
