from setuptools import setup

setup(name='gpumeter',
      version='1.0',
      description='Power Meter for NVIDIA GPUs',
      author='Xiaozhe Yao',
      author_email='xiaozhe.yaoi@gmail.com',
      url='https://github.com/autoai-incubator/powermeter',
      packages=['powermeter'],      
      install_requires=[
          'py3nvml',
      ],
)
