import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent


# Setup Chrome WebDriver
def setup_driver():
    ua = UserAgent()
    options = webdriver.ChromeOptions()
    user_agent = ua.random
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--start-maximized")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


# Log in to Amazon
def login_to_amazon(driver, email, password):
    driver.get("https://www.amazon.in/ap/signin")
    try:
        # Enter Email
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ap_email"))
        ).send_keys(email)
        driver.find_element(By.ID, "continue").click()

        # Enter Password
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ap_password"))
        ).send_keys(password)
        driver.find_element(By.ID, "signInSubmit").click()

        # Handle Two-Factor Authentication if enabled (optional step)
        try:
            otp_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "auth-mfa-otpcode"))
            )
            otp = input("Enter the OTP sent to your registered mobile/email: ")
            otp_field.send_keys(otp)
            driver.find_element(By.ID, "auth-signin-button").click()
        except TimeoutException:
            print("No OTP step detected, proceeding...")

        # Verify login success
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "nav-link-accountList"))
        )
        print("Login successful!")

    except TimeoutException:
        print("Login failed. Check credentials or website layout.")
        driver.quit()


# Scrape Product Details
def scrape_product_details(driver, product_url):
    # Same logic as in the previous code for extracting product details
    pass


# Scrape Category
def scrape_category(driver, category_url, category_name, max_products=10):
    # Same logic as in the previous code for extracting categories
    pass


# Save to CSV
def save_to_csv(data, filename):
    if not data:
        print("No data to save.")
        return

    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"Data saved to {filename}")


# Main Function
def main():
    # Update with your Amazon credentials
    amazon_email = "your@gmail.com"
    amazon_password = "your password"

    # Category URLs
    categories = {
        "Kitchen": "https://www.amazon.in/gp/bestsellers/kitchen/ref=zg_bs_nav_kitchen_0",
        "Shoes": "https://www.amazon.in/gp/bestsellers/shoes/ref=zg_bs_nav_shoes_0",
        "Computers": "https://www.amazon.in/gp/bestsellers/computers/ref=zg_bs_nav_computers_0",
        "Electronics": "https://www.amazon.in/gp/bestsellers/electronics/ref=zg_bs_nav_electronics_0"
    }

    max_products_per_category = 10
    driver = setup_driver()
    all_products = []

    try:
        # Login to Amazon
        login_to_amazon(driver, amazon_email, amazon_password)

        # Scrape each category
        for category_name, category_url in categories.items():
            print(f"Scraping Category: {category_name}")
            category_products = scrape_category(driver, category_url, category_name, max_products=max_products_per_category)
            all_products.extend(category_products)

        # Save to CSV
        save_to_csv(all_products, "amazon_products.csv")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
