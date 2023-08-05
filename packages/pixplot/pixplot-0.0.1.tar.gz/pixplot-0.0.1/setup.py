from setuptools import setup
from os.path import join
from pathlib import Path
from glob2 import glob

web = glob(join('pixplot', 'web', '**'))
web = [join(*list(Path(i).parts[1:])) for i in web]

setup (
  name='pixplot',
  version='0.0.1',
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
  install_requires=open('requirements.txt').read().splitlines(),
  entry_points={
    'console_scripts': [
      'pixplot=pixplot:parse',
    ],
  },
)