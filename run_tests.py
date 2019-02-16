import sys
import os
import subprocess
import re


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
            print("make failed in: " + target)
            print(str(completeProcess.stderr))
            exit(1)
       else:
            print(target + " built!")

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
                print(execTarget + " differs from correct file!")
                return 2
            else:
                return 0
    else:
        print("No matching correct file found for " + execTarget + ", skipping")
        return 1

def runAllTests(executionTargets: list):
    totalTests = 0
    failedCount = 0
    for target in executionTargets:
        for i in range(0, 10):
            totalTests += 1
            res = runTest(target)
            if res == 1 or res > 1:
                failedCount += 1
                break
    print("Ran " + totalTests, ", there were " + failedCount + " failures.")


def main():
    """entry point for test program"""
    execStrs = compileProject()
    runAllTests(execStrs)

main()
