# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pro_gan_pytorch']

package_data = \
{'': ['*'], 'pro_gan_pytorch': ['metric/*', 'utils/*']}

install_requires = \
['PyYAML==5.1.2',
 'albumentations>=0.4.2,<0.5.0',
 'easydict>=1.9,<2.0',
 'imageio>=2.6,<3.0',
 'opencv-python>=4.1,<5.0',
 'pandas==0.25.2',
 'scikit-image==0.16.2',
 'torch==1.3.0',
 'torchnet>=0.0.4,<0.0.5',
 'torchvision==0.4.1',
 'tqdm==4.36.1',
 'urllib3==1.25.6']

entry_points = \
{'console_scripts': ['train = pro_gan_pytorch.train:main']}

setup_kwargs = {
    'name': 'pro-gan-pytorch',
    'version': '0.1.1',
    'description': 'various GANS training package',
    'long_description': None,
    'author': 'Sindhura',
    'author_email': 'sindhura.k@fractal.ai',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '==3.6.9',
}


setup(**setup_kwargs)
