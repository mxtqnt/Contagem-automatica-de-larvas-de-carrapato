import numpy
import matplotlib.pyplot as plt

def lista_cores(quantidade_cores):
    cmap = plt.get_cmap('tab10')
    cores_rgb = cmap(numpy.linspace(0, 1, quantidade_cores))

    cores_bgr = (cores_rgb[:, 2] * 255, cores_rgb[:, 1] * 255, cores_rgb[:, 0] * 255)
    cores_bgr = numpy.round(cores_bgr).astype(int).T

    cores_bgr = [(int(b), int(g), int(r)) for b, g, r in cores_bgr]
    return cores_bgr


quantidade_cores = 36
cores = lista_cores(quantidade_cores)
print(cores)