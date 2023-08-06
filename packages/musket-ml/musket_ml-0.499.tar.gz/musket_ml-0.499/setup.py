from setuptools import setup
import setuptools
import io
import os

here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()
    
setup(name='musket_ml',
      version='0.499',
      long_description=long_description,
      long_description_content_type="text/markdown",
      description='Common parts of my pipelines',
      url='https://github.com/petrochenko-pavel-a/musket_core',
      author='Petrochenko Pavel',
      author_email='petrochenko.pavel.a@gmail.com',
      license='MIT',
      packages=setuptools.find_packages(),
      include_package_data=True,
      install_requires=["musket_text>=0.443","musket_core>=0.498","classification_pipeline>=0.432","segmentation_pipeline>=0.432"],
      zip_safe=False)