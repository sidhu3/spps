from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import pickle
import pandas as pd
import math 

# Load the dataset
df = pd.read_csv('student_performance_data.csv')

# Features (X) and Target (y)
X = df[['hours_studied', 'attendance_percentage', 'assignments_submitted', 'previous_grades']]
y = df['performance_score']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train) 

# Evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
rmse = math.sqrt(mse)
# Print evaluation results
print(f"Model Evaluation Results:")
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"- Interpretation: The average squared difference between actual and predicted values is {mse:.2f}.")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"- Interpretation: The model's predictions are off by approximately {rmse:.2f} units on average.")
print(f"R² Score: {r2:.2f}")
if r2 >= 0.7:
    print(f"- Interpretation: The model explains {r2 * 100:.2f}% of the variance in the target variable, which is a good fit.")
else:
    print(f"- Interpretation: The model explains {r2 * 100:.2f}% of the variance in the target variable. Consider improving the model.")


# Save the trained model
with open('model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("Model training complete and saved to model.pkl.")