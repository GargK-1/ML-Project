# -*- coding: utf-8 -*-
"""
Task 1.1
"""

pip install numpy pandas

import numpy
import pandas as pd

# Load the datasets
train_data = pd.read_csv('train_emoticon.csv')
valid_data = pd.read_csv('valid_emoticon.csv')
test_data = pd.read_csv('test_emoticon.csv')

# Display the first few rows of each dataset to understand their structure
train_data.head(), valid_data.head(), test_data.head()

"""# New Section"""

pip install scikit-learn

from sklearn.feature_extraction.text import CountVectorizer
print("scikit-learn is installed and the module is accessible!")

# Final code for training logistic regression with varying amounts of training data

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# Parameters
train_file = 'train_emoticon.csv'
valid_file = 'valid_emoticon.csv'
max_iter = 1000
random_state = 42
train_percentages = [0.2, 0.4, 0.6, 0.8, 1.0]

# Load datasets
train_data = pd.read_csv(train_file)
valid_data = pd.read_csv(valid_file)

# Extract features and labels
X_train = train_data['input_emoticon']
y_train = train_data['label']
X_valid = valid_data['input_emoticon']
y_valid = valid_data['label']

# Use CountVectorizer to transform each character (emoji) into a feature
vectorizer = CountVectorizer(analyzer='char')
X_train_vec = vectorizer.fit_transform(X_train)
X_valid_vec = vectorizer.transform(X_valid)

# List to store accuracy results
accuracies = []

# Train logistic regression model on varying portions of the training data
for pct in train_percentages:
    # Subset of the training data
    subset_size = int(pct * len(X_train))
    X_train_subset = X_train_vec[:subset_size]
    y_train_subset = y_train[:subset_size]

    # Train model
    model = LogisticRegression(max_iter=max_iter, random_state=random_state)
    model.fit(X_train_subset, y_train_subset)

    # Evaluate on validation set
    y_valid_pred = model.predict(X_valid_vec)
    accuracy = accuracy_score(y_valid, y_valid_pred)
    accuracies.append(accuracy)

# Plot results
plt.figure(figsize=(10, 6))
plt.plot([int(p * 100) for p in train_percentages], accuracies, marker='o', linestyle='-')
plt.title('Validation Accuracy vs. Training Data Percentage')
plt.xlabel('Percentage of Training Data Used')
plt.ylabel('Validation Accuracy')
plt.grid(True)
plt.show()

"""it uses scikit-learn's LogisticRegression class, which performs binary classification by estimating the probability that a given input belongs to a particular class. The model is configured to:

Treat each emoji as a distinct feature (using a character-level CountVectorizer).
Train with the max_iter parameter set to allow for up to 1,000 iterations to ensure convergence.
Use a random_state to ensure reproducible results.
"""

from sklearn.svm import SVC

# List to store accuracy results for SVM
svm_accuracies = []

# Train SVM model on varying portions of the training data
for pct in train_percentages:
    # Subset of the training data
    subset_size = int(pct * len(X_train))
    X_train_subset = X_train_vec[:subset_size]
    y_train_subset = y_train[:subset_size]

    # Train SVM model
    svm_model = SVC(kernel='linear', random_state=random_state)
    svm_model.fit(X_train_subset, y_train_subset)

    # Evaluate on validation set
    y_valid_pred = svm_model.predict(X_valid_vec)
    accuracy = accuracy_score(y_valid, y_valid_pred)
    svm_accuracies.append(accuracy)

# Plot results
plt.figure(figsize=(10, 6))
plt.plot([int(p * 100) for p in train_percentages], svm_accuracies, marker='o', linestyle='-', color='orange')
plt.title('Validation Accuracy vs. Training Data Percentage (SVM)')
plt.xlabel('Percentage of Training Data Used')
plt.ylabel('Validation Accuracy')
plt.grid(True)
plt.show()

"""The plot illustrates how the validation accuracy of the SVM model changes as we increase the percentage of training data used. Here’s a breakdown of what the results suggest:

1. **Increasing Training Data Improves Accuracy**: Generally, as more training data is used (from 20% to 100%), the model’s accuracy improves on the validation set. This trend is typical because more data helps the model capture more patterns and variability, which leads to better performance.

2. **Stabilization of Accuracy**: You may notice that beyond a certain point (often between 80% and 100% in similar cases), the accuracy may start to level off. This suggests that the model has learned most of the meaningful patterns it can, and additional data doesn’t significantly improve its performance. In this case, if the accuracy stabilizes, it may indicate that the model has reached its optimal performance level given the features and data format.

3. **SVM with a Linear Kernel**: The choice of a linear kernel in the SVM model is often effective for text-like data (such as emojis in this case) where classes can be linearly separated in a higher-dimensional space. If this model did improve over the logistic regression model, it suggests that the SVM is better at distinguishing between the two classes within the current feature set.

4. **Comparison to Logistic Regression**: If the SVM model performs consistently better than logistic regression at each training percentage, it may indicate that SVM is a better choice for this particular dataset. SVMs are known for finding the optimal separating hyperplane, which can be more effective for certain types of data, especially when the classes are not perfectly linearly separable.

In summary, this analysis suggests that SVM can better handle the features extracted from emoji data and benefits from additional data up to a point. You can choose to stick with SVM if it shows robust performance, or experiment further with other models or feature extraction methods if higher accuracy is needed.

# The dip in accuracy that sometimes appears when using higher percentages of training data can occur due to several reasons:

### 1. **Overfitting and Model Complexity**:
   - As the model trains on more data, it might start to fit noise or irrelevant patterns in the training set, particularly if the additional data is not perfectly representative of the validation set. This overfitting can cause the model's performance on the validation set to decrease slightly.
   - While SVMs are generally less prone to overfitting than some other models, they can still exhibit overfitting if the data is noisy or has complex patterns that aren't consistently present in the validation set.

### 2. **Class Imbalance in Data Subsets**:
   - Depending on how the training data is split, the smaller subsets might be more balanced or have specific characteristics that suit the model well. As more data is added, there could be a shift in the balance or distribution of features, which can affect the model's ability to generalize if the newly added data is more complex or noisy.
   - For example, if the first 20% or 40% of the data has simpler, clearer patterns that the model learns well, introducing more complex data at 60%, 80%, or 100% could challenge the model’s learned patterns, causing a temporary dip.

### 3. **Validation Data Characteristics**:
   - If the validation set has patterns that are somewhat different from those in the additional training data, the model might struggle with the new data it’s trained on. The new data could, for example, introduce variations in emoji combinations that do not match as well with what’s in the validation set, affecting accuracy.
   
### 4. **Random Variation**:
   - Small fluctuations in accuracy can happen due to inherent randomness, especially if the dataset is relatively small. The model's performance might naturally vary slightly as the amount of data used changes, even if there isn’t a significant underlying pattern to this dip.
   
In this case, the dip might suggest that while more training data is beneficial up to a point, some of the later data could be introducing patterns that don’t align as well with the validation set or could be creating a mild overfitting effect. To mitigate this, regularization (adjusting the `C` parameter in SVM) or a careful evaluation of the data's consistency across splits may help stabilize performance.
"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

# Use TF-IDF Vectorizer to capture unique emoji patterns with importance weights
tfidf_vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(1, 2))  # Considering unigrams and bigrams of characters
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_valid_tfidf = tfidf_vectorizer.transform(X_valid)

# Parameters for the Random Forest
n_estimators = 100  # Number of trees in the forest
max_depth = None  # Let trees grow until they contain fewer than min_samples_split samples

# List to store accuracy results
rf_accuracies = []

# Train Random Forest on varying portions of the training data
for pct in train_percentages:
    # Subset of the training data
    subset_size = int(pct * len(X_train))
    X_train_subset = X_train_tfidf[:subset_size]
    y_train_subset = y_train[:subset_size]

    # Train Random Forest model
    rf_model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=random_state)
    rf_model.fit(X_train_subset, y_train_subset)

    # Evaluate on validation set
    y_valid_pred = rf_model.predict(X_valid_tfidf)
    accuracy = accuracy_score(y_valid, y_valid_pred)
    rf_accuracies.append(accuracy)

# Plot results
plt.figure(figsize=(10, 6))
plt.plot([int(p * 100) for p in train_percentages], rf_accuracies, marker='o', linestyle='-', color='green')
plt.title('Validation Accuracy vs. Training Data Percentage (Random Forest with TF-IDF)')
plt.xlabel('Percentage of Training Data Used')
plt.ylabel('Validation Accuracy')
plt.grid(True)
plt.show()

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Embedding, LSTM, Dense, Input, concatenate, Dropout
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.callbacks import EarlyStopping

# Load datasets
train_file = 'train_emoticon.csv'
valid_file = 'valid_emoticon.csv'
train_data = pd.read_csv(train_file)
valid_data = pd.read_csv(valid_file)

# Extract features and labels
X_train = train_data['input_emoticon']
y_train = train_data['label']

# 1. Emoji Embedding Preparation
# Create a Tokenizer for emojis
tokenizer = Tokenizer(char_level=True, filters='')
tokenizer.fit_on_texts(X_train)
X_train_seq = tokenizer.texts_to_sequences(X_train)

# Pad sequences to ensure uniform input length
max_seq_len = max(len(seq) for seq in X_train_seq)
X_train_pad = pad_sequences(X_train_seq, maxlen=max_seq_len, padding='post')

# Define embedding size
embedding_dim = 16
vocab_size = len(tokenizer.word_index) + 1

# 2. TF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(1, 3))
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train).toarray()

# 3. Cross-Validation Setup
kfold = KFold(n_splits=5, shuffle=True, random_state=42)
accuracies = []

for train_index, val_index in kfold.split(X_train_pad):
    # Split data
    X_train_cv, X_val_cv = X_train_pad[train_index], X_train_pad[val_index]
    X_train_tfidf_cv, X_val_tfidf_cv = X_train_tfidf[train_index], X_train_tfidf[val_index]
    y_train_cv, y_val_cv = np.array(y_train)[train_index], np.array(y_train)[val_index]

    # Define LSTM Model with Embedding and TF-IDF
    embedding_input = Input(shape=(max_seq_len,))
    tfidf_input = Input(shape=(X_train_tfidf.shape[1],))

    # Emoji embedding and LSTM layer
    embedded = Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_seq_len)(embedding_input)
    lstm_out = LSTM(32)(embedded)

    # Merge TF-IDF with LSTM output
    combined = concatenate([lstm_out, tfidf_input])
    combined = Dropout(0.5)(combined)
    combined = Dense(64, activation='relu')(combined)
    combined = Dense(32, activation='relu')(combined)
    output = Dense(1, activation='sigmoid')(combined)

    model = Model(inputs=[embedding_input, tfidf_input], outputs=output)

    # Compile model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Fit model with early stopping
    early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
    model.fit([X_train_cv, X_train_tfidf_cv], y_train_cv, validation_data=([X_val_cv, X_val_tfidf_cv], y_val_cv),
              epochs=20, batch_size=32, callbacks=[early_stopping], verbose=1)

    # Predict and evaluate
    y_val_pred = (model.predict([X_val_cv, X_val_tfidf_cv]) > 0.5).astype(int)
    accuracy = accuracy_score(y_val_cv, y_val_pred)
    accuracies.append(accuracy)

# Calculate and print average accuracy across folds
avg_accuracy = np.mean(accuracies)
print(f'Average Cross-Validation Accuracy: {avg_accuracy * 100:.2f}%')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Embedding, LSTM, Dense, Input, concatenate, Dropout
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.callbacks import EarlyStopping

# Load datasets
train_file = 'train_emoticon.csv'
train_data = pd.read_csv(train_file)

# Extract features and labels
X_train = train_data['input_emoticon']
y_train = train_data['label']

# Define proportions of data to use
train_percentages = [0.2, 0.4, 0.6, 0.8, 1.0]
accuracies = []

# 1. Emoji Embedding Preparation
# Create a Tokenizer for emojis
tokenizer = Tokenizer(char_level=True, filters='')
tokenizer.fit_on_texts(X_train)
X_train_seq = tokenizer.texts_to_sequences(X_train)

# Pad sequences to ensure uniform input length
max_seq_len = max(len(seq) for seq in X_train_seq)
X_train_pad = pad_sequences(X_train_seq, maxlen=max_seq_len, padding='post')

# Define embedding size
embedding_dim = 16
vocab_size = len(tokenizer.word_index) + 1

# 2. TF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(1, 3))
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train).toarray()

# Loop over each training size percentage
for pct in train_percentages:
    # Calculate subset size
    subset_size = int(pct * len(X_train))

    # Create subset of training data
    X_train_subset_pad = X_train_pad[:subset_size]
    X_train_subset_tfidf = X_train_tfidf[:subset_size]
    y_train_subset = np.array(y_train)[:subset_size]

    # Define LSTM Model with Embedding and TF-IDF
    embedding_input = Input(shape=(max_seq_len,))
    tfidf_input = Input(shape=(X_train_tfidf.shape[1],))

    # Emoji embedding and LSTM layer
    embedded = Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_seq_len)(embedding_input)
    lstm_out = LSTM(32)(embedded)

    # Merge TF-IDF with LSTM output
    combined = concatenate([lstm_out, tfidf_input])
    combined = Dropout(0.5)(combined)
    combined = Dense(64, activation='relu')(combined)
    combined = Dense(32, activation='relu')(combined)
    output = Dense(1, activation='sigmoid')(combined)

    model = Model(inputs=[embedding_input, tfidf_input], outputs=output)

    # Compile model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Fit model with early stopping
    early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
    model.fit([X_train_subset_pad, X_train_subset_tfidf], y_train_subset,
              epochs=20, batch_size=32, validation_split=0.2, callbacks=[early_stopping], verbose=1)

    # Predict and evaluate on the validation set (using validation data from the split above)
    val_predictions = model.predict([X_train_subset_pad, X_train_subset_tfidf])[-len(y_train_subset):]
    y_val_pred = (val_predictions > 0.5).astype(int)
    accuracy = accuracy_score(y_train_subset[-len(y_val_pred):], y_val_pred)
    accuracies.append(accuracy)
    print(f'Accuracy with {int(pct*100)}% training data: {accuracy * 100:.2f}%')

# Plotting Accuracy vs Training Data Percentage
plt.figure(figsize=(10, 6))
plt.plot([int(p * 100) for p in train_percentages], accuracies, marker='o', linestyle='-', color='blue')
plt.title('Validation Accuracy vs. Training Data Percentage')
plt.xlabel('Percentage of Training Data Used')
plt.ylabel('Validation Accuracy')
plt.grid(True)
plt.show()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Embedding, LSTM, Dense, Input, concatenate, Dropout
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.callbacks import EarlyStopping

# Load datasets
train_file = 'train_emoticon.csv'
train_data = pd.read_csv(train_file)

# Load test dataset
test_file = 'test_emoticon.csv'  # Adjust the file name/path as needed
test_data = pd.read_csv(test_file)

# Extract test features
X_test = test_data['input_emoticon']

# Extract features and labels
X_train = train_data['input_emoticon']
y_train = train_data['label']

# Define proportions of data to use
train_percentages = [0.4]
accuracies = []

# 1. Emoji Embedding Preparation
# Create a Tokenizer for emojis
tokenizer = Tokenizer(char_level=True, filters='')
tokenizer.fit_on_texts(X_train)
X_train_seq = tokenizer.texts_to_sequences(X_train)

# Preprocess test data (emoji embedding)
X_test_seq = tokenizer.texts_to_sequences(X_test)
X_test_pad = pad_sequences(X_test_seq, maxlen=max_seq_len, padding='post')

# TF-IDF transformation
X_test_tfidf = tfidf_vectorizer.transform(X_test).toarray()

# Pad sequences to ensure uniform input length
max_seq_len = max(len(seq) for seq in X_train_seq)
X_train_pad = pad_sequences(X_train_seq, maxlen=max_seq_len, padding='post')

# Define embedding size
embedding_dim = 16
vocab_size = len(tokenizer.word_index) + 1

# 2. TF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(1, 3))
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train).toarray()

# Loop over each training size percentage
for pct in train_percentages:
    # Calculate subset size
    subset_size = int(pct * len(X_train))

    # Create subset of training data
    X_train_subset_pad = X_train_pad[:subset_size]
    X_train_subset_tfidf = X_train_tfidf[:subset_size]
    y_train_subset = np.array(y_train)[:subset_size]

    # Define LSTM Model with Embedding and TF-IDF
    embedding_input = Input(shape=(max_seq_len,))
    tfidf_input = Input(shape=(X_train_tfidf.shape[1],))

    # Emoji embedding and LSTM layer
    embedded = Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_seq_len)(embedding_input)
    lstm_out = LSTM(32)(embedded)

    # Merge TF-IDF with LSTM output
    combined = concatenate([lstm_out, tfidf_input])
    combined = Dropout(0.5)(combined)
    combined = Dense(64, activation='relu')(combined)
    combined = Dense(32, activation='relu')(combined)
    output = Dense(1, activation='sigmoid')(combined)

    emoticon_model = Model(inputs=[embedding_input, tfidf_input], outputs=output)

    # Compile model
    emoticon_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Fit model with early stopping
    early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
    emoticon_model.fit([X_train_subset_pad, X_train_subset_tfidf], y_train_subset,
              epochs=20, batch_size=32, validation_split=0.2, callbacks=[early_stopping], verbose=1)

    # Make predictions on test data
    test_predictions = emoticon_model.predict([X_test_pad, X_test_tfidf])

    # Convert predictions to binary labels (0 or 1)
    test_pred_labels = (test_predictions > 0.5).astype(int).flatten()  # Flatten the array to a 1D array

    # Save the predictions to a .txt file
    np.savetxt('pred_emoticon.txt', test_pred_labels, fmt='%d')  # Save as integers (0 or 1)

"""Task 1.2"""

import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

import numpy as np

# Attempt to load the provided dataset files
try:
    train_data = np.load('train_feature.npz')
    val_data = np.load('valid_feature.npz')
    test_data = np.load('test_feature.npz')

    X_train = train_data['features']  # Shape: (num_samples, 13, 786)
    y_train = train_data['label']

    X_val = val_data['features']  # Shape: (num_samples, 13, 786)
    y_val = val_data['label']

    X_test = test_data['features']  # Shape: (num_samples, 13, 786)

    result = "Dataset loaded successfully."
except Exception as e:
    result = f"Error loading dataset: {str(e)}"

result

# Step 1: Feature Engineering - Concatenate the 13x786 matrix

def concatenate_features(X):
    # Flatten the 13x786 matrix into a single 1D vector (13 * 786 = 10218 features)
    return X.reshape(X.shape[0], -1)  # Shape will be (num_samples, 10218)

X_train_concat = concatenate_features(X_train)
X_val_concat = concatenate_features(X_val)
X_test_concat = concatenate_features(X_test)

# Step 2: Optional - Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_concat)
X_val_scaled = scaler.transform(X_val_concat)
X_test_scaled = scaler.transform(X_test_concat)

# Step 3: Optional - Apply PCA for dimensionality reduction
pca = PCA(n_components=300)  # Reduce to 300 components, you can adjust this number based on experiments
X_train_pca = pca.fit_transform(X_train_scaled)
X_val_pca = pca.transform(X_val_scaled)
X_test_pca = pca.transform(X_test_scaled)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Load the Deep Features dataset
train_data = np.load('train_feature.npz')
val_data = np.load('valid_feature.npz')
test_data = np.load('test_feature.npz')

X_train = train_data['features']  # Shape: (num_samples, 13, 786)
y_train = train_data['label']

X_val = val_data['features']  # Shape: (num_samples, 13, 786)
y_val = val_data['label']

X_test = test_data['features']

# Step 1: Feature Engineering - Concatenate the 13x786 matrix
def concatenate_features(X):
    # Flatten the 13x786 matrix into a single 1D vector (13 * 786 = 10218 features)
    return X.reshape(X.shape[0], -1)  # Shape will be (num_samples, 10218)

X_train_concat = concatenate_features(X_train)
X_val_concat = concatenate_features(X_val)
X_test_concat = concatenate_features(X_test)

# Step 2: Optional - Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_concat)
X_val_scaled = scaler.transform(X_val_concat)
X_test_scaled = scaler.transform(X_test_concat)

# Step 3: Optional - Apply PCA for dimensionality reduction
pca = PCA(n_components=300)  # Reduce to 300 components
X_train_pca = pca.fit_transform(X_train_scaled)
X_val_pca = pca.transform(X_val_scaled)
X_test_pca = pca.transform(X_test_scaled)

# Define the percentages of data to train on
percentages = [0.2, 0.4, 0.6, 0.8, 0.99]
accuracies = []

# Train and evaluate the model on different subsets of the data
for percentage in percentages:
    # Split the training data according to the percentage
    X_train_partial, _, y_train_partial, _ = train_test_split(
        X_train_pca, y_train, train_size=percentage, random_state=42
    )

    # Train the Logistic Regression model with PCA on the subset of data
    logistic_model_pca_partial = LogisticRegression(max_iter=1000)
    logistic_model_pca_partial.fit(X_train_partial, y_train_partial)

    # Predict on the validation set
    y_pred_logistic_pca_partial = logistic_model_pca_partial.predict(X_val_pca)

    # Calculate the accuracy and append to the list
    accuracy_partial = accuracy_score(y_val, y_pred_logistic_pca_partial)
    accuracies.append(accuracy_partial)

    # Print the accuracy, classification report, and confusion matrix
    print(f"Training on {int(percentage * 100)}% of the data")
    print(f"Accuracy: {accuracy_partial * 100:.2f}%")
    print(classification_report(y_val, y_pred_logistic_pca_partial))
    print(confusion_matrix(y_val, y_pred_logistic_pca_partial))
    print("\n")

# Plot the graph of accuracy vs percentage of training data
plt.figure(figsize=(8, 6))
plt.plot([int(p * 100) for p in percentages], [a * 100 for a in accuracies], marker='o')
plt.title('Accuracy vs Percentage of Training Data')
plt.xlabel('Percentage of Training Data (%)')
plt.ylabel('Accuracy (%)')
plt.grid(True)
plt.show()

# Logistic Regression with PCA
logistic_model_pca = LogisticRegression(max_iter=1000)
logistic_model_pca.fit(X_train_pca, y_train)
y_pred_logistic_pca = logistic_model_pca.predict(X_val_pca)

# Random Forest with PCA
rf_model_pca = RandomForestClassifier()
rf_model_pca.fit(X_train_pca, y_train)
y_pred_rf_pca = rf_model_pca.predict(X_val_pca)

# SVM with PCA
svm_model_pca = SVC()
svm_model_pca.fit(X_train_pca, y_train)
y_pred_svm_pca = svm_model_pca.predict(X_val_pca)

# LightGBM with PCA
params = {
    'objective': 'binary',
    'metric': 'binary_logloss',
    'boosting_type': 'gbdt',
    'num_leaves': 31,
    'learning_rate': 0.3,
    'feature_fraction': 0.3,
}
num_round = 105
lgb_train_pca = lgb.Dataset(X_train_pca, label=y_train)
lgb_model_pca = lgb.train(params, lgb_train_pca, num_round)
y_pred_lgb_pca = lgb_model_pca.predict(X_val_pca)
y_pred_lgb_pca = [1 if x >= 0.5 else 0 for x in y_pred_lgb_pca]

# Step 5: Evaluate Models

print("---- PCA Features ----")
models_pca = {
    "Logistic Regression (PCA)": y_pred_logistic_pca,
    "Random Forest (PCA)": y_pred_rf_pca,
    "SVM (PCA)": y_pred_svm_pca,
    "LightGBM (PCA)": y_pred_lgb_pca
}

for model_name, y_pred in models_pca.items():
    accuracy = accuracy_score(y_val, y_pred)
    print(f"{model_name} Accuracy (PCA): {accuracy * 100:.2f}%")
    print(classification_report(y_val, y_pred))
    print(confusion_matrix(y_val, y_pred))
    print("\n")

# make predications on test data
y_pred = svm_model_pca.predict(X_test_pca)

# Save the predictions to a .txt file
np.savetxt('pred_deepfeat.txt', y_pred, fmt='%d')  # Save as integers (0 or 1)

"""Task 1.3"""

pip uninstall scikit-learn -y

pip install scikit-learn

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# Load the datasets
train_data = pd.read_csv('train_text_seq.csv')
valid_data = pd.read_csv('valid_text_seq.csv')
test_data = pd.read_csv('test_text_seq.csv')

# Strip any potential whitespace from column names
train_data.columns = train_data.columns.str.strip()
valid_data.columns = valid_data.columns.str.strip()
test_data.columns = test_data.columns.str.strip()

# Preprocess the input_str sequences using CountVectorizer
vectorizer = CountVectorizer(analyzer='char', ngram_range=(1, 2))  # Using character-level bigrams
X_train_full = vectorizer.fit_transform(train_data['input_str'])
y_train_full = train_data['label']
X_valid = vectorizer.transform(valid_data['input_str'])
y_valid = valid_data['label']

# Define the percentages to train on and store accuracies
percentages = [0.2, 0.4, 0.6, 0.8, 1.0]
accuracies = []

for pct in percentages:
    # Select the fraction of the training data
    num_samples = int(pct * X_train_full.shape[0])
    X_train = X_train_full[:num_samples]
    y_train = y_train_full[:num_samples]

    # Train logistic regression model
    model = LogisticRegression(max_iter=1000, solver='liblinear')
    model.fit(X_train, y_train)

    # Evaluate the model on the validation set
    y_valid_pred = model.predict(X_valid)
    accuracy = accuracy_score(y_valid, y_valid_pred)
    accuracies.append(accuracy)

# Plot the accuracy as a function of training data percentage
plt.figure(figsize=(10, 6))
plt.plot([p * 100 for p in percentages], accuracies, marker='o', linestyle='-')
plt.title('Validation Accuracy vs. Training Data Percentage')
plt.xlabel('Percentage of Training Data Used')
plt.ylabel('Validation Accuracy')
plt.grid(True)
plt.show()

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from sklearn.preprocessing import LabelEncoder
from keras.callbacks import EarlyStopping
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# Encode labels to integers if they are not
encoder = LabelEncoder()
y_train_full_encoded = encoder.fit_transform(y_train_full)
y_valid_encoded = encoder.transform(y_valid)

# Define percentages to train on and store accuracies
accuracies_nn = []

for pct in percentages:
    num_samples = int(pct * X_train_full.shape[0])
    X_train = X_train_full[:num_samples].toarray()  # Convert sparse matrix to dense
    y_train = y_train_full_encoded[:num_samples]

    # Define the shallow neural network
    model_nn = Sequential()
    model_nn.add(Dense(64, input_dim=X_train.shape[1], activation='relu'))
    model_nn.add(Dense(1, activation='sigmoid'))

    # Compile the model
    model_nn.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])

    # Early stopping to avoid overfitting
    early_stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

    # Train the model
    model_nn.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_valid.toarray(), y_valid_encoded), callbacks=[early_stop], verbose=0)

    # Evaluate the model on the validation set
    valid_loss, valid_accuracy = model_nn.evaluate(X_valid.toarray(), y_valid_encoded, verbose=0)
    accuracies_nn.append(valid_accuracy)

# Plot the accuracy as a function of training data percentage
plt.figure(figsize=(10, 6))
plt.plot([p * 100 for p in percentages], accuracies_nn, marker='o', linestyle='-')
plt.title('Validation Accuracy vs. Training Data Percentage (Shallow NN)')
plt.xlabel('Percentage of Training Data Used')
plt.ylabel('Validation Accuracy')
plt.grid(True)
plt.show()

import xgboost as xgb
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# Preprocess the input_str sequences using CountVectorizer
vectorizer = CountVectorizer(analyzer='char', ngram_range=(1, 3))  # Using character-level bigrams
X_train_full = vectorizer.fit_transform(train_data['input_str'])
y_train_full = train_data['label']
X_valid = vectorizer.transform(valid_data['input_str'])
y_valid = valid_data['label']

# Convert the sparse matrix to dense format for XGBoost
X_train_full = X_train_full.toarray()
X_valid = X_valid.toarray()

# Define the percentages to train on and store accuracies
percentages = [0.2, 0.4, 0.6, 0.8, 1.0]
accuracies_xgb = []

for pct in percentages:
    # Select the fraction of the training data
    num_samples = int(pct * X_train_full.shape[0])
    X_train = X_train_full[:num_samples]
    y_train = y_train_full[:num_samples]

    # Define the XGBoost classifier
    model_xgb = xgb.XGBClassifier(
        objective='binary:logistic',  # Binary classification
        eval_metric='logloss',        # Evaluation metric
        use_label_encoder=False       # Disable label encoder
    )

    # Train the model
    model_xgb.fit(X_train, y_train, eval_set=[(X_valid, y_valid)], verbose=False)

    # Predict on the validation set
    y_valid_pred = model_xgb.predict(X_valid)
    accuracy = accuracy_score(y_valid, y_valid_pred)
    accuracies_xgb.append(accuracy)

# Plot the accuracy as a function of training data percentage
plt.figure(figsize=(10, 6))
plt.plot([p * 100 for p in percentages], accuracies_xgb, marker='o', linestyle='-')
plt.title('Validation Accuracy vs. Training Data Percentage (XGBoost)')
plt.xlabel('Percentage of Training Data Used')
plt.ylabel('Validation Accuracy')
plt.grid(True)
plt.show()

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
# from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dropout, Dense
import matplotlib.pyplot as plt

# Load dataset
df_train_textseq = pd.read_csv("train_text_seq.csv")
df_test_textseq = pd.read_csv("test_text_seq.csv")
df_val_textseq = pd.read_csv("valid_text_seq.csv")

# Tokenize
tokenizer = Tokenizer(char_level=True)  # Adjust to False if word-level tokenization is needed
tokenizer.fit_on_texts(df_train_textseq.input_str)

# Removing first three characters from input strings (if this is intentional)
df_train_textseq.input_str = [s[3:] for s in df_train_textseq.input_str]
df_val_textseq.input_str = [s[3:] for s in df_val_textseq.input_str]

# Convert text to sequences and pad them
X_train_seq = tokenizer.texts_to_sequences(df_train_textseq.input_str)
X_train_padded = pad_sequences(X_train_seq, maxlen=47, padding='post', truncating='post')

X_val_seq = tokenizer.texts_to_sequences(df_val_textseq.input_str)
X_val_padded = pad_sequences(X_val_seq, maxlen=47, padding='post', truncating='post')

X_test_seq = tokenizer.texts_to_sequences(df_test_textseq.input_str)
X_test_padded = pad_sequences(X_test_seq, maxlen=47, padding='post', truncating='post')

X_train_textseq = X_train_padded
X_val_textseq = X_val_padded
X_test_textseq = X_test_padded

# Labels
y_train_textseq = df_train_textseq.label
y_val_textseq = df_val_textseq.label

# Train-test split
X_new_train, X_new_val, y_new_train, y_new_val = train_test_split(
    X_train_textseq, y_train_textseq, test_size=0.2, random_state=42, stratify=y_train_textseq
)

# Define LSTM model
model_lstm = Sequential()
model_lstm.add(Embedding(input_dim=len(tokenizer.word_index)+1, output_dim=64))
model_lstm.add(LSTM(8))
model_lstm.add(Dropout(0.2))
model_lstm.add(Dense(1, activation='sigmoid'))

# Compile model
model_lstm.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
history = model_lstm.fit(X_new_train, y_new_train, epochs=100, batch_size=20, validation_data=(X_new_val, y_new_val))

# % of training data vs Validation set accuracy.
percentages = [0.2, 0.4, 0.6, 0.8, 1.0]
validation_accuracies = []

for pct in percentages:
    print(f"{pct*100}% of dataset using...")
    num_samples = int(pct * len(X_new_train))
    X_partial_train = X_new_train[:num_samples]
    y_partial_train = y_new_train[:num_samples]
    history = model_lstm.fit(
        X_partial_train, y_partial_train,
        epochs=100,
        batch_size=20,
        validation_data=(X_new_val, y_new_val),
        verbose=0
    )
    validation_accuracies.append(history.history['val_accuracy'][-1])
    print(f"Training with {int(pct * 100)}% of data: Validation Accuracy = {history.history['val_accuracy'][-1] * 100:.2f}%")
    print("\n")

print("\n")

# Plot the results
plt.figure(figsize=(8, 6))
plt.plot([int(pct * 100) for pct in percentages], validation_accuracies, marker='o')
plt.xlabel("Percentage of Training Data Used")
plt.ylabel("Validation Set Accuracy")
plt.title("Training Data Usage vs. Validation Accuracy")
plt.ylim(0.30, 0.80)
plt.yticks(np.arange(0.60, 0.95, 0.05))
plt.grid(True)
plt.show()

y_test_pred_final = model_lstm.predict(X_test_textseq)

# Save the predictions to a .txt file
np.savetxt('pred_textseq.txt', y_test_pred_final, fmt='%d')  # Save as integers (0 or 1)

"""Task 2"""

import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import matplotlib.pyplot as plt

# Load Data
df_train_npz = np.load('train_feature.npz')
df_test_npz = np.load('test_feature.npz')
df_val_npz = np.load('valid_feature.npz')
df_train_textseq = pd.read_csv("train_text_seq.csv")
df_test_textseq = pd.read_csv("test_text_seq.csv")
df_val_textseq = pd.read_csv("valid_text_seq.csv")

# PCA for dimensionality reduction
pca = PCA(n_components=250)  # Changed number of components to 250

# Feature extraction and concatenation
def concatenate_features(X):
    return X.reshape(X.shape[0], -1)

# Preparing train, val, test sets
X_train = concatenate_features(df_train_npz['features'])
X_val = concatenate_features(df_val_npz['features'])
X_test = concatenate_features(df_test_npz['features'])

y_train = df_train_npz['label']
y_val = df_val_npz['label']

# Standard scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

# PCA transformation
X_train_pca = pca.fit_transform(X_train_scaled)
X_val_pca = pca.transform(X_val_scaled)
X_test_pca = pca.transform(X_test_scaled)

# Tokenizer for text sequences
tokenizer = Tokenizer(char_level=True)
tokenizer.fit_on_texts(df_train_textseq.input_str)

X_train_seq = tokenizer.texts_to_sequences(df_train_textseq.input_str)
X_train_padded = pad_sequences(X_train_seq, maxlen=50, padding='post', truncating='post')

X_val_seq = tokenizer.texts_to_sequences(df_val_textseq.input_str)
X_val_padded = pad_sequences(X_val_seq, maxlen=50, padding='post', truncating='post')

X_test_seq = tokenizer.texts_to_sequences(df_test_textseq.input_str)
X_test_padded = pad_sequences(X_test_seq, maxlen=50, padding='post', truncating='post')

# Combining PCA features and padded sequences
X_train_final = np.concatenate([X_train_pca, X_train_padded], axis=1)
X_val_final = np.concatenate([X_val_pca, X_val_padded], axis=1)
X_test_final = np.concatenate([X_test_pca, X_test_padded], axis=1)

# XGBoost Model Parameters
params_xgb = {
    'n_estimators': 150,
    'learning_rate': 0.05,
    'max_depth': 8,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'random_state': 42
}

# Training with different percentages of data
percentages = [0.2, 0.4, 0.6, 0.8, 1.0]
validation_accuracies = []

for pct in percentages:
    if pct < 1.0:
        # Split the data if pct is less than 100%
        X_train_subset, _, y_train_subset, _ = train_test_split(X_train_final, y_train, train_size=pct, random_state=42)
    else:
        # Use the entire dataset for 100% case
        X_train_subset = X_train_final
        y_train_subset = y_train

    # Train the model with subset of the data
    model = xgb.XGBClassifier(**params_xgb)
    model.fit(X_train_subset, y_train_subset)

    # Predict on validation set
    y_val_pred = model.predict(X_val_final)

    # Calculate accuracy
    acc = accuracy_score(y_val, y_val_pred)
    validation_accuracies.append(acc)

    # Print the accuracy for this percentage of data
    print(f"Training with {int(pct * 100)}% of data: Validation Accuracy = {acc * 100:.2f}%")

# Plot the results
plt.figure(figsize=(8, 6))
plt.plot([int(pct * 100) for pct in percentages], validation_accuracies, marker='o')
plt.xlabel("Percentage of Training Data Used")
plt.ylabel("Validation Set Accuracy")
plt.title("Training Data Usage vs. Validation Accuracy (XGBoost)")
plt.ylim(0.70, 1.0)
plt.yticks(np.arange(0.70,  1.05, 0.05))
plt.grid(True)
plt.show()

# Final Model Evaluation on Full Data
final_model = xgb.XGBClassifier(**params_xgb)
final_model.fit(X_train_final, y_train)

# Predict on the full validation set
y_val_pred_final = final_model.predict(X_val_final)

# Calculate final accuracy and display metrics
final_accuracy = accuracy_score(y_val, y_val_pred_final)
print(f"XGBoost Model Accuracy: {final_accuracy * 100:.2f}%")

# Print Classification Report and Confusion Matrix
print(classification_report(y_val, y_val_pred_final))
print(confusion_matrix(y_val, y_val_pred_final))

# Train the model
model = xgb.XGBClassifier(**params_xgb)
model.fit(X_train_final, y_train)

# Predict on test set
y_test_pred_final = model.predict(X_test_final)
# y_test_pred_final = [1 if x >= 0.5 else 0 for x in y_test_pred_final]

# Save the predictions to a .txt file
np.savetxt('pred_combined.txt', y_test_pred_final, fmt='%d')  # Save as integers (0 or 1)
