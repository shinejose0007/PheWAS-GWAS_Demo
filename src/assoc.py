import pandas as pd
import statsmodels.api as sm
import numpy as np

def per_variant_logistic(genotypes_df, phenotype_series, covariates_df=None):
    results = []
    # ensure index alignment
    phenotype_series = phenotype_series.loc[genotypes_df.index]
    if covariates_df is not None:
        covariates_df = covariates_df.loc[genotypes_df.index]
    for variant in genotypes_df.columns:
        x = genotypes_df[variant].astype(float)
        X = x.to_frame(name=variant)
        if covariates_df is not None:
            X = pd.concat([X, covariates_df], axis=1)
        X = sm.add_constant(X, has_constant='add')
        try:
            model = sm.Logit(phenotype_series.astype(float), X, missing='drop')
            res = model.fit(disp=0)
            pval = res.pvalues[variant]
            coef = res.params[variant]
        except Exception as e:
            pval = np.nan
            coef = np.nan
        results.append({'variant': variant, 'coef': coef, 'pval': pval})
    return pd.DataFrame(results)

def per_variant_linear(genotypes_df, phenotype_series, covariates_df=None):
    results = []
    phenotype_series = phenotype_series.loc[genotypes_df.index]
    if covariates_df is not None:
        covariates_df = covariates_df.loc[genotypes_df.index]
    for variant in genotypes_df.columns:
        x = genotypes_df[variant].astype(float)
        X = x.to_frame(name=variant)
        if covariates_df is not None:
            X = pd.concat([X, covariates_df], axis=1)
        X = sm.add_constant(X, has_constant='add')
        try:
            model = sm.OLS(phenotype_series.astype(float), X, missing='drop')
            res = model.fit()
            pval = res.pvalues[variant]
            coef = res.params[variant]
        except Exception:
            pval = np.nan
            coef = np.nan
        results.append({'variant': variant, 'coef': coef, 'pval': pval})
    return pd.DataFrame(results)
