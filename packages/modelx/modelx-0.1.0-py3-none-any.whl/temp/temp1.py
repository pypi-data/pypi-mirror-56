import os.path
import pathlib
import modelx as mx
import sys

def foo(x):
    """foo is a function cells."""
    return 3 * x

def testmodel():
    m, s = mx.new_model("TestModel"), mx.new_space(name='TestSpace')
    s.doc = "This is the TestSpace docstring"

    c = s.new_cells(name="lambdacells", formula=lambda x: 2 * x)
    # c._impl._doc = "This is a lambda cells."

    f = s.new_cells(formula=foo)

    # s.m = [m]
    f[0] = 0
    f[1] = m
    c[0] = "123"
    c[s] = 3

    return m



tmp_path = here = os.path.abspath(os.path.dirname(__file__))
os.chdir(here)

def write_model(testmodel):

    path_ = pathlib.Path(tmp_path) / "testdir"
    mx.write_model(testmodel, path_, version=2)

if __name__ == "__main__":
    # m = testmodel()
    # write_model(m)
    m2 = mx.read_model(pathlib.Path(tmp_path) / "testdir", name="t2")
