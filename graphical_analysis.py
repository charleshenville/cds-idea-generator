import matplotlib.pyplot as plt
import numpy as np

data = ([2, 4, 2], [4, 3, 3], [4, 3, 1], [5, 4, 5], [4, 4, 4], [3, 3, 3], [4, 4, 2], [3, 5, 2], [3, 4, 4], [4, 3, 5])
labels = (35, 67, 66, 77, 37, 58, 52, 21, 13, 5)

hypersensitivity = []
durability = []
ease_of_use = []

for item in data:
    hypersensitivity.append(item[0])
    durability.append(item[1])
    ease_of_use.append(item[2])

print(hypersensitivity)
print(durability)
print(ease_of_use)

figure, axis = plt.subplots()
mainplot = axis.scatter(hypersensitivity, ease_of_use, c=durability, edgecolors='black')
cbar = figure.colorbar(mainplot)
cbar.set_label('Durability')

mainplot.set_clim(0, 5)
axis.set_xlim(0, 5.5)
axis.set_ylim(0, 5.5)

axis.set_xlabel('Hypersensitivity')
axis.set_ylabel('Ease of Use')
axis.set_title('Graphical Analysis Chart\n')

for i in range(len(data)):
    axis.annotate(str(labels[i]), (hypersensitivity[i]+0.1, ease_of_use[i]-0.07))

plt.show()
