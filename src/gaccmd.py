import subprocess
import datetime

def check_diff(path: str) -> bool:
    try:
        subprocess.check_call(["git", "add", "-N", "."], cwd=path)
        diff = subprocess.check_output(["git", "diff", "--shortstat"], cwd=path)
    except subprocess.CalledProcessError:
        raise

    if diff == b'':
        return False
    else:
        return True

def commit_all(path: str, commit_msg=f"Automated commit: {str(datetime.datetime.now())}") -> bool:
    try:
        subprocess.check_call(["git", "add", "."], cwd=path)
        subprocess.check_call(["git", "commit", "-m", commit_msg], cwd=path)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Commit/Staging error: {e}")
        return False
