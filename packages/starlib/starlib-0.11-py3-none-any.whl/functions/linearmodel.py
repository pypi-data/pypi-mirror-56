#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 11:30:44 2019

@author: jennstarling

A utility for linear regression, which builds on scikit-learn's model,
but returns coefficients and the vcov matrix, sigma-hat, and residual values for the model.
"""

import numpy as np
import pandas as pd
from patsy import dmatrices, dmatrix
from sklearn.linear_model import LinearRegression


# Linear regression utility.  Can do splines, polynomial, etc - whatever patsy formula you choose.
def lm(formula, dftrain, dftest):
    
    # Create train design matrix and response vector.
    tr = dmatrices(formula, dftrain)
    y_tr = tr[0]
    X_tr = tr[1]
    
    # Create test design matrix and response vector (if y is included in dftest).
    formula_y = formula.split('~')[0].strip()
    formula_x = formula.split('~')[1].strip()
    
    if(formula_y in dftest.columns):
        te = dmatrices(formula, dftest)
        y_te = te[0]
        X_te = te[1]
    else:
        te = dmatrix(formula_x,dftest)
        y_te = np.nan
        X_te = te
    
    # Fit linear model.
    lm = LinearRegression()
    lm.fit(X_tr, y_tr)
    
    # Get yhat values.
    y_hat = lm.predict(X_tr)
    y_pred = lm.predict(X_te)
    
    # Get residuals.
    resids = y_tr - y_hat
    
    ### ------------------------------------
    ### Summary measures.
    ### ------------------------------------
    
    # Number of samples (n) and parameters (p).
    n = np.shape(X_tr)[0]
    p = np.shape(X_tr)[1]
    
    # R-squared.
    R2 = np.asscalar(lm.score(X_tr, y_tr))
    
    # Multiple R-squared.
    SSyy = np.sum((y_tr - np.mean(y_tr))**2)
    SSE = np.sum(resids**2)
    multiple_R2 = np.asscalar(1-SSE/SSyy)
    
    # Adjusted R-squared. 
    # Adjusted R-Squared normalizes Multiple R-Squared by taking into account 
    # how many samples you have and how many variables you’re using.
    k = p-1; # Subtract one to ignore intercept, if intercept included in model.
    if(formula.find("-1")>-1 or formula.find("- 1")>-1):
        k=p  
    adjusted_R2 = np.asscalar(1 - (SSE/SSyy) * (n-1) / (n-(k+1)))
    
    # F-statistic.  The F-Statistic is a “global” test that checks if at least one of your coefficients are nonzero.
    # Ho: All coefficients are zero
    # Ha: At least one coefficient is nonzero
    # Compare test statistic to F Distribution table
    Fstat = np.asscalar(((SSyy-SSE)/k) / (SSE/(n-(k+1))))
    Fstat = pd.DataFrame({"Label":['Fstat','df1','df2'], "Value":[Fstat, k, (n-(k-1))]})


    ### ------------------------------------
    ### Model parameter estimates and variances.
    ### ------------------------------------
    
    # Get sigma_hat estimate.
    sigma_hat = np.asscalar(np.sqrt(np.sum(SSE) / (n-p)))
    
    # Get coefficients and covariance matrix.
    beta = lm.coef_
    beta_vcov = np.linalg.inv(X_tr.transpose() @ X_tr) * (sigma_hat**2)
    beta_se = np.sqrt(np.diag(beta_vcov))
    
    ### ------------------------------------
    ### Return output.
    ### ------------------------------------     
    return{'X_tr':X_tr,
            'y_tr':y_tr,
            'y_hat':y_hat,
            'X_te':X_te,
            'y_pred':y_pred,
            'beta':beta,
            'beta_se':beta_se,
            'beta_vcov':beta_vcov,
            'sigma_hat':sigma_hat,
            'formula':formula,
            'R2':R2,
            'multiple_R2':multiple_R2,
            'adjusted_R2':adjusted_R2,
            'Fstat':Fstat
            }