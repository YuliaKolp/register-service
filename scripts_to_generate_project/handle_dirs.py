import os
import shutil
import time
from pathlib import Path


def safe_remove_dir(
        path,
        max_attempts=3,
        delay=1
        ):
    """Safe dir removing with retries for Windows"""
    path = Path(path)

    if not path.exists():
        return True

    # wait some time to release files
    time.sleep(delay)

    for attempt in range(max_attempts):
        try:
            shutil.rmtree(path)
            print(f"Directory {path} is removed successfully")
            return True
        except PermissionError:
            if attempt < max_attempts - 1:
                print(f"Retry {attempt + 1} fails, another is in  {delay} sec...")
                time.sleep(delay)
                # garbage collection
                import gc
                gc.collect()
            else:
                print(f"Fail to remove dir {path} after {max_attempts} attempts")
                return False
    return False


def move_directory_contents(src, dst):
    """Move contents of src directory to dst, then remove src"""
    print(f"Moving contents from {src} to {dst}")
    cur_script_name = os.path.basename(__file__)

    # Create dst if not exists
    dst = Path(dst)
    dst.mkdir(parents=True, exist_ok=True)

    # Move contents
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        # Skip .git and script files
        if item in ['utils.py', 'generate.py', 'openapi-generator-cli-7.16.0.jar', cur_script_name, '.git', '.venv', '.idea', '__pycache__']:
            print(f'Skipping "{item}"')
            continue

        try:
            # If destination exists, remove it first
            if os.path.exists(dst_path):
                if os.path.isdir(dst_path):
                    shutil.rmtree(dst_path)
                else:
                    os.remove(dst_path)
            # Move the item
            shutil.move(src_path, dst_path)
            print(f"Moved: {item}")
        except Exception as e:
            print(f"Error moving {item}: {e}")

    # Remove source dir
    print("\n" + "=" * 50)
    print("PROJECT GENERATED SUCCESSFULLY!")
    print("=" * 50)
    print(f"\nProject location: {dst}")