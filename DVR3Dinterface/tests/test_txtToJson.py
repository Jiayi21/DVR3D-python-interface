from typing import Type
import DVR3Dinterface.source_p.dvr3dparser as dvrparser
from pathlib import Path
import json
import filecmp
from pytest import raises

testpath = "DVR3Dinterface/tests/txtToJsonData/"

def test_positive():
    filecmp.clear_cache()
    dvrparser.txtToJson(testpath+"positive.txt")
    # Note: Sometimes this compare return False even if files are same
    # If the assertion fails, please check manually
    assert filecmp.cmp(testpath+"positiveSample.json",
                        testpath+"positive.txt.json",shallow=True)

def test_positive_comment():
    dvrparser.txtToJson(testpath+"p_comment.txt")
    # Note: Sometimes this compare return False even if files are same
    # If the assertion fails, please check manually
    assert filecmp.cmp(testpath+"positiveSample.json",
                        testpath+"p_comment.txt.json",shallow=True)
