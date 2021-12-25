from plotter import Plotter

from lsystem_to_hpgl import convert_lsystem_to_hpgl

input_file = open("hpl/sphere.hpl", "rb")
data = input_file.read()
input_file.close()

print(data)

p = Plotter()

p.exec_hpgl([data])
