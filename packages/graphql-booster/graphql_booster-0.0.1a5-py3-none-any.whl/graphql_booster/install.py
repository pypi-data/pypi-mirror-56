import os
import subprocess


def setup_gateway():
    gateway_path = os.path.join(os.path.dirname(__file__), "gateway")
    print(gateway_path)
    subprocess.run("nodeenv -p".split())
    subprocess.run("npm install", cwd=gateway_path, shell=True)
