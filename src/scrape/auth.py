from selenium import webdriver
from selenium.webdriver.common.by import By
import os 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_popup_window(driver: webdriver.Chrome, main_window_handle: str):
    for handle in driver.window_handles:
        if handle != main_window_handle:
            return handle
    raise Exception("No popup window found")

def wait_loader(driver: webdriver.Chrome, by: str, value: str):
    try:
        _ = WebDriverWait(driver, 2).until(EC.presence_of_element_located((by, value)))
    except:
        return
    loader = driver.find_element(by, value)
    _ = WebDriverWait(driver, 10).until(EC.staleness_of(loader))


def handle_login(driver: webdriver.Chrome):
    main_window = driver.current_window_handle
    
    wait_loader(driver, By.ID, "loaderHolder")
    if driver.current_url.startswith("https://nofesh.prat.idf.il"):
        print("Finished early") # Test if it works
        return # finished early
    
    print("Authentication- Started", "You will receive MS Authenticator key soon.")
    user_id = os.getenv("ID")
    if not user_id:
        raise ValueError("ID environment variable not set")
    user_password = os.getenv("MS_PASSWORD")
    if not user_password:
        raise ValueError("MS_PASSWORD environment variable not set")

    id_element = driver.find_element(By.ID, "IdNumber")
    submit_button = driver.find_element(By.ID, "submitLogin")
    id_element.send_keys(user_id)
    submit_button.click()
    
    popup = get_popup_window(driver, main_window)
    driver.switch_to.window(popup)
    
    # Wait for password textbox to be loaded
    _ = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "i0118")))
    
    password_MS_element = driver.find_element(By.ID, "i0118")
    submit_MS_button  = driver.find_element(By.ID, "idSIButton9")
    password_MS_element.send_keys(user_password)
    
    _ = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(submit_MS_button))
    submit_MS_button.click()
    
    # Wait until authenticator code is shown
    _ = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "idRichContext_DisplaySign")))
    authenticator_code = driver.find_element(By.ID, "idRichContext_DisplaySign").text
    
    print("Authentication- MS Authenticator Code", authenticator_code)
    
    # Authenticate with Authenticator
    _ = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.ID, "KmsiCheckboxField")))
    
    dont_ask_again_checkbox = driver.find_element(By.ID, "KmsiCheckboxField")
    submit_MS_button  = driver.find_element(By.ID, "idSIButton9")
    dont_ask_again_checkbox.click()
    submit_MS_button.click()
    
    print("Authentication- Finished successfuly", "Finished authentication")
    
    driver.switch_to.window(main_window)
