# Student Performance Prediction System

A Flask-based Machine Learning project that predicts student performance scores, grades, and pass/fail status using various academic features. The system includes authentication, CRUD operations, dashboards with filtering, data visualizations, and ML-powered analytics.

---

## 🚀 Features

### 🔐 Authentication

* User Signup
* Login
* Logout
* Password Reset (secure hashing)

### 📊 ML-Based Predictions

* Performance Score Prediction
* Grade Prediction
* Pass/Fail Prediction

### 🧮 Data Inputs

* Hours Studied
* Attendance Percentage
* Assignments Submitted
* Previous Grades

### 📋 Application Modules

* Add, update, view, and delete student records
* Dashboard with filters/search
* Pagination
* Student-wise detail view

### 📈 Visualizations

* Line Chart
* Bar Chart
* Doughnt Chart
* Radar Chart

### 🔧 Tech Stack

* Python
* Flask
* Pandas
* Scikit-learn
* Bootstrap

---

## 📂 Project Structure

```
student-performance/
│── app.py
│── model.pkl
│── requirements.txt
│── static/
│── templates/
│── instance/           # (ignored in git)
│── selenium_tests/     # (ignored in git)
│── data.csv            # (ignored in git)
│── venv/               # (ignored in git)
│── README.md
│── .gitignore
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```
git clone https://github.com/your-username/spps.git
cd spps
```

### 2️⃣ Create and Activate Virtual Environment

```
python -m venv venv
```

**Windows:**

```
venv\Scripts\activate
```

**Linux/Mac:**

```
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

### 4️⃣ Run the Application

```
python app.py
```

### 5️⃣ Open Browser

```
http://127.0.0.1:5000/
```

---

## 🧠 Machine Learning Model

The model is trained on data of 100 students using features:

* Hours Studied
* Attendance Percentage
* Assignments Submitted
* Previous Grades

Target:

* Performance Score

Additional outputs:

* Grade Prediction
* Pass/Fail Prediction

---

## 📜 .gitignore Summary

* venv/
* instance/
* selenium_tests/
* data.csv
* **pycache**/

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first to discuss the proposed change.

---

## ⭐ Support

If you find this project useful, consider giving it a **star** on GitHub!
