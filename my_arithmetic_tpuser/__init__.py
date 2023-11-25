import subprocess

def get_gitlab_tag():
    return subprocess.check_output(["git", "describe", "--tags"]).decode("utf-8").strip()

__version__ = get_gitlab_tag()