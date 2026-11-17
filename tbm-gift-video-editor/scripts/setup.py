"""One-time setup for the TBM Gift video editor (Mac or Windows). No Terminal, no Homebrew.

Claude runs:  python3 <skill-dir>/scripts/setup.py      (Windows: py -3.12 <skill-dir>/scripts/setup.py)

Makes ~/.tbm-gift-work/.venv with opencv, numpy, pillow, yt-dlp, openai-whisper and imageio-ffmpeg
(a ready-made ffmpeg with captions support, so nothing needs a password), then runs tbm.py check-setup (must print READY).
"""
import os, shutil, subprocess, sys

WIN = os.name == "nt"
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.expanduser("~/.tbm-gift-work")
V = os.path.join(WORK, ".venv")
VPY = os.path.join(V, "Scripts", "python.exe") if WIN else os.path.join(V, "bin", "python")
BIN = os.path.join(WORK, "bin")

def run(cmd, **kw):
    print("+", " ".join(cmd), flush=True)
    return subprocess.run(cmd, **kw)

def base_python():
    """whisper needs torch, which has wheels for Python 3.10-3.13: prefer one of those"""
    if WIN and shutil.which("py"):
        for v in ["3.12", "3.11", "3.13", "3.10"]:
            if run(["py", f"-{v}", "-c", "pass"], capture_output=True).returncode == 0: return ["py", f"-{v}"]
    for v in ["3.12", "3.11", "3.13", "3.10"]:
        p = shutil.which(f"python{v}")
        if p: return [p]
    return [sys.executable]

def main():
    os.makedirs(BIN, exist_ok=True)
    if not os.path.exists(VPY):
        run(base_python() + ["-m", "venv", V], check=True)
    run([VPY, "-m", "pip", "install", "-q", "--upgrade", "pip"], check=True)
    run([VPY, "-m", "pip", "install", "-q", "opencv-python-headless<5", "numpy", "pillow", "yt-dlp", "openai-whisper", "imageio-ffmpeg"], check=True)
    # use the system ffmpeg if it can burn captions, else the bundled one
    sysff = shutil.which("ffmpeg")
    ok = sysff and " subtitles " in subprocess.run([sysff, "-hide_banner", "-filters"], capture_output=True, text=True).stdout
    if ok:
        fd = os.path.dirname(sysff)
    else:
        exe = subprocess.run([VPY, "-c", "import imageio_ffmpeg as i; print(i.get_ffmpeg_exe())"], capture_output=True, text=True, check=True).stdout.strip()
        dst = os.path.join(BIN, "ffmpeg.exe" if WIN else "ffmpeg")
        shutil.copy(exe, dst); os.chmod(dst, 0o755); fd = BIN
    open(os.path.join(WORK, "ffmpeg_dir.txt"), "w").write(fd)   # tbm.py adds this folder to PATH
    r = run([VPY, os.path.join(D, "scripts", "tbm.py"), "check-setup"])
    sys.exit(r.returncode)

if __name__ == "__main__":
    main()
