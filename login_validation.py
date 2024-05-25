from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time


# Data to test against:
emails = [
    'john.doe@example.com',
    'user@sub-domain.example.com',
    'user@domain.co.uk',
    'contact@website.org'
]

passwords = [
    'password1',
    'Password',
    'PASSWORDa',
    'Password1',
    'Password1!'
]
# Initialize the Webdriver
driver = webdriver.Chrome()
# URL of the login page
login_url = 'file:///C:/Users/A%20and%20L/Downloads/QA_Task.html'



# Perform main page login


driver.get(login_url)
candidateNameField = driver.find_element(By.ID, "candidateName")
candidateEmailField = driver.find_element(By.ID, "candidateMail")
startLoginBtn = driver.find_element(By.ID, "startButton")
candidateNameField.clear()
candidateNameField.send_keys("Andrei Bucur")
candidateEmailField.clear()
candidateEmailField.send_keys("bucur21andrei@gmail.com")
startLoginBtn.click()

# Function to test the login functionality
def perform_login(email, password):

    # Locate the email and password fields
    email_field = driver.find_element(By.ID, "email")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.XPATH, '//input[@type="button" and @value="Login" and @onclick="validateLogin()"]')

    
    # Enter email and password
    email_field.clear()
    email_field.send_keys(email)
    password_field.clear()
    password_field.send_keys(password)
    
    # Click login button
    login_button.click()

    # Wait for a while to let the login process complete
    time.sleep(2)
    
    # Conditions to test against
    check_invalid_email = "Invalid email"
    check_valid_email = "Valid Email"
    check_valid_password = "Valid Password"
    check_invalid_password = "Invalid Password"
    valid_color = "rgba(0, 128, 0, 1)"
    invalid_color = "rgba(255, 0, 0, 1)"


    try:
        # Attempt to find an element that confirms successful login
        success_message = driver.find_element(By.ID, "succesMsg")
        color = success_message.value_of_css_property('color')
        # Expected color for green is 'rgba(0, 128, 0, 1)'
        if color == 'rgba(0, 128, 0, 1)':
            return "Success and green"
        else:
            return "Success but not green"
    except NoSuchElementException:

        # Find email error message element
        try:
            email_error_message = driver.find_element(By.ID, "errorMsgMail")
            email_color = email_error_message.value_of_css_property('color')
            email_message = email_error_message.text 
        except NoSuchElementException:
            email_color = None
        
        # Find password error message element
        try:
            password_error_message = driver.find_element(By.ID, "errorMsgPwd")
            password_color = password_error_message.value_of_css_property('color')
            password_message = password_error_message.text
        except NoSuchElementException:
            password_color = None

        # Check both email and password error messages
        if email_color == valid_color and check_valid_email in email_message and password_color == valid_color and check_valid_password in password_message:
            return "Email and Password are valid!"
        elif email_color == valid_color and password_color == invalid_color:
            return "Valid Email and Invalid Password" 
        elif email_color == invalid_color and check_valid_email in email_message and password_color == invalid_color:
            return "Valid email with wrong CSS property, and invalid password"
        elif email_color == valid_color and check_invalid_email in email_message and password_color == invalid_color and check_invalid_password in password_message:
            return "Invalid Email with Green CSS property and invalid password"  
        elif email_color == invalid_color and check_invalid_password in email_message and password_color == invalid_color and check_valid_password in password_message:
            return "Invalid check!: Password message found inside the email validation field!"
        elif email_color == valid_color and check_invalid_password in email_message and password_color == invalid_color and check_valid_password in password_message:
            return "Invalid check!: Password message found inside the email validation field!"
        elif email_color == valid_color and check_valid_password in email_message and password_color == valid_color:
            return "Invalid check!: Password message found inside the email validation field!"
        elif email_color == invalid_color and check_valid_password in email_message and password_color == valid_color:
            return "Invalid check!: Password message found inside the email validation field!"   
        elif password_color == valid_color and check_valid_password in password_message and email_color == invalid_color and "Invalid Email" in email_message:
            return "Valid Password & Invalid Email!"
        elif password_color == valid_color and check_invalid_password in password_message and email_color == invalid_color:
            return "Invalid Password but with Green CSS property!"
        elif email_color == invalid_color and check_invalid_email in email_message and password_color == invalid_color and check_invalid_password in password_message:
            return "Both email and password are invalid!"
        else:
            return "Failure, no message found!"

# Function to run tests
def run_tests():
    for email in emails:
        for password in passwords:
            result = perform_login(email, password)
            print(f"Test with email: {email} and password: {password} - Result: {result}")

try:
    # Run the tests
    run_tests()
finally:
    # Close the browser
    driver.quit()