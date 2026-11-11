from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
for name in ["01_clean.py", "02_visualize.py", "03_train.py",
             "04_classify.py"]:
    print("Po ekzekutohet:", name, flush=True)
    subprocess.run([sys.executable, str(root / name)], cwd=root, check=True)
print("Perfundoi. Hap aplikacionin me: python app.py")
