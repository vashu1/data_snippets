# run ./get_nucleide_data.sh first
from os import listdir
from os.path import isfile, join

nuc_path = 'www.nucleide.org/DDEP_WG/Nuclides/'
files = [f for f in listdir(nuc_path) if f.endswith('lara.txt')]

data = {}
data2 = []
for file in files:
    with open(join(nuc_path, file)) as f:
        lines = [line.strip() for line in f.readlines()]
        hf = [line for line in lines if line.startswith('Half-life (s)')]
        assert len(hf) == 1
        hf = hf[0]
        hf = hf.split(';')
        hf = list(map(float, hf[1:]))
        data2 += [max(hf)]
        elem_name = file.replace('.lara.txt', '')
        data[elem_name] = min(hf)

max(data.values())
min(data.values())

# take min half_lifes
import matplotlib.pyplot as plt
plt.yscale('log')
plt.xlabel('sorted isotopes')
plt.ylabel('half life, s')
plt.plot(sorted(data.values()))
plt.show()

# take all half_lifes
import matplotlib.pyplot as plt
plt.yscale('log')
plt.xlabel('sorted isotopes')
plt.ylabel('half life, s')
plt.plot(sorted(data2))
plt.show()


# docker run -v $(pwd)/xundl_201001.all:/xundl_201001.all -v $(pwd)/ensdf_201001_199:/ensdf_201001_199 -it pyne/ubuntu_18.04_py3



