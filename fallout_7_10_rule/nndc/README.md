
### To get dataset, run:

wget https://www.nndc.bnl.gov/ensdfarchivals/distributions/dist20/xundl_201001.all.zip
mkdir xundl_201001.all
unzip xundl_201001.all.zip -d xundl_201001.all

### Building pyne is a pain, so let's use docker:

git clone https://github.com/pyne/pyne.git

cd pyne

add "    pip install numpy ; \" before "pip install --force-reinstall" to pyne/docker/ubuntu_18.04-dev.dockerfile

python3 make_pyne_docker_image.py 

###

docker run -v $(pwd)/xundl_201001.all:/xundl_201001.all -it pyne/ubuntu_18.04_py3

pip install numpy

python3

```
from pyne import ensdf

from collections import Counter
reactions = Counter()
data = {}

def get_data(fname):
    for elem in ensdf.decays(fname):
        if not elem:
            continue
        # see https://pyne.io/pyapi/ensdf.html
        parent_nuc_id, child_nuc_id, reaction_id, half_life_seconds, half_life_error_seconds, *_ = elem
        reactions[(parent_nuc_id, child_nuc_id)] += 1
        if (parent_nuc_id, child_nuc_id, reaction_id) in data and half_life_seconds != data[(parent_nuc_id, child_nuc_id, reaction_id)]:
            print('ERROR', fname, (parent_nuc_id, child_nuc_id, reaction_id), half_life_seconds, data[(parent_nuc_id, child_nuc_id, reaction_id)])
        data[(parent_nuc_id, child_nuc_id, reaction_id)] = half_life_seconds


reactions = Counter()
data = {}
for i in range(1, 300+1):
    try:
        get_data(f'/xundl_201001.all/xundl.{i:03}')
    except:
        pass

data = [v for v in data.values() if v and v < 1e33]
print(data)
```

### Use output of previous step to build plot

```
v = [ _PASTE_OUTPUT_HERE_ ]
import matplotlib.pyplot as plt
plt.yscale('log')
plt.xlabel('sorted isotopes')
plt.ylabel('half life, s')
plt.plot(sorted(v))
plt.show()
```