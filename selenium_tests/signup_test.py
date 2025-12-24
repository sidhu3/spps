from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("http://127.0.0.1:5000/signup")

# Note: Email ID must be uniqe each time we perform test, it's constraint is unique in table.
try:
    driver.find_element(By.ID, "uname").send_keys("test_user5")
    driver.find_element(By.ID, "email").send_keys("test12345@example.com")
    driver.find_element(By.ID, "fname").send_keys("First")
    driver.find_element(By.ID, "lname").send_keys("Last")
    driver.find_element(By.ID, "upassword").send_keys("password12345")

    signup_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#signup-form button[type='submit']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", signup_button)
    signup_button.click()

    WebDriverWait(driver, 10).until(
        EC.url_contains("/login")
    )
    print("Signup test passed!")

except Exception as e:
    print(f"Signup test failed: {e}")

finally:
    driver.quit()
