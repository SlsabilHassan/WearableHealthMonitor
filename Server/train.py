# Import necessary libraries
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

def main():
    # Load the dataset
    file_path = 'qt_dataset.csv'  # Update with your dataset path
    data = pd.read_csv(file_path)

    # Encoding the 'Result' column
    label_encoder = LabelEncoder()
    data['Result'] = label_encoder.fit_transform(data['Result'])

    # Splitting the dataset into features and target
    X = data[['SPo2', 'Heart Rate']]
    y = data['Result']

    # Splitting the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Training a logistic regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Predicting and evaluating the model
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)

    # Output the results
    print("Classification Report:\n", report)
    print("Confusion Matrix:\n", conf_matrix)

    # Saving the model to a .pkl file
    with open('tiredness_model.pkl', 'wb') as file:
        pickle.dump(model, file)

    print("Model saved as pkl file'")

if __name__ == "__main__":
    main()
