from typing import Type
import DVR3Dinterface.source_p.dvr3dparser as dvrparser
from pathlib import Path
import json
import filecmp
from pytest import raises

testpath = "DVR3Dinterface/tests/txtToJsonData/"

def test_positive():
    dvrparser.txtToJson(testpath+"positive.txt")
    assert filecmp.cmp(testpath+"positiveSample.json",
                        testpath+"positive.txt.json")

def test_positive_comment():
    dvrparser.txtToJson(testpath+"p_comment.txt")
    assert filecmp.cmp(testpath+"positiveSample.json",
                        testpath+"p_comment.txt.json")
