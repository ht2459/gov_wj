import subprocess
while True:
    p = subprocess.Popen('python main.py', shell=True).wait()
    
    if p != 0:
        continue
    else:
        break