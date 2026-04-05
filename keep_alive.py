from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def wake_streamlit():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Runs without a GUI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print("Visiting the app...")
        driver.get("https://your-app-url.streamlit.app")
        
        # Wait for the page to load
        time.sleep(10) 
        
        # Streamlit's "Wake up" button usually contains specific text or classes
        # This looks for any button that might say "Wake up"
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for button in buttons:
            if "Wake up" in button.text:
                button.click()
                print("Clicked 'Wake up' button.")
                time.sleep(5)
                break
        
        print("Keep-alive visit successful.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    wake_streamlit()
