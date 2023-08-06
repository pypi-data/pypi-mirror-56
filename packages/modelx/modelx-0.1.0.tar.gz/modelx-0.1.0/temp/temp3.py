import modelx as mx
import os.path
import pathlib
import pickle

# m, s = mx.new_model("TestIF"), mx.new_space("ThisSpace")
#
#
# @mx.defcells
# def foo(x):
#     return foo(x - 1) + 1 if x > 0 else 1
#
#
# s2 = m.new_space("OtherSpace")
#
# iflist = [s, s2, foo]
# m.iflist = iflist
# s.iflist2 = iflist


tmp_path = here = os.path.abspath(os.path.dirname(__file__))
os.chdir(here)

path_ = pathlib.Path(tmp_path) / "testdir"
# # mx.write_model(m, path_, version=2)
m2 = mx.read_model(path_)