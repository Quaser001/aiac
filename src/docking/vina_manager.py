import os
import sys
import requests
import shutil
import platform
import stat
import subprocess

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CACHE_DIR = os.path.join(BASE_DIR, "data", "docking_cache", "vina")
VINA_EXE = os.path.join(CACHE_DIR, "vina.exe") if platform.system() == "Windows" else os.path.join(CACHE_DIR, "vina")

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def download_vina():
    """Downloads Vina binary from GitHub."""
    ensure_dir(CACHE_DIR)
    
    url = "https://github.com/ccsb-scripps/AutoDock-Vina/releases/download/v1.2.3/vina_1.2.3_windows_x86_64.exe"
    if platform.system() != "Windows":
        # Fallback for Linux
        url = "https://github.com/ccsb-scripps/AutoDock-Vina/releases/download/v1.2.3/vina_1.2.3_linux_x86_64"

    print(f"[Vina] Downloading from {url}...")
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(VINA_EXE, "wb") as f:
                shutil.copyfileobj(response.raw, f)
            
            if platform.system() != "Windows":
                 st = os.stat(VINA_EXE)
                 os.chmod(VINA_EXE, st.st_mode | stat.S_IEXEC)
                 
            print(f"[Vina] Saved to {VINA_EXE}")
            return True
        else:
            print(f"[Vina] Failed to download: {response.status_code}")
            return False
    except Exception as e:
        print(f"[Vina] Download Error: {e}")
        return False

def verify_vina():
    """Runs vina --help to verify binary works."""
    if not os.path.exists(VINA_EXE):
        return False
    
    try:
        result = subprocess.run([VINA_EXE, "--help"], capture_output=True, text=True)
        if "AutoDock Vina" in result.stdout:
            print("[Vina] Verification Successful.")
            return True
        else:
            print("[Vina] Binary exists but produced unexpected output.")
            return False
    except Exception as e:
        print(f"[Vina] Execution Error: {e}")
        return False

def get_vina_path():
    """Ensures Vina is ready and returns path, or None."""
    if not os.path.exists(VINA_EXE):
        success = download_vina()
        if not success:
            return None
    
    # Always verify before returning
    if verify_vina():
        return VINA_EXE
    return None

if __name__ == "__main__":
    # Self-test
    path = get_vina_path()
    print(f"Vina Path: {path}")
