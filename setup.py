from setuptools import setup, find_packages

setup(
  name='Goon Threat',
  description='Goon Threat the Game',
  version='0.1.0',
  url='https://github.com/goon-threat/goon-threat',
  packages=find_packages(),
  entry_points={
    'console_scripts': [
      'goon-threat = goon_threat.runtime:run'
    ]
  },
  python_requires='>=3.5',
  install_requires=[
    'esper>=1.0',
    'pygame>=1.9'
  ]
)
