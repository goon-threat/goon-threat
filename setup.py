from setuptools import setup

setup(
  name='Goon Threat',
  description='Goon Threat the Game',
  version='0.1.0',
  url='https://github.com/goon-threat/goon-threat',
  packages=['goon-threat'],
  # entry_points=[],
  # scripts=[],
  python_requires='>=3.5',
  install_requires=[
    'esper',
    'pygame'
  ]
)
