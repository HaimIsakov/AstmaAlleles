import statsmodels.api as sm
import pandas as pd
from sklearn import preprocessing

housing_dataset = pd.read_csv("Housing.csv")

y_train = housing_dataset.pop('price')
X_train = housing_dataset['area']
X_train_lm = sm.add_constant(X_train)
lm = sm.OLS(y_train, X_train_lm)
lm = lm.fit()
print(lm.summary())