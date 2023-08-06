from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RandomizedSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix
import numpy as np
from pprint import pprint

class PiByPhiClassifier():
    def __init__(self,verbose=0,random_state=None,n_jobs=None):
        """ Initializing the PiByPhiClassifier with all hyperparameters. """
        self.verbose=verbose
        self.random_state=random_state
        self.n_jobs=n_jobs
        self.n_estimators = list(range(10,500,50))
        self.max_features = ['auto', 'sqrt']
        self.max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
        self.max_depth.append(None)
        self.min_samples_split = [2, 5, 10]
        self.min_samples_leaf = [1, 2, 4]
        self.bootstrap = [True, False]
        self.RandomForestClassifierParams = {'n_estimators': self.n_estimators,
                                'max_features': self.max_features,
                                'max_depth': self.max_depth,
                                'min_samples_split': self.min_samples_split,
                                'min_samples_leaf': self.min_samples_leaf,
                                'bootstrap': self.bootstrap}


       
        self.C = np.logspace(0,4,10)
        self.penalty = ['l1', 'l2']
        self.LogisticRegressionParams = {'C': self.C,
                     'penalty': self.penalty}
        self.alpha = np.linspace(0.5, 1.5, 6)
        self.fit_prior = [True, False]
        self.MultinomialNBParams={'alpha' : self.alpha,
                                  'fit_prior' : self.fit_prior}




        self.LogisticRegression = LogisticRegression()
        self.RandomForestClassifier = RandomForestClassifier()
        self.MultinomialNB = MultinomialNB()
        self.classifiers={'LogisticRegression' : [self.LogisticRegression, self.LogisticRegressionParams],

                     'RandomForestClassifier': [self.RandomForestClassifier, self.RandomForestClassifierParams],
                     'MultinomialNB' : [self.MultinomialNB,self.MultinomialNBParams]}

        
        self.model_accuracy = {}
        self.confusion_matrix = {}
        self.CrossValidation = {}
    def fit(self,X_train,y_train):
        """fit the model by providing X_train and y_train.

            --------Example---------
            model=PiByPhiClassifier()
            model.fit(X_train,y_train)
            It will take some time to fit model with best hyperparameters"""
        for keys, value in self.classifiers.items():
            self.CrossValidation[keys] = RandomizedSearchCV(estimator = value[0], param_distributions = value[1], n_iter = 100, cv = 3, verbose=self.verbose, random_state=self.random_state, n_jobs = self.n_jobs)
            self.CrossValidation[keys].fit(X_train,y_train)

            
    def evaluation(self,X_test,y_test,confusion=False,all_models=False):
        """ Use evaluation function to get accuracy score and confusion matrix of models

            -------------Example---------
            model.evaluation(X_test,y_test,confusion=True,all_models=True)


            confusion=bool,[True,False]
            all_models=bool,[True,False]"""
        
        for keys, value in self.classifiers.items():
            self.model_accuracy[keys]   = accuracy_score(y_test, self.CrossValidation[keys].predict(X_test))*100
            self.confusion_matrix[keys] = confusion_matrix(y_test,self.CrossValidation[keys].predict(X_test))


        pprint('Maximum Accuracy {accuracy}% is getting by {model}'.format(model=max(self.model_accuracy, key=self.model_accuracy.get),accuracy=self.model_accuracy[max(self.model_accuracy, key=self.model_accuracy.get)]))
        print('\n')
        if all_models:
            fmt='{0} is getting {1} % accuracy'
            for keys, value in self.model_accuracy.items():
                pprint(fmt.format(keys,value))
                print('\n')

        if confusion and not all_models:
            pprint('-----------Confusion Matrix-----------')
            print('\n')
            pprint(self.confusion_matrix[max(self.model_accuracy, key=self.model_accuracy.get)])

        if all_models and confusion:
            pprint('-----------Confusion Matrix-----------')
            for keys, value in self.confusion_matrix.items():
                print('Confusion Matrix for {model} is : \n {confusion_matrix}'.format(model=keys,confusion_matrix=value))
                print('\n')
            


        
        
