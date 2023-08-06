from setuptools import setup

setup(name='tensorcox',
      version='0.1',
      description='Coxs partial likelihood in Tensorflow',
      url='https://github.com/alexwjung/TensorCox/archive/v_0.1.tar.gz',
      author='awj',
      author_email='alexwjung@googlemail.com',
      license='MIT',
      packages=['tensorcox', 'tensorcox.test'],
      install_requires=['tensorflow', 'numpy'],
      long_description_content_type='text/markdown',
      long_description=open('README.md').read(),
      zip_safe=False)
