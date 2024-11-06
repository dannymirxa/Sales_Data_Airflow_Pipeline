from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/drive']
# SERVICE_ACCOUNT_FILE = 'diy-assessment-6bd74330e042.json'
SERVICE_ACCOUNT_FILE = '/opt/airflow/credentials/diy-assessment-6bd74330e042.json'
PARENT_FOLDER_ID = "1agNDkq3L8f2-Qzs9m5-NC1AN1A1-PJbB"

def authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def upload_excel(file_path):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name' : "Product Category Data DIY",
        'parents' : [PARENT_FOLDER_ID]
    }

    file = service.files().create(
        body=file_metadata,
        media_body=file_path
    ).execute()

# upload_excel("/opt/airflow/file_output/product_category.xlsx")