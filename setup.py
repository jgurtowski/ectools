from setuptools import setup

def readme():
    with open('README') as f:
        return f.read()



setup(name='ectools',
      version='0.2',
      description='Long Read Error Correction using pre-assembled short reads',
      long_description=readme(),
      url='https://github.com/jgrutowski/ectools',
      author='James Gurtowski',
      author_email='gurtowsk@cshl.edu',
      license='GPL',
      packages=['ectools'],
      scripts=['scripts/schtats'],
      zip_safe=False)
      
      
      
      
