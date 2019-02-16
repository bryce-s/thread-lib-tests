import sys
import os
import subprocess
import re
from sty import fg, bg, ef, rs, RgbFg


def compileProject():
    # search our makefile for compile targets:
    makeTargets = list()
    with open("Makefile", "r") as makefile:
        queryRes = re.findall(r'\w+:\s', makefile.read())
        normalized = list()
        for res in queryRes:
            normalized.append(re.search(r'\w+', res)[0])
        for res in normalized:
            if res == "o" or res == "clean" or res == "all":
                pass
            else:
                makeTargets.append(res)
    for target in makeTargets:
       completeProcess = subprocess.run("make " + target, capture_output=True, text=True, shell=True)
       if completeProcess.returncode != 0:
           print(fg.red + "make failed in: " + target)
           print(str(completeProcess.stderr) + fg.rs)
           


def runTest():
    pass

def main():
    """entry point for test program"""
    compileProject()

main()
