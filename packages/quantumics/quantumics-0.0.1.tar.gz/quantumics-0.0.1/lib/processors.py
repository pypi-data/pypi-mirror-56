import dwavebinarycsp as dbc;
from qiskit import ClassicalRegister as CR, QuantumRegister as QR, QuantumCircuit as QC
import math;
from dwave.system.samplers import DWaveSampler;
from qiskit import IBMQ, backends;
from hybrid import State, States;
from pymongo import MongoClient;
import numpy as np;
import sklearn as skl;
import qsharp
from qoperator import QOperator;
from quantumics import QUnit, QTUnit, QData, QTData;
from qmap import QMap;
from qdatabase import QDatabase;
#import Microsoft.Samples as ms







class QProcessor():

	def __init__(self, mins=[0,0,0,0], database=QDatabase('mongodb://localhost:7000'), 
		maxs=[16, 16, 16, 16], delayed=False):
		self.delayed = delayed
		self.maxs = maxs;
		self.mins = mins;
		self.database = database;




	def __mul__(self, a, b):
		return self.dot(a, b);



	def __add__(self, a, b):
		return self.add(a, b);



	def __sub__(self, a, b):
		return self.sub(a, b);



	def __eq__(self, a, b):
		return self.equal(a, b);



	def equal(self, a, b):
		if type(a) == QUnit or type(a) == QTUnit:
			return (type(a) == type(b)) and (a.amplitude == b.amplitude) and (a.state == b.state)
		elif type(a) == QData or type(b) == QTData:
			return (type(a) == type(b)) and (a.states == b.states)
		elif type(a) == QMap and type(b) == QMap:
			return dict(a) == dict(b);


	def dot(self, qa, qb):
		"""
		Use Optimization Problem approach with DWave System.
		"""
		if (type(qa)== QUnit or type(qa) == QTUnit) and (type(qb)== QUnit or type(qb) == QTUnit):
			return self.unit_mul(qa, qb);
		elif (type(qa)== QData or type(qa) == QTData) and (type(qb)== QData or type(qb) == QTData):
			return self.data_mul(qa, qb);
		elif type(qa)== QOperator and type(qb)==QUnit:
			return self.operator_qunit(qa, qb);
		elif type(qa)== QOperator and type(qb)==QOperator:
			return self.operator_mul(qa, qb);
		elif type(qa)== QTUnit and type(qb)==QOperator:
			return self.qtunit_operator(qa, qb);
		elif type(qa)== QOperator and type(qb)==QData:
			return self.operator_qdata(qa, qb);
		elif type(qa)== QTData and type(qb)==QOperator:
			return self.qtdata_operator(qa, qb);
		elif (type(qa) == QMap or issubclass(type(qa), QMap))  and type(qb) == QUnit:
			return self.qmap_qunit_mul(qa, qb);
		elif (type(qb) == QMap or issubclass(type(qb), QMap)) and type(qa) == QTUnit:
			return self.qtunit_qmap_mul(qa, qb);
		elif (type(qa) == QMap or issubclass(type(qa), QMap)) and type(qb) == QData:
			return self.qmap_qdata_mul(qa, qb);
		elif (type(qb) == QMap or issubclass(type(qb), QMap)) and type(qa) == QTData:
			return self.qtdata_qmap_mul(qa, qb);




	def div(self, qa, qb):
		"""
		Use Optimization Problem approach with DWave System.
		"""
		if type(qa)== QUnit and type(qb)==QUnit:
			return self.qunit_mul(qa, qb);
		elif type(qa)== Operator and type(qb)==QUnit:
			return self.operator_qunit(qa, qb);
		elif type(qa)== Operator and type(qb)==Operator:
			return self.operator_mul(qa, qb);
		elif type(qa)== QTUnit and type(qb)==Operator:
			return self.qtunit_operator(qa, qb);
		elif type(qa)== QTUnit and type(qb)==QTUnit:
			return self.qtunit_mul(qa, qb);
		elif type(qa)== QTUnit and type(qb)==QUnit:
			return self.qtunit_qunit(qa, qb);
		elif type(qa)== QUnit and type(qb)==QTUnit:
			return self.qunit_qtunit(qa, qb);
		elif type(qa)== QData and type(qb)==QData:
			return self.qdata_mul(qa, qb);
		elif type(qa)== Operator and type(qb)==QData:
			return self.operator_qdata(qa, qb);
		elif type(qa)== QTData and type(qb)==Operator:
			return self.qtdata_operator(qa, qb);
		elif type(qa)== QTData and type(qb)==QTData:
			return self.qtdata_mul(qa, qb);
		elif type(qa)== QTData and type(qb)==QData:
			return self.qtdata_qdata(qa, qb);
		elif type(qa)== QData and type(qb)==QTData:
			return self.qdata_qtdata(qa, qb);



	def add(self, qa, qb):
		"""
		Use Optimization Problem approach with DWave System.
		"""
		if type(qa) != type(qb):
			if type(qa) == QData and type(qb) == QUnit:
				return self.qdata_qunit_add(qa, qb);
			elif type(qb) == QData and type(qa) == QUnit:
				return self.qdata_qunit_add(qb, qa);
			elif type(qa) == QTData and type(qb) == QTUnit:
				return self.qtdata_qtunit_add(qb, qa);
			elif type(qb) == QTData and type(qa) == QTUnit:
				return self.qtdata_qtunit_add(qb, qa);
		elif type(qa) == type(qb):
			if type(qa) == QOperator:
				return self.operator_add(qa, qb);
			elif type(qa) == QUnit or type(qa) == QTUnit:
				return self.unit_add(qa, qb);
			elif type(qa) == QData or type(qa) == QTData and type(qa)==type(qb):
				return self.data_add(qa, qb);
			elif type(qa) == Quantumic(qa, qb):
				return self.quantumic_add(qa, qb);
			elif type(qa) == QEntangle or type(qa) == QBind:
				return self.qentangle_add(qa, qb);
			elif type(qa) == QSystem(qa, qb):
				return self.qsystem_add(qa, qb);
			elif type(qa) == Quantumics(qa, qb):
				return self.quantumics_add(qa, qb);



	def sub(self, qa, qb):
		"""
		Use Optimization Problem approach with DWave System.
		"""
		if type(qa) != type(qb):
			raise Exception();
		elif type(qa) == type(qb):
			if type(qa) == QOperator:
				return self.operator_sub(qa, qb);
			elif type(qa) == QUnit or type(qa) == QTUnit:
				return self.unit_sub(qa, qb);
			elif type(qa) == QData(qa, qb) or type(qa) == QTData:
				return self.data_sub(qa, qb);
			elif type(qa) == Quantumic(qa, qb):
				return self.quantumic_sub(qa, qb);
			elif type(qa) == QEntangle or type(qa) == QBind:
				return self.qentangle_sub(qa, qb);
			elif type(qa) == QSystem(qa, qb):
				return self.qsystem_sub(qa, qb);
			elif type(qa) == Quantumics(qa, qb):
				return self.quantumics_sub(qa, qb);


	def train(self, *args, **kwargs):
		return self.hamiltonian(*args, **kwargs)



	def fit(self, *args, **kwargs):
		return self.hamiltonian(*args, **kwargs);




	def eval(self, a):
		pass



	def hamiltonian(self, operator, matrix=None, qdata=None, processor=None, dataset=None, energy_function=None, file=None):
		if energy_function != None:
			self.energy_function = energy_function if energy_function!=None else self.energy_function;
			self.bqm = dbc.dimod.BinaryQuadraticModel().from_function(self.energy_function, quantumic.labels);
		if dataset != None:
			self.from_values(dataset);
		return operator;




	def save(self, database=None, name=None):
		if database == None:
			database = self.database
		return self.database.save(self, name=name);



	def fft(self, *args, **kwargs):
		pass



	def pow(self, *args, **kwargs):
		pass



	def exp(self, *args, **kwargs):
		pass



	def svd(self, *args, **kwargs):
		pass


	def min(self, *args, **kwargs):
		pass



	def max(self, *args, **kwargs):
		pass




	def pca(self, *args, **kwargs):
		pass




	def identity(self,n_qbits=None):
		"""
		Find Identity BQM
		"""
		self.bqm = dbc.dimod.BinaryQuadraticModel().from_numpy_matrix(np.identity(n_qbits))
		return self.processor.identity(n_qbits=n_qbits);




	def hammard(self, n_qbits=None):
		"""
		"""
		self.bqm = None
		return self



	def multiply(self, qa, qb):
		pass


	def divide(self, qa, qb):
		pass



	def qand(self, qa, qb):
		pass




	def qor(self, qa, qb, n_qbits=None):
		pass




	def cnot(self, qa, qb, n_qbits=None):
		pass







class CPUQProcessor(QProcessor):


	def train(self, *args, **kwargs):
		return self.hamiltonian(args, kwargs);



	def fit(self, *args, **kwargs):
		return self.hamiltonian(args, kwargs);


	def __repr__(self):
		pass


	def eval(self, a):
		pass



	def hamiltonian(self, operator=None, model=None, eigenmatrix=None, metric_basis=None, dataset=None, eingenfunction=None, file=None):
		if operator != None:
			return operator;
		if model == None:
			pass
		else:
			return QOperator(model, metric_basis=metric_basis);



	def save(self, database=None, name=None):
		if database == None:
			database = self.database
		return self.database.save(self, name=name);



	def fft(self, *args, **kwargs):
		pass



	def pow(self, *args, **kwargs):
		pass



	def exp(self, *args, **kwargs):
		pass



	def svd(self, *args, **kwargs):
		pass




	def pca(self, *args, **kwargs):
		pass




	def identity(self,n_qbits=None):
		"""
		Find Identity BQM
		"""
		self.bqm = dbc.dimod.BinaryQuadraticModel().from_numpy_matrix(np.identity(n_qbits))
		return self.processor.identity(n_qbits=n_qbits);




	def hammard(self, n_qbits=None):
		"""
		"""
		self.bqm = None
		return self



	def multiply(self, qa, qb):
		pass


	def divide(self, qa, qb):
		pass



	def qand(self, qa, qb):
		pass




	def qor(self, qa, qb, n_qbits=None):
		pass




	def cnot(self, qa, qb, n_qbits=None):
		pass


	def condense(self, qa):
		typer = type(qa);
		if typer == QData or typer == QTData:
			states = set([ qu.state for qu in qa.states]);
			return typer([(sum(qa[state]), state) for state in states])



	def unit_add(self, qa, qb):
		typer = type(qa)
		if typer == QUnit or typer ==QTUnit:
			if qa.state == qb.state :
				dtyper = QData if type(qa) == QUnit else QTData;
				return dtyper([typer(qa.amplitude + qb.amplitude, *qb.state)]);
			else:
				return QData([qa, qb]) if typer == QUnit else QTData([qa, qb]);


	def operator_add(self, qa, qb):
		typer1 = type(qa);
		typer2 = type(qb);
		if typer1 == QOperator and typer2==QOperator:
			return QOperator(qa.amplitudes + qb.amplitudes, qb.states);



	def unit_sub(self, qa, qb):
		typer = type(qa)
		if typer == QUnit or typer ==QTUnit:
			if qa.state == qb.state :
				dtyper = QData if type(qa) == QUnit else QTData;
				return dtyper([typer(amplitude=(qa.amplitude - qb.amplitude), state=qb.state)]);
			else:
				qb.amplitude = - qb.amplitude;
				return QData([qa, qb]) if typer == QUnit else QTData([qa, qb]);



	def operator_sub(self, qa, qb):
		typer1 = type(qa);
		typer2 = type(qb);
		if typer1 == QOperator and typer2==QOperator:
			return QOperator(qa.amplitudes - qb.amplitudes, qb.states);



	def unit_mul(self, qa, qb):
		typer = type(qa)
		if typer == QUnit or typer ==QTUnit:
			if type(qa) == type(qb): 
				return typer(qa.amplitude*qb.amplitude, (qa.state, qb.state))
			elif type(qa) == QUnit and type(qb) == QTUnit:
				a = QUnit(1, qa.state); b = QUnit(1, qb.state);
				return QOperator([[qa.amplitude*qb.amplitude]], metrics=QOperatorMetrics([[(a,b)]]))
			elif type(qa) == QTUnit and type(qb) == QUnit:
				return qa.amplitude*qb.amplitude*qa.model.get_metric(qa.state, qb.state);
			elif (type(qa) != QTUnit and type(qa)) != QUnit and (type(qb) == QTUnit or type(qb) == QUnit):
				return type(qb)(qa*qb.amplitude, qb.state);
			elif (type(qb) != QTUnit and type(qb)) != QUnit and (type(qa) == QTUnit or type(qa) == QUnit):
				return type(qa)(qb*qa.amplitude, qa.state);



	def operator_mul(self, qa, qb):
		typer1 = type(qa);
		typer2 = type(qb);
		if typer1 == QOperator and typer2==QOperator:
			return QOperator(qa.amplitudes * qb.amplitudes, qb.states);



	def qmap_qunit_mul(self, qa, qb):
		return qa.transform(qb);



	def qtunit_qmap_mul(self, qa, qb):
		return qb.transform(qa);



	def qmap_qdata_mul(self, qa, qb):
		return qa.transform(qb);



	def qtdata_qmap_mul(self, qa, qb):
		return qb.transform(qa);



	def qoperator_qmap_mul(self, qa, qb):
		return qb.transform(qa);


	def qmap_qoperator_mul(self, qa, qb):
		return qa.transform(qb);





	def data_add(self, qa, qb):
		typer = type(qa)
		if typer == QData or typer ==QTData:
			if typer == type(qb):
				keys = qa.keys;
				keys.extend(qb.keys);
				keys = list(set(keys));
				return typer([type(qa[0])( sum([ s.amplitude for s in qa[key].states]) + sum([ w.amplitude for w in qb[key].states]),  *qa[key][0].state ) for key in keys ]);
			else:
				pass;



	def data_sub(self, qa, qb):
		typer = type(qa)
		if typer == QData or typer ==QTData:
			if typer == typer(qb):
				sub_typer = type(qa[0]);
				states = list(set(qa.states.concat(qb.states)));
				return typer([sub_typer(qa.amplitudes[qa.index(k)] - qa.amplitudes[qa.index(k)]) for k in states ]);
			else:
				raise Exception();


	def data_mul(self, qa, qb):
		if type(qa) == QData and type(qb) ==QTData:
			return self.data_outer_product(qa, qb);
		elif type(qa) == QTData and type(qb) ==QData:
			return self.data_inner_product(qa, qb);
		elif (type(qa) == QData and type(qb) ==QData) or (type(qa) == QTData and type(qb) == QTData) :
			return self.data_outer_product(qa, qb);
			


	def data_outer_product(self, qa, qb):
		return QOperator([[],[]],[[],[]])



	def data_inner_product(self, qa, qb):
		pass


	def data_tensor_product(self, qa, qb):
		return QData();


	def qdata_qunit_add(self, qa, qb):
		return qa + QData([qb]);



	def qtdata_qtunit_add(self, qa, qb):
		return qa + QTData([qb]); 




class DWaveQProcessor(QProcessor):


	def train(self, *args, **kwargs):
		return self.hamiltonian(args, kwargs);



	def fit(self, *args, **kwargs):
		return self.hamiltonian(args, kwargs);



	def eval(self, a):
		pass



	def hamiltonian(self, operator=None, model=None, eigenmatrix=None, metric_basis=None, dataset=None, eingenfunction=None, file=None):
		if operator != None:
			return operator;
		if model == None:
			pass
		else:
			return QOperator(model, metric_basis=metric_basis);



	def measure(self, ):
		return None;



	def save(self, database=None, name=None):
		if database == None:
			database = self.database
		return self.database.save(self, name=name);



	def fft(self, *args, **kwargs):
		np_identity_matrix = np.identity(n_qbits)
		self.bqm = dbc.dimod.BinaryQuadraticModel().from_numpy_matrix(np_identity_matrix);
		return QOperator();





	def svd(self, *args, **kwargs):
		np_identity_matrix = np.identity(n_qbits)
		self.bqm = dbc.dimod.BinaryQuadraticModel().from_numpy_matrix(np_identity_matrix);
		return QOperator();




	def pca(self, *args, **kwargs):
		np_identity_matrix = np.identity(n_qbits)
		self.bqm = dbc.dimod.BinaryQuadraticModel().from_numpy_matrix(np_identity_matrix);
		return QOperator();




	def identity(self,n_qbits=None):
		"""
		Find Identity BQM
		"""
		np_identity_matrix = np.identity(n_qbits)
		self.bqm = dbc.dimod.BinaryQuadraticModel().from_numpy_matrix(np_identity_matrix);
		return QOperator();




	def hammard(self, n_qbits=None):
		"""
		"""
		hammard_matrix = np.matrix([[], [], []]);
		self.bqm = dbc.dimod.BinaryQuadraticModel().from_numpy_matrix(hammard_matrix);
		return QOperator();




	def multiply(self, qa, qb):
		np_identity_matrix = np.identity(n_qbits)
		self.bqm = dbc.dimod.BinaryQuadraticModel().from_numpy_matrix(np_identity_matrix);
		return QOperator();



	def divide(self, qa, qb):
		np_identity_matrix = np.identity(n_qbits)
		self.bqm = dbc.dimod.BinaryQuadraticModel().from_numpy_matrix(np_identity_matrix);
		return QOperator();



	def qand(self, qa, qb):
		np_identity_matrix = np.identity(n_qbits)
		self.bqm = dbc.dimod.BinaryQuadraticModel().from_numpy_matrix(np_identity_matrix);
		return QOperator();




	def qor(self, qa, qb, n_qbits=None):
		np_identity_matrix = np.identity(n_qbits)
		bqm = dbc.dimod.BinaryQuadraticModel().from_numpy_matrix(np_identity_matrix);
		return QOperator();




	def cnot(self, qa, qb, n_qbits=None):
		np_identity_matrix = np.identity(n_qbits)
		bqm = dbc.dimod.BinaryQuadraticModel().from_numpy_matrix(np_identity_matrix);
		return QOperator();



	def unit_add(self, qa, qb):
		typer = type(qa)
		if typer == QUnit or typer ==QTUnit:
			if qa.state == qb.state :
				csp = None;
				bqm = None;
				if self.delayed == True:
					result_qdata = QData();
					result_qdata.model.processor.set_query(bqm);
					return result_qdata;
				else :
					result = DWaveSampler().sample(bmq);
					states = result.samples();
					result_qdata = QData([(x.energy, state) for x in states]);
					result_qdata.model.set_processor(self);
					return result_qdata;
			else:
				return QData([qa, qb]) if typer == QUnit else QTData([qa, qb]);


	def operator_add(self, A, B):
		typer1 = type(A);
		typer2 = type(B);
		if typer1 == QOperator and typer2==QOperator:
			bqm = dbc.BinaryQuadraticModel();
			return QOperator(qa.amplitudes + qb.amplitudes, qb.states);



	def unit_sub(self, qa, qb):
		typer = type(qa)
		if typer == QUnit or typer ==QTUnit:
			if qa.state == qb.state :
				return typer(qa.amplitude - qb.amplitude, qb.state);
			else:
				qb.amplitude = - qb.amplitude;
				return QData([qa, qb]) if typer == QUnit else QTData([qa, qb]);



	def operator_sub(self, A, B):
		typer1 = type(A);
		typer2 = type(B);
		if typer1 == QOperator and typer2==QOperator:
			bqm = dbc.BinaryQuadraticModel();
			return QOperator(qa.amplitudes + qb.amplitudes, qb.states);



	def unit_mul(self, qa, qb):
		typer = type(qa)
		if typer == QUnit or typer ==QTUnit:
			if type(qa) == type(qb): 
				return typer(qa.amplitude*qb.amplitude, (qa.state, qb.state))
			elif type(qa) == QUnit and type(qb) == QTUnit:
				a = QUnit(1, qa.state); b = QUnit(1, qb.state);
				return QOperator([[qa.amplitude*qb.amplitude]], metrics=QOperatorMetrics([[(a,b)]]))
			elif type(qa) == QTUnit and type(qb) == QUnit:
				return qa.amplitude*qb.amplitude*qa.model.get_metric(qa.state, qb.state);
			elif (type(qa) != QTUnit and type(qa)) != QUnit and (type(qb) == QTUnit or type(qb) == QUnit):
				return type(qb)(qa*qb.amplitude, qb.state);
			elif (type(qb) != QTUnit and type(qb)) != QUnit and (type(qa) == QTUnit or type(qa) == QUnit):
				return type(qa)(qb*qa.amplitude, qa.state);



	def operator_mul(self, qa, qb):
		typer1 = type(qa);
		typer2 = type(qb);
		if typer1 == QOperator and typer2==QOperator:
			return QOperator(qa.amplitudes * qb.amplitudes, qb.states);





	def data_add(self, qa, qb):
		typer = type(qa)
		if typer == QData or typer ==QTData:
			if typer == typer(qb):
				sub_typer = type(qa[0]);
				states = list(set(qa.states.concat(qb.states)));
				return typer([sub_typer(qa.amplitudes[qa.index(k)] + qa.amplitudes[qa.index(k)]) for k in states ]);
			else:
				raise Exception();



	def data_sub(self, qa, qb):
		typer = type(qa)
		if typer == QData or typer ==QTData:
			if typer == typer(qb):
				sub_typer = type(qa[0]);
				states = list(set(qa.states.concat(qb.states)));
				return typer([sub_typer(qa.amplitudes[qa.index(k)] - qa.amplitudes[qa.index(k)]) for k in states ]);
			else:
				raise Exception();


	def data_mul(self, qa, qb):
		if type(qa) == QData and type(qb) ==QTData:
			return self.data_outer_product(qa, qb);
		elif type(qa) == QTData and type(qb) ==QData:
			return self.data_inner_product(qa, qb);
		elif (type(qa) == QData and type(qb) ==QData) or (type(qa) == QTData and type(qb) == QTData) :
			return self.data_outer_product(qa, qb);
			


	def data_outer_product(self, qa, qb):
		return QOperator([[],[]],[[],[]])



	def data_inner_product(self, qa, qb):
		pass


	def data_tensor_product(self, qa, qb):
		return QData();







class IBMQProcessor(QProcessor):


	def test(self):
		return ms.HelloQ.simulate();


	def eval(self, a):
		pass



	def hamiltonian(self, operator, matrix=None, qdata=None, processor=None, dataset=None, energy_function=None, file=None):
		if energy_function != None:
			self.energy_function = energy_function if energy_function!=None else self.energy_function;
			self.bqm = dbc.dimod.BinaryQuadraticModel().from_function(self.energy_function, quantumic.labels);
		if dataset != None:
			self.from_values(dataset);
		return operator;




	def save(self, database=None, name=None):
		if database == None:
			database = self.database
		return self.database.save(self, name=name);



	def fft(self, *args, **kwargs):
		pass



	def pow(self, *args, **kwargs):
		pass



	def exp(self, *args, **kwargs):
		pass



	def svd(self, *args, **kwargs):
		pass




	def pca(self, *args, **kwargs):
		pass




	def identity(self,n_qbits=None):
		self.bqm = dbc.dimod.BinaryQuadraticModel().from_numpy_matrix(np.identity(n_qbits))
		return self.processor.identity(n_qbits=n_qbits);




	def hammard(self, n_qbits=None):
		self.bqm = None
		return self



	def multiply(self, qa, qb):
		pass


	def divide(self, qa, qb):
		pass



	def qand(self, qa, qb):
		pass




	def qor(self, qa, qb, n_qbits=None):
		pass




	def cnot(self, qa, qb, n_qbits=None):
		pas






