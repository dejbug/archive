import os, time, base64, pickle

ROOT = '.cache'
ENCODING = 'utf8'

def path(slot):
	assert isinstance(slot, (str, bytes))
	if isinstance(slot, str): slot = slot.encode(ENCODING)
	slot = base64.b64encode(slot, b'+-').decode("ascii")
	return os.path.join(ROOT, slot)

def age(slot):
	p = path(slot)
	if os.path.isfile(p):
		return time.time() - os.path.getmtime(p)

def read(slot):
	p = path(slot)
	if os.path.isfile(p):
		with open(p, 'rb') as file:
			return file.read()

def write(slot, data):
	assert isinstance(data, bytes)
	p = path(slot)
	with open(p, 'wb') as file:
		file.write(data)

def set(slot, data):
	with open(path(slot), 'wb') as file:
		pickle.dump(data, file)

def get(slot):
	p = path(slot)
	if os.path.isfile(p):
		with open(p, 'rb') as file:
			return pickle.load(file)
