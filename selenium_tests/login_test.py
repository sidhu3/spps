from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Chrome options (run headless if you don't want the UI)
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Comment this out if you want to see the browser UI

# Set up ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open the Flask app (assuming it's running locally on port 5000)
driver.get("http://127.0.0.1:5000/login")
print("Page loaded")

# Wait for the login page elements (username, password fields)
try:
    # Wait for the username field to be visible
    username_field = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.NAME, "uname"))
    )
    password_field = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.NAME, "upassword"))
    )
    submit_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )

    # Enter dummy credentials and submit the form
    username_field.send_keys("testuser")  # Replace 'testuser' with your dummy username
    password_field.send_keys("password123")  # Replace 'password123' with your dummy password
    submit_button.click()

    # Wait for the post-login page (check for the redirected page or any element indicating success)
    WebDriverWait(driver, 15).until(
        EC.url_contains("/")  # Adjust URL path according to your post-login page
    )

    print("Login test passed! Redirected successfully.")

except Exception as e:
    print(f"Test failed: {e}")

# Close the browser
driver.quit()
