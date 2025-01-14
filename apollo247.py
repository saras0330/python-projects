import json
import unicodedata
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configure Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--start-maximized')
options.add_argument('--disable-notifications')

# Initialize the WebDriver
driver = webdriver.Chrome(options=options)

def decode_unicode_using_unicodedata(text):
    """
    Decodes any Unicode escape sequences into their actual characters using unicodedata.

    Args:
        text (str): The string containing Unicode escape sequences.

    Returns:
        str: The string with Unicode escape sequences decoded into actual symbols.
    """
    # Normalize the string to decompose combined characters (e.g., decomposing accented characters)
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')

def extract_doctor_details(doctor_url):
    """
    Extracts detailed information from a doctor's profile page.

    Args:
        doctor_url (str): The URL of the doctor's profile page.

    Returns:
        dict: A dictionary containing the doctor's details.
    """
    doctor_info = {}
    try:
        driver.get(doctor_url)
        wait = WebDriverWait(driver, 20)

        # Extract Name
        try:
            name_element = wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='mainContainerCT']/div[2]/div[1]/div[2]/div[1]/h1"))
            )                                            
            doctor_info['name'] = name_element.text.strip()
        except Exception as e:
            print(f"Failed to extract doctor's name: {e}")
            doctor_info['name'] = "Not available"

        # Extract Specialization
        try:
            specialties_elements = driver.find_elements(By.XPATH, "//*[@id='mainContainerCT']/div[2]/div[1]/div[2]/div[2]/h2")
            doctor_info['specialization'] = [specialty.text.strip() for specialty in specialties_elements if specialty.text.strip()]
        except Exception as e:
            print(f"Failed to extract specialization: {e}")
            doctor_info['specialization'] = []

        # Extract Experience
        try:
            experience_element = wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='mainContainerCT']/div[2]/div[1]/div[2]/div[2]/div/h3"))
            )
            doctor_info['experience'] = experience_element.text.strip()
        except Exception as e:
            print(f"Failed to extract experience: {e}")
            doctor_info['experience'] = "Not available"

        # Extract Languages Spoken
        try:
            languages_elements = driver.find_elements(By.XPATH, "//*[@id='mainContainerCT']/div[2]/div[1]/div[2]/div[4]/h3")
            doctor_info['languages_spoken'] = [language.text.strip() for language in languages_elements if language.text.strip()]
        except Exception as e:
            print(f"Failed to extract languages spoken: {e}")
            doctor_info['languages_spoken'] = []

        # Extract Services - Debugging this part
        try:
            # Wait for the element containing services
            services_elements = wait.until(
                EC.presence_of_all_elements_located((By.XPATH, "//*[@id='mainContainerCT']/div[2]/div[5]/div[2]/div[5]/ul/li"))
            )
            
            # Print to check if we are extracting the correct elements
            print(f"Found {len(services_elements)} service items.")

           
            doctor_info['services'] = [
                service.text.strip().replace("\u2022", "-").replace("\n", "")
                for service in services_elements if service.text.strip()
            ]
            
            if not doctor_info['services']:
                print("No services found in the list.")
        except Exception as e:
            print(f"Failed to extract services: {e}")
            doctor_info['services'] = [] 

        # Extract Qualifacation
        try:
            services_elements = driver.find_elements(By.XPATH, "//*[@id='mainContainerCT']/div[2]/div[1]/div[2]/div[3]/h3")
            doctor_info['Qualifications'] = [service.text.strip() for service in services_elements if service.text.strip()]
        except Exception as e:
            print(f"Failed to extract Qualifications: {e}")
            doctor_info['Qualifications'] = []

        # Extract Clinic Fees (if available)
        try:
            # Wait for the clinic fees element to be available
            fees_element = wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='headlessui-tabs-panel-4']/div/div[1]/p"))
            )
            # Extract the fee text
            fee_text = fees_element.text.strip()

           
            doctor_info['clinic_fees'] = decode_unicode_using_unicodedata(fee_text)
            
            print(f"Clinic Fees: {doctor_info['clinic_fees']}")  

        except Exception as e:
            print(f"Failed to extract clinic fees: {e}")
            doctor_info['clinic_fees'] = "Not available"

        print(f"Successfully extracted data for {doctor_info['name']}.")

    except Exception as e:
        print(f"Error extracting details from {doctor_url}: {e}")

    return doctor_info

def main():
    doctor_url = "https://www.apollo247.com/doctors/dr-neeraj-verma-05fef13f-cba1-4e75-b083-9fa7df9a62ef?source=Listing_Page"
    doctor_data = extract_doctor_details(doctor_url)

    # Log extracted data
    print("Extracted Data:")
    print(json.dumps(doctor_data, indent=4))

    # Save to JSON
    with open('apollo_doctor_details.json', 'w', encoding='utf-8') as f:
        json.dump(doctor_data, f, indent=4, ensure_ascii=False)
    print(f"Doctor details saved to apollo_doctor_details.json.")

    driver.quit()

if __name__ == "__main__":
    main()
