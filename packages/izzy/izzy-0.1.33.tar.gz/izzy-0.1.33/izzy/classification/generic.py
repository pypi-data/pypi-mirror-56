"""
generic.py
----------

Contains generic model functions and the GenericModel class
"""

from izzy.misc import equal

from abc import ABC
import numpy as np
import pandas as pd
from scipy.linalg import lapack
from scipy.sparse import coo_matrix
from scipy.stats import ks_2samp
from sklearn.metrics import roc_auc_score


# GenericModel class
class GenericModel(ABC):
    """
    GenericModel class. Note that this is an abstract class.
    """

    # Initialize instance of class
    def __init__(self):
        """
        Initialize instance of the GenericModel class
        """

        # Identifier that tells us this in an izzy package
        self._package = 'izzy'

        # Number of observations / features
        self.n_obs = None
        self.n_features = None

        # Class information
        self.classes = None
        self.n_classes = None

    # Compute the log-likelihood from y_true and y_pred
    def _log_likelihood(self, y_true, y_pred, normalize=True):
        """
        Computes the log likelihood from true and predicted outcomes

        Parameters
        ----------
        y_true : ArrayLike
            True outcomes
        y_pred : ArrayLike
            Predicted outcomes
        normalize : bool
            Should we compute the average log likelihood per sample? (Default: True)

        Returns
        -------
        float
            log-likelihood
        """

        # Sanity checking
        assert len(np.unique(y_true)) == self.n_classes == y_pred.shape[1]

        # Transform y_true into an expanded form
        y_true = np.eye(self.n_classes)[np.array([y_true], dtype='int').reshape(-1)]

        # Return log likelihood
        f = np.mean if normalize else np.sum
        return f(np.log(np.sum(y_true * y_pred, axis=1)))

    # Compute the log-loss from y_true and y_pred
    def _log_loss(self, y_true, y_pred, normalize=True):
        """
        Computes the log loss from true and predicted outcomes.

        Parameters
        ----------
        y_true : ArrayLike
            True outcomes
        y_pred : ArrayLike
            Predicted outcomes
        normalize : bool
            Should we normalize by the number of samples? (Default: True)

        Returns
        -------
        float
            log loss
        """

        return -self._log_likelihood(y_true, y_pred, normalize=normalize)

    # Confusion matrix
    def confusion_matrix(self, x, y):
        """
        Computes the confusion matrix

        See :func:`~izzy.classification.confusion_matrix`

        Parameters
        ----------
        x : ArrayLike
            Independent variable(s)
        y : ArrayLike
            Dependent variable(s)

        Returns
        -------
        pandas.DataFrame
            confusion matrix
        """

        # Format x
        x = format_x(x)

        # Return
        return confusion_matrix(y, self.predict_proba(x))

    # Fit the model (NotImplemented)
    def fit(self, *args, **kwargs):
        """
        Implemented in children classes.
        """

        raise NotImplementedError

    # DOF (alias to degrees_of_freedom)
    def dof(self, x):
        """
        Alias to :func:`~degrees_of_freedom`

        Parameters
        ----------
        x : ArrayLike
            Independent variable(s)

        Returns
        -------
        int
            degrees of freedom
        """

        return self.degrees_of_freedom(x)

    # Degrees of freedom (NotImplemented)
    def degrees_of_freedom(self, x):
        """
        Implemented in children classes
        """

        raise NotImplementedError

    # FIM
    def fim(self, x, y):
        """
        Alias of :func:`~fisher_information_matrix`

        Parameters
        ----------
        x : ArrayLike
            Independent variable(s)
        y : ArrayLike
            Dependent variable(s)

        Returns
        -------
        numpy.ndarray
            Fisher information matrix
        """

        return self.fisher_information_matrix(x, y)

    # Fisher
    def fisher(self, x, y):
        """
        Alias of :func:`~fisher_information_matrix`

        Parameters
        ----------
        x : ArrayLike
            Independent variable(s)
        y : ArrayLike
            Dependent variable(s)

        Returns
        -------
        numpy.ndarray
            Fisher information matrix
        """

        return self.fisher_information_matrix(x, y)

    # Fisher information matrix
    def fisher_information_matrix(self, x, y):
        """
        Computes the Fisher information matrix (FIM)

        FIM is the negative Hessian

        Parameters
        ----------
        x : ArrayLike
            Independent variable(s)
        y : ArrayLike
            Dependent variable(s)

        Returns
        -------
        numpy.ndarray
            Fisher information matrix
        """

        return -self.hessian(x, y)

    # Compute the Hessian (NotImplemented)
    def hessian(self, x, y):
        """
        Implemented in children classes
        """

        raise NotImplementedError

    # Information (alias of fisher_information_matrix)
    def information(self, x, y):
        """
        Alias of :func:`~fisher_information_matrix`

        Parameters
        ----------
        x : ArrayLike
            Independent variable(s)
        y : ArrayLike
            Dependent variable(s)

        Returns
        -------
        numpy.ndarray
            Fisher information matrix
        """

        return self.fisher_information_matrix(x, y)

    # Log likelihood
    def log_likelihood(self, x, y, normalize=True):
        """
        Computes the log-likelihood

        Mathematically, for a sample :math:`i`, we compute the likelihood :math:`L_i = p_i^{y_i} (1-p_i)^{1-y_i}.` Here,
        we compute :math:`p` as the predicted probability and :math:`y` as the true outcome.

        We can choose to `normalize` by the number of samples to get the average log likelihood per sample.

        The procedure is to use `x` to get the predicted probabilities, and then compute :math:`L_i` above.

        Note that the log likelihood depends on the specific variables in the model, i.e., cross-comparison of models is
        with different features is technically incorrect.

        Parameters
        ----------
        x : ArrayLike
            Independent variable(s)
        y : ArrayLike
            Dependent variable(s)
        normalize : bool
            Should we normalize by the number of samples? (Default: True)

        Returns
        -------
        float
            log likelihood
        """

        return self._log_likelihood(y, self.predict_proba(x), normalize=normalize)

    # Log loss
    def log_loss(self, x, y):
        """
        Compute the log loss. This is the negative log likelihood. See :func:`~log_likelihood`

        Parameters
        ----------
        x : ArrayLike
            Independent variable(s)
        y : ArrayLike
            Dependent variable(s)

        Returns
        -------
        float
            log loss
        """

        return self._log_loss(y, self.predict_proba(x))

    # Generate performance report
    def performance_report(self, x, y, threshold=0.5):
        """
        Generate a performance report for the model

        Parameters
        ----------
        x : ArrayLike
            Independent variable(s)
        y : ArrayLike
            Dependent variable(s)
        threshold : float
            Decision threshold (Default: 0.5)

        Returns
        -------
        pandas.DataFrame
            performance report
        """

        # Get predicted y values from model
        y_pred = self.predict_proba(x)

        # Get the log-likelihood and degrees of freedom
        log_likelihood = self._log_likelihood(y, y_pred)
        degrees_of_freedom = self.degrees_of_freedom(x)

        # Return performance report
        return performance_report(y, y_pred, log_likelihood, degrees_of_freedom, threshold=threshold)

    # Predict outcome probability (NotImplemented)
    def predict_proba(self, x):
        """
        Implemented in children classes.
        """

        raise NotImplementedError

    # Standard errors of parameters
    # TODO validate standard errors for multiclass?
    def standard_errors(self, x, y, mode='R'):
        """
        Computes the standard errors of parameters

        .. math:: standard errors = \sqrt{diag(covariance matrix)}

        Parameters
        ----------
        x : ArrayLike
            Independent variable(s)
        y : ArrayLike
            Dependent variable(s)
        mode : str
            See `mode` in :func:`~variance_covariance_matrix`

        Returns
        -------
        numpy.ndarray
            standard errors
        """

        return np.sqrt(np.diag(self.variance_covariance_matrix(x, y, mode=mode)))

    # Compute the variance-covariance matrix
    # TODO exclude variables with coefficient = 0
    def variance_covariance_matrix(self, x, y, mode='R'):
        r"""
        Computes the variance-covariance matrix

        The covariance matrix can be calculated in two ways.
            1. `statsmodels` method, which calculates the inverse of the Fisher information matrix (FIM). Note that FIM
               is the negative Hessian, which is equal to the second derivative of the loss function evaluated at the
               maximum likelihood estimate.
            2. `R` method, which calculates the QR decomposition of :math:`x\sqrt{d}`. Here, :math:`d` indicates
               :math:`y_{pred} (1 - y_{pred})`. If there are :math:`n` features, then the Householder reflector
               :math:`h` from QR provides the Cholesky matrix :math:`h[:n, :n]`. The inverse of this matrix gives us the
               covariance. This method, which relies on LAPACK, is *significantly* more efficient than (1).

        https://stats.stackexchange.com/questions/68080/basic-question-about-fisher-information-matrix-and-relationship-to-hessian-and-s
        https://stats.stackexchange.com/questions/224302/how-does-r-function-summary-glm-calculate-the-covariance-matrix-for-glm-model/407734#407734

        Parameters
        ----------
        x : ArrayLike
            Independent variable(s)
        y : ArrayLike
            Dependent variable(s)
        mode : str
            'statsmodels' for covariance computed from the Hessian or 'R' for the Cholesky method (Default: 'R')

        Returns
        -------
        numpy.ndarray
            variance-covariance matrix
        """

        # Right now, we only know how to solve this in the binomial case
        if self.n_classes > 2:
            raise AttributeError('can only solve if binomial')

        # If mode = 'statsmodels'
        if mode == 'statsmodels':
            # Compute Fisher information matrix (FIM)
            fim = self.fisher_information_matrix(x, y)

            # Compute covariance as the inverse of FIM
            cov = np.linalg.pinv(fim)

        # Elif mode = 'R'
        elif mode == 'R':
            # Compute y_prime = p * (1 - p)
            y_prime = np.prod(self.predict_proba(x), axis=1).reshape(-1, 1)

            # Compute QR decomposition ('raw' gets us Householder reflector)
            # TODO we need to add 1 to x here
            q, r = np.linalg.qr(x * np.sqrt(y_prime), mode='raw')

            # Compute covariance from inverse Cholesky (from LAPACK's dpotri function)
            # TODO "4" here is actually the number of columns in x
            cov = lapack.dpotri(q.T[:4, :4])[0]

        # If we get here, we have a problem
        else:
            raise AttributeError('unknown mode')

        # Return covariance
        return cov


# Accuracy computed from confusion matrix
def _accuracy(tp, tn, fp, fn):
    """
    Computes the accuracy from the confusion matrix.

    Parameters
    ----------
    tp : int
        Number of true positives
    tn : int
        Number of true positives
    fp : int
        Number of false positives
    fn : int
        Number of false negatives

    Returns
    -------
    float
        accuracy
    """

    return (tp + tn) / (tp + tn + fp + fn)


# Compute the f1 score from confusion matrix
def _f1(tp, fp, fn, **kwargs):
    """
    Computes the f1 score

    Parameters
    ----------
    tp : int
        Number of true positives
    fp : int
        Number of false positives
    fn : int
        Number of false positions

    Returns
    -------
    float
        f1-score
    """
    return 2. * tp / (2 * tp + fp + fn)


# Format weight
def _format_weight(weight, n=None):
    # If weight and n are None, we have a problem
    if weight is None and n is None:
        raise AttributeError

    # If weight is None, fill with 1s
    if weight is None:
        weight = np.ones(n)

    # Make sure that weight is of length n
    assert len(weight) == n

    # Return
    return weight


# Get tp, tn, fp, fn
def _get_tp_tn_fp_fn(y_true, y_pred, threshold=0.5):
    """
    Compute the confusion matrix and returns as a dictionary

    Parameters
    ----------
    y_true : ArrayLike
        True outcomes
    y_pred : ArrayLike
        Predicted outcomes
    threshold : float
        Cutoff for decision

    Returns
    -------
    dict
        Number of true positions ('tp'), true negatives ('tn'), false positives ('fp'), and false negatives ('fn')
    """
    # Calculate confusion matrix
    cm = confusion_matrix(y_true, y_pred, threshold=threshold)

    # We only know how to do this when we have 2 classes
    assert len(cm.columns) == 2

    # Result
    result = {
        'tp': cm.loc[1, 1],
        'tn': cm.loc[0, 0],
        'fp': cm.loc[0, 1],
        'fn': cm.loc[1, 0]
    }

    # Return result
    return result


# Helper function to compute the precision from the confusion matrix
def _precision(tp, fp, **kwargs):
    """
    Computes the precision from the confusion matrix

    Parameters
    ----------
    tp : int
        Number of true positives
    fp : int
        Number of false positives

    Returns
    -------
    float
        precision
    """

    return tp / (tp + fp)


# Recall
def _recall(tp, fn, **kwargs):
    """
    Computes the recall

    Parameters
    ----------
    tp : int
        True positives
    fn : int
        False negatives

    Returns
    -------
    float
        recall
    """
    return tp / (tp + fn)


# Accuracy
def accuracy(y_true, y_pred, threshold=0.5):
    r"""
    Computes the accuracy of the model

    We compute this by calculating the number of true positives (TP), true negatives (TN), false positives (FP), and
    false negatives (FN).

    Then, :math:`accuracy = \frac{TP+TN}{TP+TN+FP+FN}`.

    Parameters
    ----------
    y_true : ArrayLike
        True outcomes
    y_pred : ArrayLike
        Predicted outcomes
    threshold : float
        Decision boundary (Default: 0.5)

    Returns
    -------
    float
        Accuracy of predicted outcomes
    """

    return _accuracy(**_get_tp_tn_fp_fn(y_true, y_pred, threshold=threshold))


# AIC
def aic(log_likelihood, degrees_of_freedom):
    """
    Computes the Akaike Information Criteria (AIC)

    This function penalizes the log likelihood :math:`L` by the degrees of freedom :math:`D`. Specifically,

    .. math:: AIC = -2L + 2D

    Parameters
    ----------
    log_likelihood : int or float
        The log likelihood
    degrees_of_freedom : int or float
        The degrees of freedom

    Returns
    -------
    float
        AIC
    """

    return 2. * (degrees_of_freedom - log_likelihood)


# Area under ROC curve
def auroc(y_true, y_pred):
    """
    Computes the area under the ROC curve

    Presently, this inherits from :func:`sklearn.metrics.roc_auc_score`

    Parameters
    ----------
    y_true : ArrayLike
        True outcomes.
    y_pred : ArrayLike
        Predicted outcomes

    Returns
    -------
    float
        Area under the ROC curve
    """

    # Return area under ROC curve
    return roc_auc_score(y_true, y_pred)


# BIC
def bic(log_likelihood, degrees_of_freedom, num_samples):
    """
    Computes the Bayesian Information Criteria (BIC)

    This function penalizes the log likelihood :math:`L` by the degrees of freedom :math:`D` and the number of samples
    :math:`N`. Specifically, we compute,

    .. math:: BIC = -2L + Dln(N)

    Parameters
    ----------
    log_likelihood : float
        Log likelihood
    degrees_of_freedom : float
        Degrees of freedom
    num_samples : integer
        Number of observations

    Returns
    -------
    float
        BIC
    """
    return np.log(num_samples) * degrees_of_freedom - 2. * log_likelihood


# Classify
def classify(y_pred, classes=None, threshold=0.5):
    """
    Classify predicted probabilistic outcomes

    Parameters
    ----------
    y_pred : ArrayLike
        Predicted outcomes (expressed as probabilities)
    classes : ArrayLike
        Names of classes (Default: integers from 1 to `n` classes)
    threshold : float
        Decision cutoff, only applied if the number of classes = 2; otherwise, the most likely class is chosen
        (Default: 0.5)

    Returns
    -------
    numpy.ndarray
        classified outcomes
    """

    # Get number of classes
    n_classes = y_pred.shape[1]

    # If classes is not set, set to sequence
    if classes is None:
        classes = np.arange(n_classes)

    # Otherwise, run sanity check and ensure classes is numpy array
    else:
        assert len(classes) == n_classes
        classes = np.array(classes)

    # If binomial, use the threshold
    if y_pred.shape[1] == 2:
        y_pred = np.array(y_pred[:, 1] > threshold, dtype='int')

    # Otherwise, the class is the one with the maximum probability
    else:
        y_pred = np.argmax(y_pred, axis=1)

    # Return class labels
    return classes[y_pred]


# Compute confusion matrix
# TODO allow class_weight
def confusion_matrix(y_true, y_pred, threshold=0.5, sample_weights=None, class_weight=None):
    """
    Computes the confusion matrix

    In the binomial case, this is a 2x2 matrix that shows true vs pred

    Parameters
    ----------
    y_true : ArrayLike
        True outcomes
    y_pred : ArrayLike
        Predicted outcomes
    threshold : float
        Cutoff to turn ``y_pred`` into classes (Default: 0.5)
    sample_weights : ArrayLike
        Weights associated with individual observations
    class_weight : ArrayLike
        Weights associated with classes

    Returns
    -------
    pandas.DataFrame
        Confusion matrix with classes as row and column labels
    """

    # Get classes
    classes = np.unique(y_true)
    n_classes = len(classes)

    # Turn y_pred into class if necessary.
    # WATCH this logic might fail some day
    if n_classes != len(np.unique(y_pred)):
        y_pred = classify(y_pred, classes=classes, threshold=threshold)

    # Weights
    if sample_weights is None:
        sample_weights = np.ones(len(y_true))

    # Create confusion matrix using coo_matrix (this elegant solution is from sklearn)
    cm = coo_matrix((sample_weights, (y_true, y_pred)), shape=(n_classes, n_classes), dtype='int').toarray()

    # Turn into DataFrame and return
    return pd.DataFrame(cm, index=classes, columns=classes)


# f1-score
def f1(y_true, y_pred, threshold=0.5):
    r"""
    Computes the f1 score

    .. math:: f1 = \frac{2}{recall^{-1] + precision^{-1}}

    Parameters
    ----------
    y_true : ArrayLike
        True outcomes
    y_pred : ArrayLike
        Predicted outcomes
    threshold : float
        Decision boundary (Default: 0.5)

    Returns
    -------
    float
        f1 score

    """

    return _f1(**_get_tp_tn_fp_fn(y_true, y_pred, threshold=threshold))


# Format x
def format_x(x):
    # If list or tuple, convert to numpy array
    if isinstance(x, (list, tuple)):
        x = np.array(x)

    # If Series, convert to DataFrame
    if isinstance(x, pd.Series):
        x = pd.DataFrame(x)

    # If ndim = 1, convert to 2D array
    if x.ndim == 1:
        x = x.reshape(-1, 1)

    # We should now have either a pandas DataFrame or numpy array
    assert isinstance(x, (pd.DataFrame, np.ndarray))

    # ndim should also be 2
    assert x.ndim == 2

    # Return
    return x


# Compute Gini coefficient
def gini(y_true, y_pred):
    """
    Computes the Gini coefficient

    Although there is rich literature on Gini, in practice this is simply a function of the area under the ROC
    curve (AUROC).

    .. math:: Gini = 2 * AUROC - 1

    Parameters
    ----------
    y_true : ArrayLike
        True outcomes
    y_pred : ArrayLike
        Predicted outcomes (probabilistic)

    Returns
    -------
    float
        Gini coefficient
    """

    # Return GINI
    return 2. * auroc(y_true, y_pred) - 1.


# Determines if `engine` is an instance of an izzy model instance
def is_model_instance(engine):
    """
    Determines if `engine` is an instance of an izzy model instance.

    Parameters
    ----------
    engine : object
        An izzy model instance.

    Returns
    -------
    bool
        True or False if engine is an izzy instance.
    """

    # Result True if engine is an object that is linked to izzy package
    return isinstance(engine, object) & (getattr(engine, '_package', None) == 'izzy')


# KS statistic
def ks(y_true, y_pred):
    """
    Computes the Kolmogorov-Smirnov (KS) test statistic

    https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test

    Parameters
    ----------
    y_true : ArrayLike
        True y values
    y_pred : ArrayLike
        Predicted y values (expressed as a probability when target outcome is true)

    Returns
    -------
    float
        KS statistic
    """

    # Compute KS statistic
    statistic, p_value = ks_2samp(y_pred[y_true == 0], y_pred[y_true == 1])

    # Return KS statistic
    return statistic


# Compute the precision
def precision(y_true, y_pred, threshold=0.5):
    """
    Computes the precision of the model

    Parameters
    ----------
    y_true : ArrayLike
        True outcomes
    y_pred : ArrayLike
        Predicted outcomes
    threshold: float
        Decision boundary (Default: 0.5)

    Returns
    -------
    float
        precision
    """

    return _precision(**_get_tp_tn_fp_fn(y_true, y_pred, threshold=threshold))


# Compute the recall
def recall(y_true, y_pred, threshold=0.5):
    """
    Computes the recall

    Parameters
    ----------
    y_true : ArrayLike
        True outcomes
    y_pred : ArrayLike
        Predicted outcomes (probabilities)
    threshold : float
        Decision boundary (Default: 0.5)

    Returns
    -------
    float
        recall
    """

    return _recall(**_get_tp_tn_fp_fn(y_true, y_pred, threshold=threshold))


# Generate model performance report
# Note: this is a function (not GenericModel method) for external use
# TODO maybe sent x as argument, so log likelihood and degrees of freedom can be computed in function?
def performance_report(y_true, y_pred, log_likelihood=None, degrees_of_freedom=None, threshold=0.5):
    """
    A performance report for a model.

    Parameters
    ----------
    y_true : ArrayLike
        True outcomes
    y_pred : ArrayLike
        Predicted outcomes (probabilities)
    log_likelihood : float
        (Optional) The log-likelihood of the model
    degrees_of_freedom : float
        (Optional) The number degrees of freedom
    threshold : float
        The cutoff to indicate successful outcomes or not (Default: 0.5)

    Returns
    -------
    pandas.Series
        performance report
    """

    # Empty report container
    report = pd.Series()

    # Accuracy, precision, recall, f1
    cm = _get_tp_tn_fp_fn(y_true, y_pred, threshold=threshold)
    report['accuracy'] = _accuracy(**cm)
    report['precision'] = _precision(**cm)
    report['recall'] = _recall(**cm)
    report['f1'] = _f1(**cm)

    # Log-likelihood?
    if log_likelihood is not None and degrees_of_freedom is not None:
        report['log-likelihood'] = log_likelihood
        report['AIC'] = aic(log_likelihood, degrees_of_freedom)
        report['BIC'] = bic(log_likelihood, degrees_of_freedom, len(y_true))

    # KS statistic (only if n_classes = 2)
    if len(np.unique(y_true)) == 2:
        report['KS'] = ks(y_true, y_pred[:, 1])

    # AUROC / GINI
    report['AUROC'] = auroc(y_true, y_pred)
    report['GINI'] = gini(y_true, y_pred)

    # TODO slope

    # TODO correlation

    # Return report
    return report


# Compute Weight of Evidence
# TODO fill out
# TODO move to features
def weight_of_evidence(x, y, bins=10, mode='equal'):
    pass
