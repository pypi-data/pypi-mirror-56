
from .analyzer import fan1d


def report(df, outcome, features=None):
    # Create features
    if features is None:
        features = [column for column in df.columns if column != outcome]

    # For every feature, create a FeatureAnalyzer
    for feature in features:
        # Create a FeatureAnalyzer
        fan = fan1d(df[feature], df[outcome], clean=True)

        #




