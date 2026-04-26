from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # Automatically installs ChromeDriver

# Chrome options for headless CI/CD
options = Options()
options.add_argument("--headless=new")   # Use new headless mode
options.add_argument("--no-sandbox")     # Required for CI
options.add_argument("--disable-dev-shm-usage")  # Fix limited /dev/shm
options.add_argument("--disable-gpu")
options.add_argument("--disable-software-rasterizer")

# Use webdriver-manager to install the compatible ChromeDriver automatically
service = Service(ChromeDriverManager().install())

# Create WebDriver
driver = webdriver.Chrome(service=service, options=options)

try:
    # Open local file (if using /var/www/html/index.html)
    driver.get("file:///var/www/html/index.html")

    # Wait for element with ID 'title'
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "title"))
    )

    title = driver.find_element(By.ID, "title").text

    # Assert the title
    assert title == "Hello CI/CD", f"Expected 'Hello CI/CD' but got '{title}'"
    print(f"TEST PASSED: Title is '{title}'")

except Exception as e:
    print(f"TEST FAILED: {e}")

finally:
    driver.quit()
