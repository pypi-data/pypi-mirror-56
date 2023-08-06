def allow_processor_agnosticism(func):
	def call_right_processor_function(*args, **kwargs):
		return use_classical();
	def use_classical(*args, **kwargs):
		return func(*args, **kwargs);
	def use_dwave(*ags, **kwargs):
		return func(*args, **kwargs);
	def use_ms(*args, **kwargs):
		return func(*args, **kwargs);
	def use_google(*args, **kwargs):
		return func(*args, **kwargs);
	def use_rigetti(*args, **kwargs):
		return func(*args, **kwargs);
	def use_ibm(*args, **kwargs):
		return func(*args, **kwargs);
	return call_right_processor_function