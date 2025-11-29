from sklearn.base import BaseEstimator, TransformerMixin

class YearToAgeTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, reference_year=2020):
        self.reference_year = reference_year

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        X["Car_Age"] = self.reference_year - X["Year"]
        return X.drop(columns=["Year"])
