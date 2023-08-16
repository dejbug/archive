import sys

def stringify(cls):
	def __str__(self):
		return self.__class__.__name__ + str(self.__dict__)
	setattr(cls, "__str__", __str__)
	return cls

def dumpify(cls):
	def dump(self, file = sys.stdout):
		for k, v in self.__dict__.items():
			file.write(f'{k:>10s} = |{v}|\n')
		file.write('\n')
	setattr(cls, "dump", dump)
	return cls
