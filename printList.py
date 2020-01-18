import numpy 
ar = numpy.load('list1.npy')
listForm=numpy.ndarray.tolist(ar)

with open("test.txt", "w") as file:
    file.write(str(listForm))