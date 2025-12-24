from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

try:
    # Step 1: Login
    driver.get("http://127.0.0.1:5000/login")
    driver.find_element(By.ID, "uname").send_keys("test_user")
    driver.find_element(By.ID, "upassword").send_keys("password123")
    driver.find_element(By.CSS_SELECTOR, "#login-form button[type='submit']").click()

    # Wait for login redirect
    WebDriverWait(driver, 10).until(EC.url_changes("http://127.0.0.1:5000/login"))
    print("Logged in successfully.")

    # Step 2: Directly go to logout URL (simulate logout)
    driver.get("http://127.0.0.1:5000/logout")
    print("Visited logout URL.")

    # Step 3: Wait for redirect after logout (usually login page or home page)
    WebDriverWait(driver, 10).until(EC.url_contains("/"))
    print("Logout successful, redirected to Home page.")

except Exception as e:
    print(f"Logout test failed: {e}")

finally:
    driver.quit()
