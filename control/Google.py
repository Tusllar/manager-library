from google.oauth2 import service_account # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.http import MediaIoBaseDownload
import os
import win32com.client
from googleapiclient.http import MediaFileUpload,MediaIoBaseUpload
import pythoncom
PARENT_FOLDER_ID = "161T4j3VgAVtD0uWEGRbnYqkavyyYmqh_" 
# # Hàm xác thực với Google Drive
def authenticate():
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = 'pbl3.json'
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
     # call Drive API client
    service = build('drive', 'v3', credentials=creds)
    return service
def word_to_pdf(input_file,output_file):
    pythoncom.CoInitialize()
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    word.DisplayAlerts = False
    try:
        doc = word.Documents.Open(input_file)
        doc.SaveAs(output_file, FileFormat=17)
        print("success pdf")
    except Exception as e:
        print("Error: ", e)
    finally:
        doc.Close()
        word.Quit()
        pythoncom.CoUninitialize()
    return output_file
