import numpy as np;



class QOperatorMetric():

	def __init__(self, a, b):
		self.right_ket=a;
		self.left_ket=b;
		self.transition_phase=a.phase*b.phase;


	def __repr__(self):
		return str(self.transition_phase)+"|"str(self.right_ket.state)"><"+str(self.left_ket.state)"|";


class QOperatorMetrics(np.matrix):

	def __int__(self, values):
		super(np.matrix, self).__init__(self, values);



class QOperator(np.matrix):


	def __init__(self, phases, metric_basis=None, function=None):
		self.energy_function = function;
		self.metric_basis = metric_basis;
		if type(phases) == list:
			self.phases = np.asmatrix(phases);
		if type(phases) == np.ndarray:
			self.phases = np.asmatrix(phases);
		elif type(phases) == dict:
			linear = lambda i: phases['linear'][i] if 'linear' in phases.keys() else phases['h'] if 'h' in phases.keys() else None;
			quadratic =lambda i,j: phases['quadratic'][i] if 'quadratic' in phases.keys() else phases['J'] if 'J' in phases.keys() else None;
			self.phases = (linear, quadratic);
			#self.phases = np.asmatrix([[ get_linear(i) if i==j for j in range(len(phases[i])) else get_quadratic(i,j)] if j>i else 0 for i in range(len(phases))]);
		#elif energy_function != None:
			#self = self.hamiltonian(energy_function=energy_function);


	def get_model(self,):
		return self.model;


	def get_path_function(self):
		return self.path_function;


	def get_optimizer(self):
		return self.optimizer;


	def set_config(self, config):
		self.config = config;



	def index(self, key):
		pass


	def __repr__(self):
		return str(self.phases.__repr__())+"\n"+str(self.metric_basis);




	def __eq__(self, qb):
		return self.config.processor.__eq__(self, qb)



	def __sub__(self, qb):
		return self.config.processor.__sub__(self, qb);



	def __add__(self, qb):
		return self.config.processor.__add__(self, qb);



	def __mul__(self, a):
		return self.config.processor.__mul__(self, a);




	def get_linear(self):
		return np.asarray([self.value[i,i] for i in range(len(self.value))]);




	def get_quadratic(self):
		return np.asarray([[self.phases[i, j] for i in range(len(self.phases))  if i > j] for j in range(len(self.phases))])




	def save(self, database=None, name=None):
		if database == None:
			database = self.database;
		return database.save(self, name=name);




	def identity(self, *args, **kwargs):
		return self.processor.identity(*args, **kwargs);




	def hammard(self, *args, **kwargs):
		return self.processor.hammard(*args, **kwargs);




	def fft(self, *args, **kwargs):
		return self.processor.fft(*args, **kwargs);




	def svd(self, *args, **kwargs):
		return self.processor.svd(*args, **kwargs);




	def pca(self, *args, **kwargs):
		return self.processor.pca(*args, **kwargs);




	def exp(self, *args, **kwargs):
		return self.processor.exp(*args, **kwargs);




	def pow(self, *args, **kwargs):
		return self.processor.pow(*args, **kwargs);




	def hamiltonian(self, *args, **kwargs):
		return self.processor.hamiltonian(*args, **kwargs);




	def train(self, *args, **kwargs):
		return self.processor.hamiltonian(*args, **kwargs);




	def multiply(self, *args, **kwargs):
		return self.processor.multiplier(*args, **kwargs);




	def divide(self, *args, **kwargs):
		return self.processor.divide(**args, **kwargs);




	def qand(self, *args, **kwargs):
		return self.processor.qand(*args, **kwargs);




	def qor(self, *args, **kwargs):
		return self.processor.qor(*args, **kwargs);




	def cnot(self, *args, **kwargs):
		return self.processor.cnot(*args, **kwargs);






