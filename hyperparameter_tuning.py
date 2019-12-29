import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
import nltk
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from numpy import *
from hyperopt import fmin, tpe, hp, Trials, STATUS_OK, STATUS_FAIL, space_eval
import inspect
import math
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
import json


def write_to_json(lst, file_name):
    """

    :param lst: the dictionary into the list
    :param file_name: the name
    :return:
    """
    with open(os.path.join(os.getcwd(), 'hyperparams_results', file_name),
              'a', encoding='utf-8') as file:
        for item in lst:
            x = json.dumps(item)
            file.write(x + '\n')


trials = Trials()
MAX_EVALS = 500


def f(space):
    try:
        fitness = 1 - create_models(**space)
        return {'loss': fitness, 'status': STATUS_OK}
    except:
        return {'loss': math.inf, 'status': STATUS_FAIL}


def get_search_space():
    search_space = {
        'classifier_type': hp.choice('classifier_type', ['rf', 'svc', 'lr']),
        'C': hp.uniform('C', 0.001, 15),
        'l': hp.choice('l', ['l1', 'l2']),
        'kernel': hp.choice('kernel', ['linear', 'poly', 'rbf', 'sigmoid', 'precomputed']),
        'n_trees': hp.choice('n_trees', [int(x) for x in np.linspace(start=200, stop=2000, num=10)]),
        'lr_penalty': hp.choice('lr_penalty', ['l1', 'l2']),
    }

    target_f_params = inspect.getfullargspec(create_models).args

    filtered_search_space = {i: search_space[i] for i in list(search_space.keys()) if i in target_f_params}
    if len(filtered_search_space) != len(search_space):
        print('WARNING: Some arguments are not in the target function')
    return filtered_search_space


def create_models(classifier_type, C, l, kernel, n_trees, lr_penalty):
    """
    Hyperparameter tuning - Hyperopt

    :param classifier_type:
    :param C: regularization parameter
    :param l: kernel type to be used in the algorithm
    :param kernel: kernel in svm
    :param n_trees: number of trees for random forest
    :param lr_penalty: penalty for logistic regression
    :return: accuracy scores
    """

    _results = {'model': classifier_type}
    n_folds = 3
    skf = StratifiedKFold(n_splits=n_folds)
    skf.get_n_splits(X, y)

    _results['l'] = l

    # Building classifier
    if classifier_type == 'svc':
        clf = Pipeline([
            ('feature_vect', TfidfVectorizer(strip_accents='unicode',
                                             tokenizer=nltk.word_tokenize,
                                             stop_words='english',
                                             decode_error='ignore',
                                             analyzer='word',
                                             norm=l,
                                             ngram_range=(1, 2)
                                             )),
            ('clf', SVC(probability=True,
                        C=C,
                        shrinking=True,
                        kernel=kernel))
        ])
        _results['kernel'] = kernel
        _results['C'] = C
    elif classifier_type == 'rf':
        clf = Pipeline([
            ('feature_vect', TfidfVectorizer(strip_accents='unicode',
                                             tokenizer=nltk.word_tokenize,
                                             stop_words='english',
                                             decode_error='ignore',
                                             analyzer='word',
                                             norm=l,
                                             ngram_range=(1, 2)
                                             )),
            ('clf', RandomForestClassifier(random_state=42,
                                           # n_estimators=n_trees,
                                           class_weight='balanced'))
        ])
        _results['n_trees'] = n_trees

    elif classifier_type == 'lr':
        clf = Pipeline([
            ('feature_vect', TfidfVectorizer(strip_accents='unicode',
                                             tokenizer=nltk.word_tokenize,
                                             stop_words='english',
                                             decode_error='ignore',
                                             analyzer='word',
                                             norm=l,
                                             ngram_range=(1, 2)
                                             )),
            ('clf', LogisticRegression(penalty=lr_penalty,
                                       C=C,
                                       class_weight='balanced',
                                       random_state=44))
        ])
        _results['lr_penalty'] = lr_penalty
        _results['C'] = C

    else:
        print(f'No model selected......error\n\nInsert {classifier_type} into the space!')
        clf = None

    scores, losses = [], []
    for train_index, test_index in skf.split(X, y):
        # split in train and test set
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        clf.fit(X_train, y_train)
        predicted = clf.predict(X_test)
        score = accuracy_score(y_test, predicted)
        scores.append(score)

    _results['score'] = scores
    acc = np.mean(scores)
    _results['mean_scores'] = acc
    _results['std_score'] = np.std(scores)
    print(f'Averaged accuracy is: {acc}')

    try:
        write_to_json([_results], '28_12_official_CV_model_results.json')
    except:
        print(ValueError)

    return acc


if __name__ == '__main__':
    path = os.path.join(os.getcwd(), 'spam_data', 'spam.csv')
    df = pd.read_csv(path, encoding='latin-1')

    X = df.v2
    y = df.v1

    filtered_search_space = get_search_space()

    best = fmin(
        fn=f,
        space=filtered_search_space,
        algo=tpe.suggest,
        max_evals=MAX_EVALS,
        trials=trials
    )

    print("Found minimum after {} trials:".format(MAX_EVALS))

    os.chdir('..')
    os.chdir('..')
    print(os.getcwd())

    # path_to_save_directories = os.path.join(current_dir_project, '2019', 'phase1_new', 'Models_folder')
    create_models(**space_eval(filtered_search_space, best))
