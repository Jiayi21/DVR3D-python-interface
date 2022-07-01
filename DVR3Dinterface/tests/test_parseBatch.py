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
    assert testCII.commands == [['./rot.out <input/temp/tempjob1.job> output1.result', 
                                'cp fort.8 fort.11', 
                                'cp fort.9 fort.12', 
                                './dip.out <input/temp/tempjob2.job> output2.result']]
    assert filecmp.cmp(tempPath+"job1positive.job", tempPath+"tempjob1.job")
    assert filecmp.cmp(tempPath+"job2positive.job", tempPath+"tempjob2.job")
    
def test_positive_pickFileNameArg():
    testCII = CII.CombinedInputInterface(inputPath+"positive.txt")
    assert testCII.PROJECT_NAME=="TEST"
    assert testCII.JROT == 2
    assert testCII.IDIA == 1
