from setuptools import find_packages, setup

version = '3.0.2'

setup(name='pub.tools',
      version=version,
      description="Package of tools for formatting publication data and accessing data from PubMed's Entrez tool",
      long_description=open("README.md").read() + "\n" + open("CHANGES.md").read(),
      long_description_content_type='text/markdown',
      classifiers=[
          "Programming Language :: Python :: 3",
          "Topic :: Scientific/Engineering",
          "Topic :: Scientific/Engineering :: Bio-Informatics",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='',
      author='Eric Wohnlich',
      author_email='wohnlice@imsweb.com',
      url='http://git.imsweb.com/wohnlice/pub.tools',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['pub'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'biopython>=1.73',
          'unidecode',
          'lxml',
          'requests'
      ],
      )
