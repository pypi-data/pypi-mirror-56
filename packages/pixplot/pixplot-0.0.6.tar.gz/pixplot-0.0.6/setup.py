from setuptools import setup
from os.path import join
from pathlib import Path
import os

# populate list of all paths in `./pixplot/web`
web = []
for root, subdirs, files in os.walk(os.path.join('pixplot', 'web')):
  if not files: continue
  for file in files:
    web.append(os.path.join(root, file))
web = [join(*list(Path(i).parts[1:])) for i in web]

setup (
  name='pixplot',
  version='0.0.6',
  packages=['pixplot'],
  package_data={
    'pixplot': web,
  },
  keywords = ['computer-vision', 'webgl', 'three.js', 'tensorflow', 'machine-learning'],
  description='Visualize large image collections with WebGL',
  url='https://github.com/yaledhlab/pix-plot',
  author='Douglas Duhaime',
  author_email='douglas.duhaime@gmail.com',
  license='MIT',
  install_requires=[
    'glob2>=0.6',
    'Keras>=2.3.0',
    'Pillow>=6.1.0',
    'numpy>=1.16.0',
    'scikit-image>=0.15.0',
    'scikit-learn>=0.21.3',
    'tensorflow>=1.14.0,<=2.0.0',
    'umap-learn>=0.3.10',
    'yale-dhlab-rasterfairy>=1.0.3',
  ],
  entry_points={
    'console_scripts': [
      'pixplot=pixplot:parse',
    ],
  },
)