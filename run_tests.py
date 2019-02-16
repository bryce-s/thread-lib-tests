import sys
import os
import subprocess
import re
from sty import fg, bg, ef, rs, RgbFg


def compileProject():
    # search our makefile for compile targets. Return execution targets.
    executionTargets = list()
    makeTargets = list()
    with open("Makefile", "r") as makefile:
        mf_str = makefile.read()
        executionTargets = re.findall(r'-o\s\w+', mf_str)
        queryRes = re.findall(r'\w+:\s', mf_str)
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
            exit(1)
       else:
            print(fg.green + target + " built!" + fg.rs)

    return executionTargets


def runTest(execTarget: str):
    """returns 0 if test ran sucessfully, 1 if skip, else >1"""
    runString = "./" + execTarget
    print("Calling: " + runString)
    correctOutput = "tests/output/" + execTarget + "_out_correct"
    if os.path.isfile(correctOutput):
        completeProcess = subprocess.run(runTest, capture_output=True, text=True, shell=True)
        with open("tests/output/" + execTarget + "_out_correct") as correctFile:
            correctText = correctFile.read()
            if correctText != completeProcess.stdout:
                print(fg.red + execTarget + " differs from correct file!" + fg.rs)
                return 2
            else:
                return 0
    else:
        print(fg.yellow + "No matching correct file found for " + execTarget + ", skipping" + fg.rs)
        return 1

def runAllTests(executionTargets: list):
    for target in executionTargets:
        for i in range(0, 10):
            res = runTest(target)
            if res == 1 or res > 1:
                break



def main():
    """entry point for test program"""
    compileProject()

main()
