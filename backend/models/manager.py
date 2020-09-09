models = {}

def get_model(name):
	return models[name]

def set_model(name, model):
	global models
	models[name] = model