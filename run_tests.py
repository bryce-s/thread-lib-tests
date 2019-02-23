

import sys
import os
import subprocess
import re
from sty import fg, bg, ef, rs, RgbFg


def clean():
     completeProcess = subprocess.run("make clean", capture_output=True, text=True, shell=True)
     if completeProcess.returncode != 0:
         print(fg.red + "make clean failed wtf?" + fg.rs)
     else:
         print(fg.green + "Project cleaned!" + fg.rs)

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
            normalized.append(re.search(r'\w+', res).group(0))
        for res in normalized:
            if res == "o" or res == "clean" or res == "all":
                pass
            else:
                makeTargets.append(res)
    clean()
    for target in makeTargets:
       completeProcess = subprocess.run("make " + target, capture_output=True, text=True, shell=True)
       if completeProcess.returncode != 0:
            print(fg.red + "make failed in: " + target)
            print(str(completeProcess.stderr) + fg.rs)
            exit(1)
       else:
            print(fg.green + target + " built!" + fg.rs)
            print(completeProcess.stdout)

    return makeTargets 


def run_test_check_failure_only(testName: str, num_times: int):
    """we just see if it exits with error, here"""
     
def runTest(execTarget: str, verbose: bool, iteration: int):
    """returns 0 if test ran sucessfully, 1 if skip, else >1"""
    runString = "./" + execTarget
    pattern = r'(_exec_only_)(\d+)'
    matchObj = re.search(pattern, execTarget)
    if matchObj:
        completeProcess = None
        try:
            completeProcess = subprocess.run(runString, capture_output=True, timeout=5, text=True, shell=True)
        except subprocess.TimeoutExpired:
            print(fg.red + "A call timed out.. Moving on" + fg.rs)
            return 1
        if completeProcess.returncode == 0:
            return 0
        else:
            print(fg.red + execTarget + " exited with error!")
            print(fg.red + "incorrect output:" + fg.rs)
            print(completeProcess.stdout + completeProcess.stderr)
            return 1
    correctOutput = "tests/output/" + execTarget + "_out_correct"    
    if verbose:    
        print("Calling: " + runString)        
    if os.path.isfile(correctOutput):
        completeProcess = None
        try:
            completeProcess = subprocess.run(runString, capture_output=True, timeout=5, text=True, shell=True)
        except subprocess.TimeoutExpired:
            print(fg.red + "A call timed out.. Moving on" + fg.rs)
            return 1
        with open("tests/output/" + execTarget + "_out_correct") as correctFile:
            correctText = correctFile.read()
            stout = completeProcess.stdout
            stderr = completeProcess.stderr
            if correctText != stout:
                print(fg.red + execTarget + " differs from correct file on i = " + str(iteration))
                print(fg.red + "incorrect output:" + fg.rs)
                print(stout)
                print(fg.da_magenta + "stderr:\n" + stderr + fg.rs)
                print(fg.red + "correct output:" + fg.rs)
                print(correctText)
                print(fg.blue + ">> MOVING ON TO NEXT TEST FILE\n" + fg.rs)
                return 2
            else:
                if verbose:
                    print(fg.green + execTarget + " passed!" + fg.rs)
                return 0
    else:
        print(fg.yellow + "No matching correct file found for " + execTarget + ", skipping" + fg.rs)
        return 1

def runAllTests(executionTargets: list):
    totalTests = 0
    failedCount = 0
    for target in executionTargets:
        pattern = r'(_exec_only_)(\d+)'
        matchObj = re.search(pattern, target)
        if matchObj:
            num_times = matchObj.group(2)
            print(fg.blue + ">> CHECKING TO SEE IF EXITS WITHOUT ERROR ONLY" + fg.rs)
            print("Calling " + target + " " + num_times + " times.")
            for i in range(0, int(num_times)):
                res = runTest(target, True, i)
                if res >= 1:
                    failedCount += 1
                    totalTests += 1
                    break
                totalTests += 1
                if i == int(num_times) - 1:
                    print(fg.green + target + " passed all!" + fg.rs)
                pattern = r'(_exec_only_)(\d+)'
        pattern = r'(_interleave_)(\d+)'
        interleave_matchObj = re.search(pattern, target)
        if interleave_matchObj:
            num_times = interleave_matchObj.group(2)
            
            print(fg.blue + ">> RUNNING AN ARBITARY AMOUNT OF TIMES" + fg.rs)
            print("Calling " + target + " " + num_times + " times.")
            for i in range(0, int(num_times)):
                totalTests += 1
                res = runTest(target, False, i)
                if res == 1 or res > 1:
                    failedCount += 1
                    break
                if i == int(num_times) - 1:
                    print(fg.green + target + " passed." + fg.rs)
        else:
            for i in range(0, 10):
                totalTests += 1
                res = runTest(target, True, i)
                if res == 1 or res > 1:
                    failedCount += 1
                    break
    print("SUMMARY:\nRan " + str(totalTests), "tests, there were " + str(failedCount) + " failures.")


def main():
    """entry point for test program"""
    execStrs = compileProject()
    runAllTests(execStrs)

main()

