from typing import Type
import DVR3Dinterface.source_p.dvr3dparser as parser
from pathlib import Path
import json
import filecmp
from pytest import raises


def test_positive():
    dvrparser = parser.GeneralParser("DVR3Dinterface/configs/DVR3DJZ.json")
    with open (Path("DVR3Dinterface/tests/testdata/positive.json")) as fin:
        jsonfile = json.load(fin)
    dvrparser.write(jsonfile,Path("DVR3Dinterface/tests/testdata/PositiveTest.job"))
    assert filecmp.cmp("DVR3Dinterface/tests/testdata/PositiveSample.job",
                        "DVR3Dinterface/tests/testdata/PositiveTest.job")

def test_IntToFloat():
    dvrparser = parser.GeneralParser("DVR3Dinterface/configs/DVR3DJZ.json")
    with open (Path("DVR3Dinterface/tests/testdata/IntToFloat.json")) as fin:
        jsonfile = json.load(fin)
    dvrparser.write(jsonfile,Path("DVR3Dinterface/tests/testdata/IntToFLoat.job"))
    assert filecmp.cmp("DVR3Dinterface/tests/testdata/PositiveSample.job",
                        "DVR3Dinterface/tests/testdata/IntToFLoat.job")

def test_WrongChar():
    dvrparser = parser.GeneralParser("DVR3Dinterface/configs/DVR3DJZ.json")
    with open (Path("DVR3Dinterface/tests/testdata/CharForFloat.json")) as fin:
        jsonfile = json.load(fin)
    with raises(TypeError) as exception:
        dvrparser.write(jsonfile,Path("DVR3Dinterface/tests/testdata/CharForFloat.job"))