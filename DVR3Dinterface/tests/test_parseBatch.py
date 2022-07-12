from logging import exception
from typing import Type
import DVR3Dinterface.source_p.combinedInputInterface as CII
from pathlib import Path
import json
import filecmp
from pytest import raises
import os

inputPath = "DVR3Dinterface/tests/testparseBatchData/"
tempPath = "DVR3Dinterface/tests/testtemp/"

def test_positive():
    testCII = CII.CombinedInputInterface(inputPath+"positive.txt")
    assert testCII.commands == [['./rot.out <input/temp/tempjob1.job> result_Unknown_JxD1.ROTLEV3', 
                                'cp fort.8 fort.11', 
                                'cp fort.9 fort.12', 
                                './dip.out <input/temp/tempjob2.job> result_TEST_J2D1.DIPOLE3']]
    assert filecmp.cmp(tempPath+"job1positive.job", tempPath+"tempjob1.job")
    assert filecmp.cmp(tempPath+"job2positive.job", tempPath+"tempjob2.job")
    
def test_positive_pickFileNameArg():
    testCII = CII.CombinedInputInterface(inputPath+"positive.txt")
    assert testCII.PROJECT_NAME=="TEST"
    assert testCII.JROT == 2
    assert testCII.IDIA == 1

def test_positive_ChangedFilename():
    testCII = CII.CombinedInputInterface(inputPath+"changedFilename.txt")
    assert testCII.commands == [['./rot.out <input/temp/tempjob1.job> result_Unknown_JxD1.ROTLEV3'], 
                                ['cp fort.8 fort.11', 
                                'cp fort.9 fort.12', 
                                './dip.out <input/temp/tempjob2.job> result_TEST_J2D-2.DIPOLE3']]

def test_positive_missingExe():
    testCII = CII.CombinedInputInterface(inputPath+"p_missingExe.txt")
    # Testing on windows (without Fortran), running fortran will cause RuntimeError for os.system(cmd) will not work
    with raises(RuntimeError) as exception:
        testCII.run()
    # This ensure the error is running commands, not Nothing To Run
    assert "Error code 1 on running: ./rot.out <input/temp/tempjob1.job> result_Unknown_JxD1.ROTLEV3" in str(exception.value)

def test_negative_IllegalLine():
    with raises(IndexError) as exception:
        testCII = CII.CombinedInputInterface(inputPath+"n_wrongLine.txt")

def test_negative_nothingToRun():
    testCII = CII.CombinedInputInterface(inputPath+"n_nothingToRun.txt")
    with raises(RuntimeError) as exception:
        testCII.run()
    assert "No commands to run." in str(exception.value)