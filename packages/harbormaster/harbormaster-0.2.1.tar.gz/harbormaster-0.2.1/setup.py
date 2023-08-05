from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='harbormaster',
      version='0.2.1',
      description='automating docker remote host forwarding',
      long_description=readme(),
      long_description_content_type="text/markdown",
      url='https://github.com/tanishq-dubey/harbormaster',
      author='Tanishq Dubey',
      author_email='tanishq@dubey.dev',
      license='MIT',
      packages=['harbormaster'],
      zip_safe=False,
      scripts=['harbormaster/harbormaster.py'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'Topic :: Utilities',
          'Environment :: Console',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
      ])
