from quantumics_dna import QuantumDNASeq;

class ClassicalDNASeq():

	def __init__(self, dna_sequence_str=None, verilog_str=None):
		self.dna_code = dna_sequence_str if dna_sequence_str != None else self.get_dna_code(verilog_str);
		self.verilog_code = verilog_str if verilog_str != None else self.get_verilog_code(dna_sequence_str);


	def quantumize(self):
		return QuantumDNASeq(self);


	def get_verilog_code(self, dna_code):
		to_verilog_code = lambda dna_code: dna_code;
		return to_verilog_code(dna_code) if dna_code != None else to_verilog_code(self.dna_code);



	def get_dna_code(self, verilog_str):
		to_dna_code = lambda verilog_str: verilog_str;
		return to_dna_code(verilog_str) if verilog_str != None else to_dna_code(self.verilog_code);