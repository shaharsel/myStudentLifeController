from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
password_file = open(r"C:\Users\shaha\PycharmProjects\myStudentLifeController\Resources\GmailPassword", "r")
gmail_password = password_file.read()
password_file.close()


def get_service():
    SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                r'C:\Users\shaha\PycharmProjects\myStudentLifeController\Resources\credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('classroom', 'v1', credentials=creds)
    return service


def open_MyStudyLife():
    global gmail_password
    driver = webdriver.Chrome(r'C:\Users\shaha\bin\chromedriver.exe')
    driver.get("https://app.mystudylife.com/dashboard")
    # Open My Study Life
    continue_with_google = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Continue with Google"))
    )
    continue_with_google.click()
    # Click on sign in with google
    insert_email = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "identifier"))
    )
    insert_email.send_keys("shaharsel@gmail.com")
    insert_email.send_keys(Keys.RETURN)
    # Enter my email
    insert_password = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    time.sleep(1)
    insert_password.send_keys(gmail_password)
    insert_password.send_keys(Keys.RETURN)
    # Enter my password
    time.sleep(5)
    driver.quit()
    return driver


service = get_service()
results = service.courses().list(pageSize=10).execute()
courses = results.get('courses', [])

if not courses:
    print('No courses found.')
else:
    print('Courses:')
    for course in courses:
        print(course['name'])
