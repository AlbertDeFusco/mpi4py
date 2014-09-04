from mpi4py import MPI
import mpiunittest as unittest

import sys

try:
    import cPickle
except ImportError:
    cPickle = None

try:
    import pickle as pyPickle
except ImportError:
    pyPickle = None

try:
    import dill
except ImportError:
    dill = None

try:
    import marshal
except ImportError:
    marshal = None

try:
    import simplejson
except ImportError:
    simplejson = None

try:
    import json
except ImportError:
    json = None

try:
    import yaml
except ImportError:
    yaml = None

OBJS = [
    None,
    True,
    False,
    7,
    1<<32,
    3.14,
    1+2j,
    'qwerty',
    (0, 1, 2),
    [0, 1, 2],
    {'a':0, 'b':1},
    ]

class TestPickle(unittest.TestCase):

    def setUp(self):
        self.pickle = MPI.pickle

    def tearDown(self):
        self.pickle.__init__()

    def do_pickle(self, obj, pickle):
        comm = MPI.COMM_SELF
        o = comm.sendrecv(obj, 0, 0, None, 0, 0)
        self.assertEqual(obj, o)
        s = pickle.dumps(obj)
        o = pickle.loads(s)
        self.assertEqual(obj, o)

    def testDefault(self):
        pickle = self.pickle
        protocols = [0, 1, 2]
        if sys.version_info[:2] >= (3, 0):
            protocols.append(3)
        if sys.version_info[:2] >= (3, 4):
            protocols.append(4)
        protocols.append(-1)
        protocols.append(None)
        for proto in protocols:
            pickle.__init__(protocol=proto)
            for obj in OBJS:
                self.do_pickle(obj, pickle)
            self.do_pickle(OBJS, pickle)

    if cPickle is not None:
        def testCPickle(self):
            pickle = self.pickle
            dumps = cPickle.dumps
            loads = cPickle.loads
            protocols = [0, 1, 2]
            if sys.version_info[:2] >= (3, 0):
                protocols.append(3)
            if sys.version_info[:2] >= (3, 4):
                protocols.append(4)
            protocols.append(-1)
            protocols.append(None)
            for proto in protocols:
                pickle.__init__(dumps, loads, proto)
                for obj in OBJS:
                    self.do_pickle(obj, pickle)
                self.do_pickle(OBJS, pickle)

    if pyPickle is not None:
        def testPyPickle(self):
            pickle = self.pickle
            dumps = pyPickle.dumps
            loads = pyPickle.loads
            protocols = [0, 1, 2]
            if sys.version_info[:2] >= (3, 0):
                protocols.append(3)
            if sys.version_info[:2] >= (3, 4):
                protocols.append(4)
            protocols.append(-1)
            protocols.append(None)
            for proto in protocols:
                pickle.__init__(dumps, loads, proto)
                for obj in OBJS:
                    self.do_pickle(obj, pickle)
                self.do_pickle(OBJS, pickle)

    if dill is not None:
        def testDill(self):
            pickle = self.pickle
            dumps = dill.dumps
            loads = dill.loads
            protocols = list(range(dill.HIGHEST_PROTOCOL+1))
            protocols.append(-1)
            protocols.append(None)
            for proto in protocols:
                pickle.__init__(dumps, loads, proto)
                for obj in OBJS:
                    self.do_pickle(obj, pickle)
                self.do_pickle(OBJS, pickle)

    if marshal is not None:
        def testMarshal(self):
            pickle = self.pickle
            dumps = marshal.dumps
            loads = marshal.loads
            protocols = [0, 1, 2]
            if sys.version_info[:2] >= (3, 4):
                protocols.append(3)
                protocols.append(4)
            protocols.append(None)
            for protocol in protocols:
                pickle.__init__(dumps, loads, protocol)
                for obj in OBJS:
                    self.do_pickle(obj, pickle)
                self.do_pickle(OBJS, pickle)

    if simplejson is not None:
        def testSimpleJson(self):
            pickle = self.pickle
            dumps = lambda o: simplejson.dumps(o).encode()
            loads = lambda s: simplejson.loads(s.decode())
            pickle.__init__(dumps, loads)
            OBJS2 = [o for o in OBJS
                     if not isinstance(o, (float, complex, tuple))]
            for obj in OBJS2:
                self.do_pickle(obj, pickle)
            self.do_pickle(OBJS2, pickle)

    if json is not None:
        def testJson(self):
            pickle = self.pickle
            dumps = lambda o: json.dumps(o).encode()
            loads = lambda s: json.loads(s.decode())
            pickle.__init__(dumps, loads)
            OBJS2 = [o for o in OBJS
                     if not isinstance(o, (float, complex, tuple))]
            for obj in OBJS2:
                self.do_pickle(obj, pickle)
            self.do_pickle(OBJS2, pickle)

    if yaml is not None:
        def testYAML(self):
            pickle = self.pickle
            dumps = lambda o: yaml.dump(o).encode()
            loads = lambda s: yaml.load(s.decode())
            pickle.__init__(dumps, loads)
            OBJS2 = [o for o in OBJS
                     if not isinstance(o, (complex, tuple))]
            for obj in OBJS2:
                self.do_pickle(obj, pickle)
            self.do_pickle(OBJS2, pickle)


if __name__ == '__main__':
    try:
        unittest.main()
    except SystemExit:
        pass
