__all__ = ['GraphType', 'Mode', 'Inference', 'Sampler', 'StatisticsType']

import ctypes
import time
import numpy
import itertools
import struct
from sys import platform
from .functions import *

class Colors:
	INIT  = '\033[11m'
	TRAIN = '\033[10m'
	OTHER = '\033[94m'
	ENDC  = '\033[0m'
	BOLD  = '\033[1m'
	UNDERLINE = '\033[4m'

from pathlib import Path
path = Path(__file__)

if platform == "linux" or platform == "linux2":
	pxpath = str(path.parent / "lib/libpx.so")
elif platform == "darwin":
#	pxpath = path.parent / "lib/libpx.dylib"
	raise TypeError('macOS will be supported soon!')
elif platform == "win32":
	pxpath = str(path.parent / "lib/libpx.dll")

example_model_filename = str(path.parent / "data/5_14.mod")
example_data_filename  = str(path.parent / "data/sin44")

class disc_t(ctypes.Structure):
	_fields_ = [("num_intervals", ctypes.c_uint64), ("num_moments", ctypes.c_uint64), ("_intervals", ctypes.POINTER(ctypes.c_double)), ("_moments", ctypes.POINTER(ctypes.c_double))]

	@property
	def intervals(self):
		return numpy.ctypeslib.as_array(self._intervals, shape = (self.num_intervals, 2))

	@property
	def moments(self):
		return numpy.ctypeslib.as_array(self._moments, shape = (self.num_moments, 4))

lib = ctypes.cdll.LoadLibrary(pxpath)

lib.create_ctx.restype = ctypes.c_uint64

lib.version.restype = ctypes.c_uint64

lib.ctx_set_code.restype = ctypes.c_bool

lib.discretize.restype = disc_t
lib.discretize.argtypes = [ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64]

lib.reset_ctx.restype  = ctypes.c_bool
lib.reset_ctx.argtypes = [ctypes.c_uint64]

lib.run_ctx.restype  = ctypes.c_bool
lib.run_ctx.argtypes = [ctypes.c_uint64]

lib.ctx_write_reg.restype  = ctypes.c_bool
lib.ctx_write_reg.argtypes = [ctypes.c_uint64, ctypes.c_char_p, ctypes.c_uint64]

lib.ctx_read_reg.restype  = ctypes.c_uint64
lib.ctx_read_reg.argtypes = [ctypes.c_uint64, ctypes.c_char_p]

MISSING_VALUE = 65535

class Graph(ctypes.Structure):
	_fields_ = [("__unused", ctypes.c_uint64), ("itype", ctypes.c_uint8), ("nodes", ctypes.c_uint64), ("edges", ctypes.c_uint64), ("A", ctypes.POINTER(ctypes.c_uint64))]

	@property
	def edgelist(self):
		res = numpy.ctypeslib.as_array(self.A, shape = (self.edges, 2))
		res.flags.writeable = False
		return res

class STGraph(ctypes.Structure):
	_fields_ = [("__unused", ctypes.c_uint64), ("itype", ctypes.c_uint8), ("T", ctypes.c_uint64), ("base", ctypes.POINTER(Graph)), ("Tm1inv", ctypes.c_float)]

	@property
	def nodes(self):
		H = self.base.contents
		return H.nodes * self.T

	@property
	def edges(self):
		H = self.base.contents
		return H.edges * self.T + (self.T-1) * ( H.nodes + 2 * H.edges )

	@property
	def edgelist(self):
		if not hasattr(self, 'E'):
			self.E = numpy.zeros((self.edges, 2), dtype = numpy.uint64)
			H = self.base.contents

			for v in range(H.nodes):
				for t in range(self.T-1):
					e = v * (self.T-1) + t
					self.E[e][0] = t * H.nodes + v
					self.E[e][1] = (t + 1) * H.nodes + v

			for f in range(H.edges):
				a = H.edgelist[f][0]
				b = H.edgelist[f][1]
				for t in range(self.T-1):
					e = (self.T-1) * H.nodes + f * 3 * (self.T-1) + t * 3
					self.E[e + 0][0] = t * H.nodes + a
					self.E[e + 0][1] = t * H.nodes + b
					self.E[e + 1][0] = t * H.nodes + a
					self.E[e + 1][1] = (t + 1) * H.nodes + b
					self.E[e + 2][0] = (t + 1) * H.nodes + a
					self.E[e + 2][1] = t * H.nodes + b

				e = (self.T-1) * H.nodes + (self.T-1) * 3 * H.edges + f
				self.E[e][0] = (self.T-1) * H.nodes + a
				self.E[e][1] = (self.T-1) * H.nodes + b

			self.E.flags.writeable = False

		return self.E

	def spatial_vertex(self, v):
		H = self.base.contents
		return v % H.nodes

	def time(self, v):
		H = self.base.contents
		return (v-self.spatial_vertex(v)) / H.nodes

	def is_spatial_edge(self, e):
		return self.time(self.edgelist[e][0]) == self.time(self.edgelist[e][1])

class Model(ctypes.Structure):
	"""
	Parameters
	----------
	weights : :class:`numpy.ndarray`
		Model weights
	graph : :py:class:`Graph`
		Undirected graph, representing the conditional independence structure
	states : Integer or 1-dimensional :class:`numpy.ndarray` of length at least :any:`graph.nodes`
		Vertex statespace sizes. Desired output data-type.
	stats : :class:`StatisticsType`, optional
		Determines wether the model's sufficient statistic is minimal or overcomplete (default). 
		For now, setting stats=StatisticsType.minimal requires states=2. 

	See Also
	--------
	:meth:`pxpy.train`, :meth:`pxpy.load_model`, :class:`StatisticsType`
	
	Notes
	-----
	The number of variables in the model is determinded by the number of nodes
	in the :any:`graph` (:any:`graph.nodes`). Each variables's statespace size is controlled 
	via :any:`states`. If :any:`states` is an integer, all variables will have state spaces
	of that size. In case :any:`states` is a numpy.ndarray, statespace sizes for each variable
	are read from that array. This requires the user to manually set all the values in the array. 
	
	Examples
	--------
	>>> import pxpy as px
	>>> import numpy as np
	>>> E = np.array([0, 1], dtype = np.uint64).reshape(1, 2) # an edgelist with a single edge
	>>> G = px.custom_graph(E)
	>>> w = np.array([0.5, 0.6, 0.6, -0.3]) # edge weight vector (for an overcomplete model)
	>>> P = px.Model(w, 2, G, stats = StatisticsType.overcomplete)
	>>> P.predict()
	"""
	_fields_ = [("itype", ctypes.c_uint8), ("vtype", ctypes.c_uint8), ("from_file", ctypes.c_bool), ("G", ctypes.c_uint64), ("H", ctypes.c_uint64), ("w", ctypes.POINTER(ctypes.c_double)), ("empirical_stats", ctypes.POINTER(ctypes.c_double)), ("Y", ctypes.POINTER(ctypes.c_uint64)), ("Ynames", ctypes.POINTER(ctypes.c_uint64)), ("Xnames", ctypes.POINTER(ctypes.c_uint64)), ("dimension", ctypes.c_uint64), ("gtype", ctypes.c_uint64), ("T", ctypes.c_uint64), ("reparam", ctypes.c_uint64), ("K", ctypes.c_uint64), ("num_instances", ctypes.c_uint64), ("llist", ctypes.c_uint64), ("clist", ctypes.c_uint64)]

	__A         = None
	__observed  = None
	__marginals = None

	def __init__(self):
		self.woff = []
		self.__A         = None
		self.__observed  = None
		self.__marginals = None

	def __init__(self, weights, graph, states, stats = StatisticsType.overcomplete):
		if not isinstance(graph, Graph):
			raise TypeError('graph must be an instance of Graph')

		if not isinstance(weights, numpy.ndarray) or weights.dtype != numpy.float64:
			raise TypeError('weights must be of type numpy.ndarray with dtype float64')

		if not (isinstance(states, numpy.ndarray) and weights.dtype == numpy.uint64) and not isinstance(states, int):
			raise TypeError('states must be an int, or of type numpy.ndarray with dtype uint64')

		if isinstance(states, numpy.ndarray) and len(states) < graph.nodes:
			raise TypeError('states must contain one statespace size for each variable in the model')

		if not isinstance(stats, StatisticsType):
			raise TypeError('model must have either covercomplete or minimal sufficient statistics')

		if stats == StatisticsType.minimal and states != 2:
			raise TypeError('for now, models with minimal sufficient statistics and more that 2 states per variable are not supported')

		self.itype = 3
		self.vtype = 5
		self.from_file = False
		self.G = ctypes.addressof(graph)
		self.H = 0

		if isinstance(states, numpy.ndarray):
			self.Y = ctypes.cast(states.ctypes.data, ctypes.POINTER(ctypes.c_uint64))
		else:
			temp = states * numpy.ones(graph.nodes, dtype = numpy.uint64)
			self.Y = ctypes.cast(temp.ctypes.data, ctypes.POINTER(ctypes.c_uint64))

		self.Ynames = None
		self.Xnames = None

		S = numpy.ctypeslib.as_array(self.Y, shape = (graph.nodes, ))
		d = 0
		for e in range(graph.edges):
			d += S[graph.edgelist[e][0]] * S[graph.edgelist[e][1]]
		self.dimension = int(d)

		if stats == StatisticsType.minimal:
			self.reparam = 12
		else:
			self.reparam = 0

		if len(weights) < d:
			weights.resize(int(d), refcheck = False)
		self.w = ctypes.cast(weights.ctypes.data, ctypes.POINTER(ctypes.c_double))
		self.empirical_stats = None
		self.gtype = int(GraphType.other)
		self.T = 1
		self.K = 0
		self.num_instances = 1
		self.llist = 0
		self.clist = 0

		self.__A         = None
		self.__observed  = None
		self.__marginals = None

		self.prepare()

	def set_ctx_state(self):
		write_register("MPT", ctypes.addressof(self))
		write_register("GPT", ctypes.addressof(self.graph))
		write_register("REP", self.reparam)
		write_register("GRA", self.gtype)

	def prepare(self):
		offset = 0
		self.obj = 0
		self.woff = []
		for e in range(self.graph.edges):
			L = self.states[self.graph.edgelist[e][0]] * self.states[self.graph.edgelist[e][1]]
			self.woff.append(offset)
			offset = offset + L
		self.woff.append(offset)

	@property
	def dim(self):
		if self.reparam == 12:
			return self.graph.nodes + self.graph.edges
		else:
			return self.dimension

	@property
	def time_frames(self):
		return self.T

	@property
	def weights(self):
		if self.vtype == 3:
			return numpy.ctypeslib.as_array(self.w, shape = (self.dim, )).view('uint64')
		else:
			return numpy.ctypeslib.as_array(self.w, shape = (self.dim, ))

	def slice_edge(self, e, A):
		if self.reparam == 12:
			raise TypeError('Edge slicing is only supported for overcomplete models')

		if not isinstance(A, numpy.ndarray):
			raise TypeError('A must be of type numpy.ndarray')

		if len(A) != self.dim:
			raise TypeError('A must be ' + str(self.dim) + ' dimensional')

		return A[int(self.woff[e]):int(self.woff[e + 1])]

	def slice_edge_state(self, e, x, y, A):
		w = self.slice_edge(e, A)

		s = self.graph.edgelist[e][0]
		t = self.graph.edgelist[e][1]

		idx = int(x * self.states[t] + y)

		return w[idx:(idx + 1)]

	@property
	def statistics(self):
		if self.empirical_stats is None:
			return None
		res = 0
		if self.vtype == 3:
			res = numpy.ctypeslib.as_array(self.empirical_stats, shape = (self.dimension, )).view('uint64') / self.num_instances
		else:
			res = numpy.ctypeslib.as_array(self.empirical_stats, shape = (self.dimension, )) / self.num_instances
		res.flags.writeable = False
		return res

	def phi(self, x):
		if not isinstance(x, numpy.ndarray):
			raise TypeError('x must be of type numpy.ndarray')

		if len(x) != self.graph.nodes:
			raise TypeError('x must be ' + str(self.graph.nodes) + ' dimensional')

		phi_x = numpy.zeros(shape = (self.dim, ))

		if self.reparam == 12:
			for v in range(self.graph.nodes):
				if x[v] >= self.states[v]:
					TypeError('Some values of x exceed the state space')

				phi_x[v] = int(x[v])

			for e in range(self.graph.edges):

				s = self.graph.edgelist[e][0]
				t = self.graph.edgelist[e][1]

				if x[s] >= self.states[s] or x[t] >= self.states[t]:
					TypeError('Some values of x exceed the state space')

				phi_x[int(self.graph.nodes + e)] = int(x[s] * x[v])
		else:
			for e in range(self.graph.edges):

				s = self.graph.edgelist[e][0]
				t = self.graph.edgelist[e][1]

				if x[s] >= self.states[s] or x[t] >= self.states[t]:
					TypeError('Some values of x exceed the state space')

				idx = int(self.woff[e] + x[s] * self.states[t] + x[t])

				phi_x[idx] = 1

		return phi_x

	def score(self, x):
		return numpy.inner(self.weights, self.phi(x))

	def edge_statespace(self, e):
		Xs = self.states[self.graph.edgelist[e][0]]
		Xt = self.states[self.graph.edgelist[e][1]]
		return numpy.array(list(itertools.product(range(Xs), range(Xt))))

	def save(self, filename):
		self.set_ctx_state()
		write_register("OVW", 1)
		L = []
		L.append("MFN \"" + filename + "\";")
		L.append("STORE MPT;")
		recode(L)
		run()

	def predict(self, observed = None, generic_progress_hook = 0, iterations = 100):
		if observed is not None:
			if not isinstance(observed, numpy.ndarray):
				raise TypeError('observed must be of type numpy.ndarray')
			if len(observed.shape) == 1:
				observed = observed.reshape(1, len(observed))
			if len(observed.shape) != 2:
				raise ValueError('observed must be 1 or 2 dimensional')

		self.set_ctx_state()

		data_ptr = ctypes.c_uint64(observed.ctypes.data)

		if generic_progress_hook != 0:
			f3 = prg_func(generic_progress_hook)
			write_register("CBP", ctypes.c_uint64.from_buffer(f3).value)
		else:
			write_register("CBP", 0)

		write_register("PGX", 0)
		write_register("MIL", iterations)
		write_register("INF", int(Inference.belief_propagation))

		L = []
		L.append("EDP " + str(data_ptr.value) + ";")
		L.append("NXX " + str(len(observed)) + ";")
		L.append("GPX " + str(len(observed) * len(observed[0]) * 2) + ";")
		L.append("LDX DPT;")
		L.append("PREDICT;")
		
		recode(L)
		run()

		return observed

	def MAP(self):
		x = numpy.full(shape = (1, self.graph.nodes), fill_value = MISSING_VALUE, dtype = numpy.uint16)
		self.predict(x)
		return x

	def sample(self, observed = None, num_samples = None, sampler = Sampler.apx_perturb_and_map, generic_progress_hook = 0, iterations = 100, perturbation = 0.1, burn = 100):
		if not isinstance(sampler, Sampler):
			raise TypeError('sampler must be an instance of Sampler Enum')

		if not ((observed is None) != (num_samples is None)):
			raise ValueError('either observed or num_samples must be set (and not both)')

		if observed is not None:
			if not isinstance(observed, numpy.ndarray):
				raise TypeError('observed must be of type numpy.ndarray')
			if len(observed.shape) == 1:
				observed = observed.reshape(1, len(observed))
			if len(observed.shape) != 2:
				raise ValueError('observed must be 1 or 2 dimensional')

		L = []

		if observed is None:
			observed = numpy.full(shape = (num_samples, self.graph.nodes), fill_value = MISSING_VALUE, dtype = numpy.uint16)

		self.set_ctx_state()

		data_ptr = ctypes.c_uint64(observed.ctypes.data)

		L = []
		L.append("EDP " + str(data_ptr.value) + ";")
		L.append("NXX " + str(len(observed)) + ";")
		L.append("GPX " + str(len(observed) * len(observed[0]) * 2) + ";")

		if generic_progress_hook != 0:
			f3 = prg_func(generic_progress_hook)
			write_register("CBP", ctypes.c_uint64.from_buffer(f3).value)
		else:
			write_register("CBP", 0)

		if sampler == Sampler.apx_perturb_and_map:
			write_register("PAM", integer_from_float(perturbation))
			write_register("MIL", iterations)
			write_register("INF", int(Inference.belief_propagation))

		elif sampler == Sampler.gibbs:
			write_register("PAM", 0)
			write_register("GRE", burn) # unified burn-in and resamplings between two samples
#			write_register("GBR", burn)
#			write_register("GRE", resamplings)

		L.append("LDX DPT;")
		L.append("SAMPLE;")
		recode(L)
		run()

		return numpy.array(observed)

	@property
	def graph(self):
		if not hasattr(self, 'LOCAL_G'):
			if self.gtype == 11:
				self.LOCAL_G = ctypes.cast(self.G, ctypes.POINTER(STGraph)).contents
			else:
				self.LOCAL_G = ctypes.cast(self.G, ctypes.POINTER(Graph)).contents
		return self.LOCAL_G


	@property
	def states(self):
		res = numpy.ctypeslib.as_array(self.Y, shape = (self.graph.nodes, ))
		return res


	def p(self, v, x, observed = None, inference = Inference.belief_propagation, iterations = 100, k = 3):
		if observed is not None:
			if not isinstance(observed, numpy.ndarray):
				raise TypeError('observed must be of type numpy.ndarray')
			if len(observed.shape) == 1:
				observed = observed.reshape(1, len(observed))
			if len(observed.shape) != 2:
				raise ValueError('observed must be 1 or 2 dimensional')

		if not (observed == self.__observed and self.__marginals is not None and self.__A is not None):
			self.infer(observed = observed, inference = inference, iterations = iterations, k = k)

		ii = numpy.where(self.graph.edgelist == v)
		e = ii[0][0]

		idx = 0
		if self.graph.edgelist[e][1] == v:
			idx = 1

		P = self.slice_edge(e, self.__marginals)
		X = self.edge_statespace(e)

		return numpy.sum(P, where = X[:,idx] == x)

	def infer(self, observed = None, inference = Inference.belief_propagation, iterations = 100, k = 3):
		if not isinstance(inference, Inference):
			raise TypeError('inference must be an instance of Inference Enum')

		if observed is not None and not isinstance(observed, numpy.ndarray):
			raise TypeError('observed must be of type numpy.ndarray')

		L = []

		if observed is not None:
			data_ptr = ctypes.c_uint64(observed.ctypes.data)
			L.append("EDP " + str(data_ptr.value) + ";")
			L.append("NXX " + str(len(observed)) + ";")
			L.append("GPX " + str(len(observed) * len(observed[0]) * 2) + ";")
			L.append("LDX DPT;")
		else:
			write_register("DPT", 0)

		self.set_ctx_state()

		write_register("KXX", k)
		write_register("MIL", iterations)
		write_register("INF", int(inference))

		L.append("INFER;")
		recode(L)
		run()

		P = ctypes.cast(int(read_register("PPT")), ctypes.POINTER(ctypes.c_double))

		res = numpy.array(numpy.ctypeslib.as_array(P, shape = (self.dimension, )))
		#res.flags.writeable = False

		self.__observed  = observed
		self.__marginals = res
		self.__A         = float_from_integer(read_register("LNZ"))

		return self.__marginals, self.__A

	@property
	def addr(self):
		return self


class progress_t(ctypes.Structure):
	_fields_ = [("_obj", ctypes.c_double), ("stepsize", ctypes.c_double), ("lam", ctypes.c_double), ("iteration", ctypes.c_uint64), ("max_iterations", ctypes.c_uint64), ("dim", ctypes.c_uint64), ("_w", ctypes.POINTER(ctypes.c_double)), ("_g", ctypes.POINTER(ctypes.c_double)), ("_e", ctypes.POINTER(ctypes.c_double)), ("is_int", ctypes.c_bool), ("_best_obj", ctypes.c_double), ("_best_w", ctypes.POINTER(ctypes.c_double)), ("value_bytes", ctypes.c_uint64), ("_model", ctypes.POINTER(Model))]

	@property
	def obj(self):
		if self.is_int != 0:
			return self._best_obj / 255.0
		else:
			return self._best_obj

	@property
	def model(self):
		mod = self._model.contents
		mod.prepare()
		mod.obj = self.obj
		return mod

	@property
	def weights(self):
		if self.is_int != 0:
			return numpy.ctypeslib.as_array(self._w, shape = (self.dim, )).view('uint64')
		else:
			return numpy.ctypeslib.as_array(self._w, shape = (self.dim, ))

	@property
	def weights_extrapolation(self):
		if self.is_int != 0:
			return numpy.ctypeslib.as_array(self._e, shape = (self.dim, )).view('uint64')
		else:
			return numpy.ctypeslib.as_array(self._e, shape = (self.dim, ))

	@property
	def best_weights(self):
		if self.is_int != 0:
			return numpy.ctypeslib.as_array(self._best_w, shape = (self.dim, )).view('uint64')
		else:
			return numpy.ctypeslib.as_array(self._best_w, shape = (self.dim, ))

	@property
	def gradient(self):
		if self.is_int != 0:
			return numpy.ctypeslib.as_array(self._g, shape = (self.dim, )).view('uint64')
		else:
			return numpy.ctypeslib.as_array(self._g, shape = (self.dim, ))

if platform == "win32":
	opt_func = ctypes.WINFUNCTYPE(None, ctypes.POINTER(progress_t))
	prg_func = ctypes.WINFUNCTYPE(None, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_char_p)
else:
	opt_func = ctypes.CFUNCTYPE(None, ctypes.POINTER(progress_t))
	prg_func = ctypes.CFUNCTYPE(None, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_char_p)


ctx = ctypes.c_uint64(lib.create_ctx())

def write_register(name, val):
	l = len(name)
	buff = ctypes.create_string_buffer(l + 1)
	buff.value = name.encode('utf-8')
	ptr = (ctypes.c_char_p)(ctypes.addressof(buff))
	return lib.ctx_write_reg(ctx, ptr, val)

write_register("SEED", int(round(time.time() * 1000)))

def version():
	return lib.version()

def discretize(data, num_states, targets = None):
	if not isinstance(data, numpy.ndarray):
		raise TypeError('data must be of type numpy.ndarray')

	R = numpy.zeros(shape = (len(data), len(data[0])), dtype = numpy.uint16)
	M = []

	if targets == None:
		t = range(len(data[0]))
	else:
		t = targets

	for col in t:
		col_data = numpy.ascontiguousarray(data[:, col])
		distinct = len(numpy.unique(col_data))
		if distinct > num_states:
			result = numpy.zeros(shape = (len(data), ), dtype = numpy.uint16)
			disc_info = lib.discretize(ctypes.c_uint64(result.ctypes.data), ctypes.c_uint64(col_data.ctypes.data), ctypes.c_uint64(len(data)), ctypes.c_uint64(num_states))
			M.append(disc_info)
			R[:, col] = result
		else:
			M.append(None)
			R[:, col] = col_data
	return R, M

def undiscretize(data, M):
	if not isinstance(data, numpy.ndarray):
		raise TypeError('data must be of type numpy.ndarray')

	R = numpy.zeros(shape = (len(data), len(data[0])))

	with numpy.nditer(data, flags = ['multi_index']) as it:
		while not it.finished:
			row = it.multi_index[0]
			col = it.multi_index[1]
			R[row, col] = M[col].moments[it[0]][0]
			it.iternext()
	return R

def run():
	if ctx is None:
		assert False
	lib.run_ctx(ctx)

def read_register(name):
	l = len(name)
	buff = ctypes.create_string_buffer(l + 1)
	buff.value = name.encode('utf-8')
	ptr = (ctypes.c_char_p)(ctypes.addressof(buff))
	return lib.ctx_read_reg(ctx, ptr)

def recode(code):
	n = len(code)
	l = 0
	for stmt in code:
		if len(stmt) > l:
			l = len(stmt)
	buffs = [ctypes.create_string_buffer(l + 1) for i in range(len(code))]
	for index, stmt in enumerate(code):
		buffs[index].value = code[index].encode('utf-8')
	ptrs = (ctypes.c_char_p * n)( * map(ctypes.addressof, buffs))
	lib.ctx_set_code(ctx, ptrs, n)
	return n

def set_seed(s):
	write_register("SEED", s)

def float_from_integer(val):
	return struct.unpack('d', struct.pack('N', val))[0]

def integer_from_float(val):
	return struct.unpack('N', struct.pack('d', val))[0]

def KL(p, q):
	if not isinstance(p, numpy.ndarray):
		raise TypeError('p must be of type numpy.ndarray')

	if not isinstance(q, numpy.ndarray):
		raise TypeError('q must be of type numpy.ndarray')

	if len(p) != len(q):
		raise TypeError('p and q must have same length')

	res = 0
	for i in range(len(p)):
		res = res + p[i] * (numpy.log(p[i]) - numpy.log(q[i]))

	return res

def load_model(filename):
	L = []
	L.append("MFN \"" + filename + "\";")
	L.append("LDX MPT;")
	recode(L)
	run()
	mod = ctypes.cast(read_register("MPT"), ctypes.POINTER(Model)).contents
	mod.prepare()
	return mod

def custom_graph(edgelist):
	if not (isinstance(edgelist, numpy.ndarray) and edgelist.dtype == numpy.uint64):
		raise TypeError('edgelist must be an instance numpy.ndarray with dtype uint64')
	if isinstance(edgelist, numpy.ndarray) and len(edgelist[0]) != 2:
		raise TypeError('provided edgelist is invalid')

	write_register("MPT", 0)
	write_register("GPT", 0)
	lib.reset_ctx(ctx)

	L = []
	L.append("idx_t UINT64")
	L.append("val_t FLT64")

	M = numpy.amax(edgelist)
	V = numpy.unique(edgelist)
	n = len(V)
	m = len(edgelist)
	s = numpy.sum(V)

	if (n != M + 1) or (s != (M * (M + 1))/2):
		raise ValueError('provided edgelist is invalid')

	data_ptr = ctypes.c_uint64(edgelist.ctypes.data)

	L.append("EAP " + str(data_ptr.value) + ";")
	L.append("GPX " + str(n) + ";")
	L.append("RES " + str(m) + ";")
	L.append("GRA " + str(int(GraphType.custom)) + ";")
	L.append("LDX GPT;")

	recode(L)
	run()

	G = ctypes.cast(read_register("GPT"), ctypes.POINTER(Graph)).contents
	return G

def train(data, graph, mode = Mode.mrf, inference = Inference.belief_propagation, iters = 1000, seed = 0, k = 3, in_model = None, initial_stepsize = 0.1, opt_progress_hook = 0, generic_progress_hook = 0, opt_regularization_hook = 0, opt_proximal_hook = 0, T = 1, edge_fraction = 0.1, lam = 0, shared_states = False):
	"""Return a new matrix of given shape and type, without initializing entries.

	Parameters
	----------
	shape : int or tuple of int
		Shape of the empty matrix.
	dtype : data-type, optional
		Desired output data-type.
	order : {'C', 'F'}, optional
		Whether to store multi-dimensional data in row-major
		(C-style) or column-major (Fortran-style) order in
		memory.

	See Also
	--------
	empty_like, zeros

	Notes
	-----
	`empty`, unlike `zeros`, does not set the matrix values to zero, 
	and may therefore be marginally faster. On the other hand, it requires
	the user to manually set all the values in the array, and should be
	used with caution.

	Examples
	--------
	>>> import numpy.matlib
	>>> np.matlib.empty((2, 2))	# filled with random data
	matrix([[  6.76425276e-320,   9.79033856e-307], # random
			[  7.39337286e-309,   3.22135945e-309]])
	>>> np.matlib.empty((2, 2), dtype = int)
	matrix([[ 6600475, 		0], # random
			[ 6586976, 22740995]])

	"""
	if not isinstance(mode, Mode):
		raise TypeError('mode must be an instance of ModeType enum')

	if not (isinstance(graph, GraphType) or isinstance(graph, Graph)):
		raise TypeError('graph must be an instance of GraphType enum or Graph class')

	if not isinstance(inference, Inference):
		raise TypeError('inference must be an instance of InferenceType enum')

	if not isinstance(data, numpy.ndarray):
		raise TypeError('data must be of type numpy.ndarray')

	if not in_model is None and not isinstance(in_model, Model):
		raise TypeError('in_model must be an instance of Model Class')

	if not in_model is None and in_model.statistics is None:
		raise TypeError('in_model must contain empirical statistics for re-training')

	write_register("MPT", 0)
	write_register("GPT", 0)
	lib.reset_ctx(ctx)

	if opt_progress_hook != 0:
		f1 = opt_func(opt_progress_hook)
		write_register("CBO", ctypes.c_uint64.from_buffer(f1).value)
	else:
		write_register("CBO", 0)

	if opt_regularization_hook != 0:
		f2 = opt_func(opt_regularization_hook)
		write_register("CBU", ctypes.c_uint64.from_buffer(f2).value)
	else:
		write_register("CBU", 0)

	if generic_progress_hook != 0:
		f3 = prg_func(generic_progress_hook)
		write_register("CBP", ctypes.c_uint64.from_buffer(f3).value)
	else:
		write_register("CBP", 0)

	if opt_proximal_hook != 0:
		f4 = opt_func(opt_proximal_hook)
		write_register("CPR", ctypes.c_uint64.from_buffer(f4).value)
	else:
		write_register("CPR", 0)

	L = []
	L.append("DEL MPT;");

	if mode == Mode.integer:
		L.append("idx_t UINT64")
		L.append("val_t UINT64")
		L.append("ALG IGD")
	else:
		write_register("STP", integer_from_float(initial_stepsize))
		L.append("idx_t UINT64")
		L.append("val_t FLT64")
		L.append("ALG FL1")

	write_register("KXX", k)
	if seed != 0:
		write_register("SEED", seed)
	write_register("MIS", ord('?'))
	write_register("SEP", ord(','))
	write_register("OVW", 1)
	write_register("HED", 0)
	write_register("LSN", 2)

	write_register("INF", int(inference))
	write_register("MIL", 100)
	write_register("MIO", iters)
	write_register("EPO", 0)
	write_register("LAM", integer_from_float(lam))
	write_register("ELAM", 0)

	if mode >= Mode.strf_linear and mode <= Mode.strf_inv_exponential:
		write_register("TXX", T)
		write_register("YYC", 1)
	else:
		write_register("TXX", 1)
		write_register("YYC", 0)
		write_register("REP", 0)

	if shared_states:
		write_register("YYC", 1)

	if in_model is None:
		data_ptr = ctypes.c_uint64(data.ctypes.data)

		L.append("EDP " + str(data_ptr.value) + ";")
		L.append("NXX " + str(len(data)) + ";")
		L.append("GPX " + str(len(data) * len(data[0]) * 2) + ";")
		L.append("LDX DPT;")

		if isinstance(graph, Graph):
			write_register("GRA", int(GraphType.custom))
			write_register("GPT", ctypes.addressof(graph))
		else:
			write_register("GRA", int(graph))
			L.append("LDX GPT;")

		if not isinstance(graph, Graph)and graph == GraphType.auto:
			L.append("PEL " + str(edge_fraction) + ";")
		L.append("CREATE;")

		if mode == Mode.dbt:
			L.append("DEL MPT;")
			L.append("GRA OTHER;")
			L.append("LSN 1024;")
			L.append("BOLTZMANNTREE;")
			L.append("INITLATENT;")
			L.append("CREATE;")

		if mode >= Mode.strf_linear and mode <= Mode.strf_inv_exponential and T>1:
			L.append("DEL MPT;")
			L.append("GRA OTHER;")
			L.append("STGRAPH;")
			L.append("REP " + str(int(mode)) + ";")
			L.append("CREATE;")

	else:
		in_model.set_ctx_state()

	if mode != Mode.integer and opt_regularization_hook == 0 and opt_proximal_hook == 0:
		L.append("CLOSEDFORM;")
	L.append("ESTIMATE;")

	recode(L)
	run()

	mod = ctypes.cast(read_register("MPT"), ctypes.POINTER(Model)).contents
	mod.prepare()

	res = read_register("RES")
	if mode != Mode.integer:
		res = float_from_integer(res)

	mod.obj = res

	return mod
