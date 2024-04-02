import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data with the correct delimiter
df = pd.read_csv('C:/Users/tyron/Heart Care Assignment/heart.csv', sep=';') 

# Print the DataFrame columns to verify
print(df.columns)

# Check for missing values
missing_values = df.isnull().sum()
print("Missing values in each column:\n", missing_values)

# Impute missing values
df['ca'].fillna(df['ca'].median(), inplace=True)
df['thal'].fillna(df['thal'].mode()[0], inplace=True)

# Check for duplicates
duplicates = df.duplicated().sum()
print("Number of duplicate rows:", duplicates)

# Remove duplicates if any
df.drop_duplicates(inplace=True)

# Define the categorical variables
categorical_vars = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal']

# Plot the distribution of classes for each categorical variable
for var in categorical_vars:
    plt.figure(figsize=(8, 4))
    sns.countplot(x=var, hue='target', data=df)
    plt.title(f'Distribution of {var} by Target')
    plt.show()

# Define the numeric variables
numeric_vars = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']

# Plot the distribution of classes for each numeric variable
for var in numeric_vars:
    plt.figure(figsize=(8, 4))
    sns.histplot(df, x=var, hue='target', kde=True)
    plt.title(f'Distribution of {var} by Target')
    plt.show()
