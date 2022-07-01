from logging import exception
from tkinter import N
from typing import Type
import DVR3Dinterface.source_p.dvr3dparser as parser
from pathlib import Path
import json
import filecmp
from pytest import raises

tpath = "DVR3Dinterface/tests/testdata/"
cpath="DVR3Dinterface/configs/DVR3DJZ.json"

def test_positive():
    dvrparser = parser.GeneralParser("DVR3Dinterface/configs/DVR3DJZ.json")
    with open (Path("DVR3Dinterface/tests/testdata/positive.json")) as fin:
        jsonfile = json.load(fin)
    dvrparser.write(jsonfile,Path("DVR3Dinterface/tests/testdata/PositiveTest.job"),noAsk=True)
    assert filecmp.cmp("DVR3Dinterface/tests/testdata/PositiveSample.job",
                        "DVR3Dinterface/tests/testdata/PositiveTest.job")

def test_positive_renaming():
    dvrparser = parser.GeneralParser(cpath)
    with open (Path(tpath+"positive.json")) as fin:
        jsonfile = json.load(fin)
    dvrparser.write(jsonfile,Path(tpath+"PositiveTest.job"),noAsk=True)
    assert dvrparser.cpCMDs == ['cp fort.14 Unknown_J2D1.LEV', 'cp fort.26 Unknown_J2D1.WAVE']

def test_positive_renaming_optional():
    dvrparser = parser.GeneralParser(cpath,NAME="TEST",svOp=True)
    with open (Path(tpath+"positive.json")) as fin:
        jsonfile = json.load(fin)
    dvrparser.write(jsonfile,Path(tpath+"PositiveTest.job"),noAsk=True)
    assert dvrparser.cpCMDs == ['cp fort.14 TEST_J2D1.LEV', 'cp fort.26 TEST_J2D1.WAVE', 
                            'cp fort.7 TEST_J2D1.EIGS1', 'cp fort.3 TEST_J2D1.VECS1', 
                            'cp fort.2 TEST_J2D1.EIGS2', 'cp fort.4 TEST_J2D1.VECS2', 
                            'cp fort.24 TEST_J2D1.OUT1', 'cp fort.25 TEST_J2D1.OUT2']


def test_IntToFloat():
    dvrparser = parser.GeneralParser("DVR3Dinterface/configs/DVR3DJZ.json")
    with open (Path("DVR3Dinterface/tests/testdata/IntToFloat.json")) as fin:
        jsonfile = json.load(fin)
    dvrparser.write(jsonfile,Path("DVR3Dinterface/tests/testdata/IntToFLoat.job"),noAsk=True)
    assert filecmp.cmp("DVR3Dinterface/tests/testdata/PositiveSample.job",
                        "DVR3Dinterface/tests/testdata/IntToFLoat.job")

def test_WrongChar():
    dvrparser = parser.GeneralParser("DVR3Dinterface/configs/DVR3DJZ.json")
    with open (Path("DVR3Dinterface/tests/testdata/CharForFloat.json")) as fin:
        jsonfile = json.load(fin)
    with raises(TypeError) as exception:
        dvrparser.write(jsonfile,Path("DVR3Dinterface/tests/testdata/CharForFloat.job"),noAsk=True)

def test_neg_WrongBool():
    dvrparser = parser.GeneralParser(cpath)
    with open (Path(tpath+"n_wrongBool.json")) as fin:
        with raises(json.JSONDecodeError) as exception:
            jsonfile = json.load(fin)

def test_neg_WrongNum():
    dvrparser = parser.GeneralParser(cpath)
    with open (Path(tpath+"n_wrongNum.json")) as fin:
        with raises(json.JSONDecodeError) as exception:
            jsonfile = json.load(fin)

def test_neg_WrongIntPRT():
    # Some parameter in PRT must be int, should fail if other type is given
    dvrparser = parser.GeneralParser(cpath)
    with open (Path(tpath+"n_wrongIntPrt.json")) as fin:
            jsonfile = json.load(fin)
    with raises(TypeError) as exception:
        dvrparser.write(jsonfile,Path("DVR3Dinterface/tests/testdata/n_wrongIntPrt.job"))