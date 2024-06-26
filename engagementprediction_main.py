# -*- coding: utf-8 -*-
"""EngagementPrediction_Main.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rvWCFjadHWgm4H3MXRzH5WrIWRRviAhx

# File and Library Import

1.1 Importing Necessary Libraries
"""

# Commented out IPython magic to ensure Python compatibility.
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.metrics import roc_curve, auc
from matplotlib.legend_handler import HandlerLine2D
# %matplotlib inline

"""1.2 Importing and loading labeled csv file that is stored in Google Drive to this notebook"""

url='https://drive.google.com/file/d/1V-vIKgmNtQ2f9xpYWkI4qHCvaduwajn2/view?usp=sharing'
url='https://drive.google.com/uc?id=' + url.split('/')[-2]
df = pd.read_csv(url)
df.head()

"""# Dataframe Information Capture"""

df.info()

df['label'].describe()

df['label'].value_counts()

df['T_Words/Turn'].describe()

df['Engagement'].describe()

engagement_array = np.array(df['Engagement'])
print(engagement_array)

df['Engagement'].value_counts()

"""# Dataframe Parameter Corelation Plots and SNS heatmap for Future use with SMOTE"""

df['label'] = df['label'].apply(lambda x: str(x))
plotdf = df.drop(df.columns[1],axis =1)
sns.pairplot(data=plotdf)

plt.figure(figsize=(12,10))
sns.heatmap(df.corr(),cmap='viridis',annot=True,cbar=False)

"""# Random Forest Implementation With Scikit Learn"""

cols_to_drop = ['id', 'label']
df.drop(cols_to_drop, axis=1, inplace=True)

# Define features and target variable
all_features = df.columns[df.columns != 'Engagement']
output_var = 'Engagement'

# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(df[all_features], df[output_var], test_size=0.3, random_state=42)

# Building the RF model
rf_model = RandomForestClassifier(n_estimators=100, max_depth=30)

# Fit model to training data
rf_model.fit(x_train, y_train)

# Model Evaluation

# Accuracy Measure
print("The in-sample accuracy is %0.2f" % accuracy_score(y_train, rf_model.predict(x_train)))
print("The out-of-sample accuracy is %0.2f" % accuracy_score(y_test, rf_model.predict(x_test)))

# Precision Measure
print("The in-sample precision is %0.2f" % precision_score(y_train, rf_model.predict(x_train)))
print("The out-of-sample precision is %0.2f" % precision_score(y_test, rf_model.predict(x_test)))

# Recall Measure
print("The in-sample recall is %0.2f" % recall_score(y_train, rf_model.predict(x_train)))
print("The out-of-sample recall is %0.2f" % recall_score(y_test, rf_model.predict(x_test)))

# ROC and AUC curve
in_sample_prob = rf_model.predict_proba(x_train)[:, 1]
out_sample_prob = rf_model.predict_proba(x_test)[:, 1]
in_sample_fpr, in_sample_tpr, _ = roc_curve(y_train, in_sample_prob)
out_sample_fpr, out_sample_tpr, _ = roc_curve(y_test, out_sample_prob)

print("In-sample AUC is: %0.4f" % auc(in_sample_fpr, in_sample_tpr))
print("Out-of-sample AUC is: %0.4f" % auc(out_sample_fpr, out_sample_tpr))

# Plot ROC curve
plt.figure(figsize=(10, 7))
plt.plot(out_sample_fpr, out_sample_tpr, color='orange', label='Out-sample ROC curve (area= %0.2f)' % auc(out_sample_fpr, out_sample_tpr))
plt.plot(in_sample_fpr, in_sample_tpr, color='blue', label='In-sample ROC curve (area= %0.2f)' % auc(in_sample_fpr, in_sample_tpr))
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve for the RandomForest Model')
plt.legend(loc="lower right")
plt.grid()
plt.show()

# Predictions on the training set
y_pred_train = rf_model.predict(x_train)

# Confusion Matrix
cm_train = confusion_matrix(y_train, y_pred_train)

# Plot the confusion matrix
plt.figure(figsize=(6, 4))
sns.heatmap(cm_train, annot=True, fmt='d', cmap='Blues', xticklabels=['No Engagement', 'Engagement'], yticklabels=['No Engagement', 'Engagement'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix (Training Set)')
plt.show()

# Predictions on the test set
y_pred_test = rf_model.predict(x_test)

# Confusion Matrix
cm_test = confusion_matrix(y_test, y_pred_test)

# Plot the confusion matrix
plt.figure(figsize=(6, 4))
sns.heatmap(cm_test, annot=True, fmt='d', cmap='Blues', xticklabels=['No Engagement', 'Engagement'], yticklabels=['No Engagement', 'Engagement'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix (Test Set)')
plt.show()

"""# Model Saving"""

from joblib import dump, load

# Save the trained Random Forest model to a file
dump(rf_model, 'random_forest_model.joblib')

# Load the trained Random Forest model from the file
loaded_rf_model = load('random_forest_model.joblib')

# Use the loaded model for predictions
loaded_model_predictions = loaded_rf_model.predict(x_test)

# Model Evaluation using the loaded model
loaded_in_sample_prob = loaded_rf_model.predict_proba(x_train)[:, 1]
loaded_out_sample_prob = loaded_rf_model.predict_proba(x_test)[:, 1]
loaded_in_sample_fpr, loaded_in_sample_tpr, _ = roc_curve(y_train, loaded_in_sample_prob)
loaded_out_sample_fpr, loaded_out_sample_tpr, _ = roc_curve(y_test, loaded_out_sample_prob)

print("Loaded In-sample AUC is: %0.4f" % auc(loaded_in_sample_fpr, loaded_in_sample_tpr))
print("Loaded Out-of-sample AUC is: %0.4f" % auc(loaded_out_sample_fpr, loaded_out_sample_tpr))

# Plot ROC curve for the loaded model
plt.figure(figsize=(10, 7))
plt.plot(loaded_out_sample_fpr, loaded_out_sample_tpr, color='orange', label='Loaded Out-sample ROC curve (area= %0.2f)' % auc(loaded_out_sample_fpr, loaded_out_sample_tpr))
plt.plot(loaded_in_sample_fpr, loaded_in_sample_tpr, color='blue', label='Loaded In-sample ROC curve (area= %0.2f)' % auc(loaded_in_sample_fpr, loaded_in_sample_tpr))
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve for the Loaded RandomForest Model')
plt.legend(loc="lower right")
plt.grid()
plt.show()

"""# Random Forest Parameter Tuning"""

# Additional code for evaluating different numbers of estimators
n_estimators = [1, 2, 4, 8, 16, 32, 64, 100, 200]
train_results = []
test_results = []

for estimator in n_estimators:
    rf = RandomForestClassifier(n_estimators=estimator, n_jobs=-1)
    rf.fit(x_train, y_train)

    # Training set
    train_pred = rf.predict(x_train)
    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_train, train_pred)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    train_results.append(roc_auc)

    # Testing set
    y_pred = rf.predict(x_test)
    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_pred)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    test_results.append(roc_auc)

# Plotting AUC scores for different numbers of estimators
line1, = plt.plot(n_estimators, train_results, 'b', label="Train AUC")
line2, = plt.plot(n_estimators, test_results, 'r', label="Test AUC")

plt.legend(handler_map={line1: HandlerLine2D(numpoints=2)})
plt.ylabel('AUC score')
plt.xlabel('n_estimators')
plt.show()

max_depths = np.arange(1, 33)  # Generate an array of integers from 1 to 32
train_results = []
test_results = []

for max_depth in max_depths:
    rf = RandomForestClassifier(max_depth=max_depth, n_jobs=-1)
    rf.fit(x_train, y_train)

    train_pred = rf.predict(x_train)
    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_train, train_pred)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    train_results.append(roc_auc)

    y_pred = rf.predict(x_test)
    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_pred)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    test_results.append(roc_auc)

from matplotlib.legend_handler import HandlerLine2D
line1, = plt.plot(max_depths, train_results, 'b', label="Train AUC")
line2, = plt.plot(max_depths, test_results, 'r', label="Test AUC")

plt.legend(handler_map={line1: HandlerLine2D(numpoints=2)})
plt.ylabel('AUC score')
plt.xlabel('Tree depth')
plt.show()

min_samples_splits = np.linspace(0.1, 1.0, 10, endpoint=True)
train_results = []
test_results = []

for min_samples_split in min_samples_splits:
    rf = RandomForestClassifier(min_samples_split=min_samples_split)
    rf.fit(x_train, y_train)

    train_pred = rf.predict(x_train)
    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_train, train_pred)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    train_results.append(roc_auc)

    y_pred = rf.predict(x_test)
    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_pred)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    test_results.append(roc_auc)

from matplotlib.legend_handler import HandlerLine2D
line1, = plt.plot(min_samples_splits, train_results, 'b', label="Train AUC")
line2, = plt.plot(min_samples_splits, test_results, 'r', label="Test AUC")

plt.legend(handler_map={line1: HandlerLine2D(numpoints=2)})
plt.ylabel('AUC score')
plt.xlabel('min samples split')
plt.show()

min_samples_leafs = np.linspace(0.1, 0.5, 5, endpoint=True)
train_results = []
test_results = []

for min_samples_leaf in min_samples_leafs:
    rf = RandomForestClassifier(min_samples_leaf=min_samples_leaf)
    rf.fit(x_train, y_train)

    train_pred = rf.predict(x_train)
    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_train, train_pred)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    train_results.append(roc_auc)

    y_pred = rf.predict(x_test)
    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_pred)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    test_results.append(roc_auc)

from matplotlib.legend_handler import HandlerLine2D
line1, = plt.plot(min_samples_leafs, train_results, 'b', label="Train AUC")
line2, = plt.plot(min_samples_leafs, test_results, 'r', label="Test AUC")

plt.legend(handler_map={line1: HandlerLine2D(numpoints=2)})
plt.ylabel('AUC score')
plt.xlabel('min samples leaf')
plt.show()

max_features = list(range(1, x_train.shape[1]))
train_results = []
test_results = []

for max_feature in max_features:
    rf = RandomForestClassifier(max_features=max_feature)
    rf.fit(x_train, y_train)

    train_pred = rf.predict(x_train)
    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_train, train_pred)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    train_results.append(roc_auc)

    y_pred = rf.predict(x_test)
    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_pred)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    test_results.append(roc_auc)

from matplotlib.legend_handler import HandlerLine2D
line1, = plt.plot(max_features, train_results, 'b', label="Train AUC")
line2, = plt.plot(max_features, test_results, 'r', label="Test AUC")

plt.legend(handler_map={line1: HandlerLine2D(numpoints=2)})
plt.ylabel('AUC score')
plt.xlabel('max features')
plt.show()

"""# Comparison between

*   Logistic Regression
*   KNeighborsClassifier
*   Random Forest
*   List item




"""

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_curve, auc
import matplotlib.pyplot as plt

# Create instances of the models
lr_model = LogisticRegression()
knn_model = KNeighborsClassifier(n_neighbors=5)  # You can adjust the number of neighbors as needed

# Fit models to training data
lr_model.fit(x_train, y_train)
knn_model.fit(x_train, y_train)

# Model Evaluation

# Linear Regression Model
print("\nLinear Regression Model:")
# Accuracy Measure
print("The in-sample accuracy is %0.2f" % accuracy_score(y_train, lr_model.predict(x_train)))
print("The out-of-sample accuracy is %0.2f" % accuracy_score(y_test, lr_model.predict(x_test)))

# Precision Measure
print("The in-sample precision is %0.2f" % precision_score(y_train, lr_model.predict(x_train)))
print("The out-of-sample precision is %0.2f" % precision_score(y_test, lr_model.predict(x_test)))

# Recall Measure
print("The in-sample recall is %0.2f" % recall_score(y_train, lr_model.predict(x_train)))
print("The out-of-sample recall is %0.2f" % recall_score(y_test, lr_model.predict(x_test)))

# ROC and AUC curve
lr_in_sample_prob = lr_model.predict_proba(x_train)[:, 1]
lr_out_sample_prob = lr_model.predict_proba(x_test)[:, 1]
lr_in_sample_fpr, lr_in_sample_tpr, _ = roc_curve(y_train, lr_in_sample_prob)
lr_out_sample_fpr, lr_out_sample_tpr, _ = roc_curve(y_test, lr_out_sample_prob)

print("In-sample AUC is: %0.4f" % auc(lr_in_sample_fpr, lr_in_sample_tpr))
print("Out-of-sample AUC is: %0.4f" % auc(lr_out_sample_fpr, lr_out_sample_tpr))

# K-Nearest Neighbors Model
print("\nK-Nearest Neighbors Model:")
# Accuracy Measure
print("The in-sample accuracy is %0.2f" % accuracy_score(y_train, knn_model.predict(x_train)))
print("The out-of-sample accuracy is %0.2f" % accuracy_score(y_test, knn_model.predict(x_test)))

# Precision Measure
print("The in-sample precision is %0.2f" % precision_score(y_train, knn_model.predict(x_train)))
print("The out-of-sample precision is %0.2f" % precision_score(y_test, knn_model.predict(x_test)))

# Recall Measure
print("The in-sample recall is %0.2f" % recall_score(y_train, knn_model.predict(x_train)))
print("The out-of-sample recall is %0.2f" % recall_score(y_test, knn_model.predict(x_test)))

# ROC and AUC curve
knn_in_sample_prob = knn_model.predict_proba(x_train)[:, 1]
knn_out_sample_prob = knn_model.predict_proba(x_test)[:, 1]
knn_in_sample_fpr, knn_in_sample_tpr, _ = roc_curve(y_train, knn_in_sample_prob)
knn_out_sample_fpr, knn_out_sample_tpr, _ = roc_curve(y_test, knn_out_sample_prob)

print("In-sample AUC is: %0.4f" % auc(knn_in_sample_fpr, knn_in_sample_tpr))
print("Out-of-sample AUC is: %0.4f" % auc(knn_out_sample_fpr, knn_out_sample_tpr))

# Plot ROC curves for all models
plt.figure(figsize=(15, 10))

# RandomForest Model
plt.plot(out_sample_fpr, out_sample_tpr, color='orange', label='RandomForest (area= %0.2f)' % auc(out_sample_fpr, out_sample_tpr))

# Linear Regression Model
plt.plot(lr_out_sample_fpr, lr_out_sample_tpr, color='green', label='Linear Regression (area= %0.2f)' % auc(lr_out_sample_fpr, lr_out_sample_tpr))

# K-Nearest Neighbors Model
plt.plot(knn_out_sample_fpr, knn_out_sample_tpr, color='red', label='K-Nearest Neighbors (area= %0.2f)' % auc(knn_out_sample_fpr, knn_out_sample_tpr))

plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curves for Different Models')
plt.legend

"""# RF - Feature Importance"""

# Get feature importances from the trained model
feature_importances = rf_model.feature_importances_

# Create a DataFrame to display feature names and their importance scores
feature_importance_df = pd.DataFrame({'Feature': all_features, 'Importance': feature_importances})

# Sort the DataFrame by importance in descending order
feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)

# Print or display the sorted feature importance DataFrame
print(feature_importance_df)

"""# Feature Correalation on trained model"""

# Calculate the correlation matrix for the features
feature_corr_matrix = df[all_features].corr()

# Plot the correlation matrix as a heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(feature_corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=.5)
plt.title('Feature Correlation Matrix')
plt.show()

"""# Logistic Regression"""

from sklearn.linear_model import LogisticRegression

# Building the Logistic Regression model
logreg_model = LogisticRegression()

# Fit the model to training data
logreg_model.fit(x_train, y_train)

# Model Evaluation

# Accuracy Measure
print("The in-sample accuracy is %0.2f" % accuracy_score(y_train, logreg_model.predict(x_train)))
print("The out-of-sample accuracy is %0.2f" % accuracy_score(y_test, logreg_model.predict(x_test)))

# Precision Measure
print("The in-sample precision is %0.2f" % precision_score(y_train, logreg_model.predict(x_train)))
print("The out-of-sample precision is %0.2f" % precision_score(y_test, logreg_model.predict(x_test)))

# Recall Measure
print("The in-sample recall is %0.2f" % recall_score(y_train, logreg_model.predict(x_train)))
print("The out-of-sample recall is %0.2f" % recall_score(y_test, logreg_model.predict(x_test)))

# ROC and AUC curve
in_sample_prob = logreg_model.predict_proba(x_train)[:, 1]
out_sample_prob = logreg_model.predict_proba(x_test)[:, 1]
in_sample_fpr, in_sample_tpr, _ = roc_curve(y_train, in_sample_prob)
out_sample_fpr, out_sample_tpr, _ = roc_curve(y_test, out_sample_prob)

print("In-sample AUC is: %0.4f" % auc(in_sample_fpr, in_sample_tpr))
print("Out-of-sample AUC is: %0.4f" % auc(out_sample_fpr, out_sample_tpr))

# Plot ROC curve
plt.figure(figsize=(10, 7))
plt.plot(out_sample_fpr, out_sample_tpr, color='orange', label='Out-sample ROC curve (area= %0.2f)' % auc(out_sample_fpr, out_sample_tpr))
plt.plot(in_sample_fpr, in_sample_tpr, color='blue', label='In-sample ROC curve (area= %0.2f)' % auc(in_sample_fpr, in_sample_tpr))
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve for the Logistic Regression Model')
plt.legend(loc="lower right")
plt.grid()
plt.show()

"""# Logistic Regression Tuning"""

from sklearn.model_selection import GridSearchCV

# Define the parameter grid to search
param_grid = {
    'penalty': ['l1', 'l2'],
    'C': [0.001, 0.01, 0.1, 1, 10, 100],
    'solver': ['liblinear', 'lbfgs']
}

# Create the logistic regression model
logreg_model = LogisticRegression()

# Create GridSearchCV
grid_search = GridSearchCV(logreg_model, param_grid, cv=5, scoring='accuracy')

# Fit the grid search to the data
grid_search.fit(x_train, y_train)

# Print the best parameters
print("Best Parameters: ", grid_search.best_params_)

# Evaluate the model with best parameters
best_logreg_model = grid_search.best_estimator_

# Model Evaluation

# Accuracy Measure
print("The in-sample accuracy is %0.2f" % accuracy_score(y_train, best_logreg_model.predict(x_train)))
print("The out-of-sample accuracy is %0.2f" % accuracy_score(y_test, best_logreg_model.predict(x_test)))

# Precision Measure
print("The in-sample precision is %0.2f" % precision_score(y_train, best_logreg_model.predict(x_train)))
print("The out-of-sample precision is %0.2f" % precision_score(y_test, best_logreg_model.predict(x_test)))

# Recall Measure
print("The in-sample recall is %0.2f" % recall_score(y_train, best_logreg_model.predict(x_train)))
print("The out-of-sample recall is %0.2f" % recall_score(y_test, best_logreg_model.predict(x_test)))

# ROC and AUC curve
in_sample_prob = best_logreg_model.predict_proba(x_train)[:, 1]
out_sample_prob = best_logreg_model.predict_proba(x_test)[:, 1]
in_sample_fpr, in_sample_tpr, _ = roc_curve(y_train, in_sample_prob)
out_sample_fpr, out_sample_tpr, _ = roc_curve(y_test, out_sample_prob)

print("In-sample AUC is: %0.4f" % auc(in_sample_fpr, in_sample_tpr))
print("Out-of-sample AUC is: %0.4f" % auc(out_sample_fpr, out_sample_tpr))

# Plot ROC curve
plt.figure(figsize=(10, 7))
plt.plot(out_sample_fpr, out_sample_tpr, color='orange', label='Out-sample ROC curve (area= %0.2f)' % auc(out_sample_fpr, out_sample_tpr))
plt.plot(in_sample_fpr, in_sample_tpr, color='blue', label='In-sample ROC curve (area= %0.2f)' % auc(in_sample_fpr, in_sample_tpr))
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve for the Tuned Logistic Regression Model')
plt.legend(loc="lower right")
plt.grid()
plt.show()

"""# Predicting Engagement on labeled csv omitting engagement column"""

url='https://drive.google.com/file/d/1DMhXFAUdcosPNY_tEGPyJv-8kcpZuKN6/view?usp=sharing'
url='https://drive.google.com/uc?id=' + url.split('/')[-2]
new_data = pd.read_csv(url)
new_data.head()

cols_to_drop_new_data = ['id', 'label']
new_data.drop(cols_to_drop_new_data, axis=1, inplace=True)

# Make predictions
new_predictions = rf_model.predict(new_data[all_features])

# Print or use the predictions as needed
print(new_predictions)

"""# Comparison  between actual and predicted engagement value"""

actual_values = [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0]

predicted_values = [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0]

# Display the actual and predicted values side by side
for actual, predicted in zip(actual_values, predicted_values):
    print("Actual: {}, Predicted: {}".format(actual, predicted))

from sklearn.metrics import accuracy_score

# Calculate accuracy
accuracy = accuracy_score(actual_values, predicted_values)

print("Accuracy: {:.2%}".format(accuracy))

"""# SMOTE"""

from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
import pandas as pd

# Assuming df is your original DataFrame

# Define features and target variable
all_features = df.columns[df.columns != 'Engagement']
output_var = 'Engagement'

# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(df[all_features], df[output_var], test_size=0.4, random_state=42)
# Apply SMOTE to the training data
smote = SMOTE(random_state=42)
x_train_resampled, y_train_resampled = smote.fit_resample(x_train, y_train)

# Concatenate the resampled data to create a new DataFrame
df_resampled = pd.concat([pd.DataFrame(x_train_resampled, columns=all_features), pd.Series(y_train_resampled, name=output_var)], axis=1)

# Check the class distribution in the resampled DataFrame
print(df_resampled['Engagement'].value_counts())

df_resampled.head(25)

"""# SMOTE Accuracy"""

x_resampled = df_resampled[all_features]
y_resampled = df_resampled[output_var]

# Predict engagement using the trained RF model
predictions_resampled = rf_model.predict(x_resampled)

# Calculate accuracy on the resampled data
accuracy_resampled = accuracy_score(y_resampled, predictions_resampled)

print("Accuracy on the resampled data: {:.2f}".format(accuracy_resampled))

"""# SMOTE Before-After Plots"""

import matplotlib.pyplot as plt
import seaborn as sns

# Plot histograms for each feature before and after SMOTE
fig, axs = plt.subplots(nrows=2, ncols=len(all_features), figsize=(15, 6))

# Plot histograms before SMOTE
for i, feature in enumerate(all_features):
    sns.histplot(df[feature], ax=axs[0, i], kde=True, color='blue', bins=20)
    axs[0, i].set_title(f'Before SMOTE\n{feature}')

# Plot histograms after SMOTE
for i, feature in enumerate(all_features):
    sns.histplot(df_resampled[feature], ax=axs[1, i], kde=True, color='orange', bins=20)
    axs[1, i].set_title(f'After SMOTE\n{feature}')

plt.tight_layout()
plt.show()

# Predict engagement using the trained RF model on the resampled data
predictions_resampled = rf_model.predict(x_resampled)

# Calculate accuracy on the resampled data
accuracy_resampled = accuracy_score(y_resampled, predictions_resampled)

# Confusion Matrix
cm_resampled = confusion_matrix(y_resampled, predictions_resampled)

# Plot the confusion matrix
plt.figure(figsize=(6, 4))
sns.heatmap(cm_resampled, annot=True, fmt='d', cmap='Blues', xticklabels=['No Engagement', 'Engagement'], yticklabels=['No Engagement', 'Engagement'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix (After SMOTE)')
plt.show()

print("Accuracy on the resampled data: {:.2f}".format(accuracy_resampled))