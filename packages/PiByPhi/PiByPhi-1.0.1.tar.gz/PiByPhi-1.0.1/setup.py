from distutils.core import setup
setup(
name = 'PiByPhi',
version = '1.0.1',
py_modules = ['PiByPhi'],
author = 'Saurabh Verma',
author_email = 'verma.saurabh8010@gmail.com',
url = 'http://www.pibyphi.com',
description = 'This pipeline enables the user to extract the best fitting classification algorithm and its respective hyperparameters based on highest accuracy achieved. Different combinations of best fitting algorithm and thier confusion matrix can be returned.',

download_url = 'https://github.com/ersaurabhverma/PiByPhi',    
keywords = ['Machine Learning', 'Data Science', 'PiByPhi','Random Forest','Logistic','Naive Bayes','Automated Classifier'],
install_requires=[            
          'validators',
          'beautifulsoup4',
      ],
classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8'
  ],
)
