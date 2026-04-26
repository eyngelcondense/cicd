from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # Automatically installs ChromeDriver

# -------------------------------
# Chrome options for headless CI/CD
# -------------------------------
options = Options()
options.add_argument("--headless=new")          # New headless mode
options.add_argument("--no-sandbox")            # Required in CI
options.add_argument("--disable-dev-shm-usage") # Avoid /dev/shm issues
options.add_argument("--disable-gpu")           # Optional
options.add_argument("--disable-software-rasterizer")
options.add_argument("--remote-debugging-port=9222")

# -------------------------------
# Setup ChromeDriver service
# -------------------------------
service = Service(ChromeDriverManager().install())

# -------------------------------
# Create WebDriver instance
# -------------------------------
driver = webdriver.Chrome(service=service, options=options)

try:
    # Open the local HTML file or localhost URL
    driver.get("file:///var/www/html/index.html")  # Use "http://localhost" if served via HTTP

    # Wait for element with ID 'title'
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "title"))
    )

    # Check the title
    title = driver.find_element(By.ID, "title").text
    assert title == "Hello CI/CD", f"Expected 'Hello CI/CD' but got '{title}'"

    print(f"TEST PASSED: Title is '{title}'")

except Exception as e:
    print(f"TEST FAILED: {e}")

finally:
    driver.quit()
