import figure_approximator as ap
import numpy as np

for i in range(1, 21):
    file = 'data/' + str(i) + '.png'
    output = 'output/' + str(i) + '.png'
    save_figure = 'figures/' + str(i) + '.png'
    figure = ap.approximate(filename=file, class_type=1, output_filename=output)
    np.save(save_figure, figure)
    print(file)
    print("coords", figure[0])
    print("area", figure[1])
    print("perimeter", figure[2])
    print("\n")


for i in range(21, 41):
    file = 'data/' + str(i) + '.png'
    output = 'output/' + str(i) + '.png'
    save_figure = 'figures/' + str(i) + '.png'
    figure = ap.approximate(filename=file, class_type=0, output_filename=output)
    np.save(save_figure, figure)
    print(file)
    print("coords", figure[0])
    print("area", figure[1])
    print("perimeter", figure[2])
    print("\n")

for i in range(41, 61):
    file = 'data/' + str(i) + '.png'
    output = 'output/' + str(i) + '.png'
    save_figure = 'figures/' + str(i) + '.png'
    figure = ap.approximate(filename=file, class_type=2, output_filename=output)
    np.save(save_figure, figure)
    print(file)
    print("coords", figure[0])
    print("area", figure[1])
    print("perimeter", figure[2])
    print("\n")
