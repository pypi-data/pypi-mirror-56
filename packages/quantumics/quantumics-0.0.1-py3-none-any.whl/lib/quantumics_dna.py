from quantumics import Quantumic, Quantumics, Operator;
import pyverilog.vparser.ast as vast
from pyverilog.ast_code_generator.codegen import ASTCodeGenerator
from classical import DNASeq
from processors import DNAProcessor



class QuantumDNASeq(Quantumic):


	def __init__(self, classicalDNASeq):
		pass





	def classicalize(self):
		return DNASeq(self);





class QGMOperator(Operator):


	def to_json():
		pass





class Organism(ClassicalDNASeq):


	def __init__(self, *args, **kwargs):
		self = DNASeq.__init__(*args, **kwargs);



	def quantumize(self):
		return QOrganism(self);







class QuantumOrganism(QuantumDNASeq):



	def __init__(self, *args, **kwargs):
		ClassicalDNASeq(*args, **kwargs);


	def add(self, operator):
		return operator * self;


	def classicalize(self):
		return ClassicalDNASeq(self);










def solution0a():
	organism = QuantumDNASeq();
	_=Operator();
	I=_.I;
	NOT=_.NOT;
	organism = I*organism;
	new_organisms = NOT*organism;
	def hypothesis_function():
		pass
	EM = _.hamiltonian(file="electromagnetism_dna_datasets", dataset="", energy_function=hypothesis_function);
	em_organism = EM*organism;
	print(em_organism);






def solution0b():
	organism = QuantumOrganism();
	_ = QGMOperator();
	def hypothesis_function():
		pass
	communication = _.hamiltonian(dataset="em_communication_dna_dataset", energy_function=hypothesis_function);
	creator = _.hamiltonian(dataset="creator_dna_dataset", energy_function=hypothesis_function);
	if_hot_action = "";
	if_high_ems_start_listening = "";
	if_protocol_matched_connect = "";
	request = "";
	response = ""
	orgamism.add(communication).add(creator).add(if_hot_action).add(if_high_ems_start_listening)
	.add(if_protocol_matched_connect).add(request).add(response);
	modified_organism_vc = organism.get_verilog_code();
	modified_organism_gc = organism.get_dna_code();








