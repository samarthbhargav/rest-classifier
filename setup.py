from setuptools import setup

setup(name='RestSentiment',
      version='1.0',
      description='REST based Classifier',
      author='Samarth Bhargav',
      author_email='samarth.bhargav92@gmail.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=['Flask==0.10.1', 'Flask-RESTful==0.2.12','scikit-learn==0.14.1'],
     )
