import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from dotenv import load_dotenv
import os

load_dotenv()

# Configuration       
cloudinary.config( 
    cloud_name = "dd9cg7ktp", 
    api_key = "491653465686427", 
    api_secret = os.getenv("API_SECRET"), # Click 'View API Keys' above to copy your API secret
    secure=True
)


def uploadPDF(file_path : str):
    try:
        response = cloudinary.uploader.upload(file_path, resource_type="raw",use_filename=True, folder="pdfs", public_id=file_path.split("/")[-1].split(".")[0])
        print("Upload completed successfully.")
        return response['secure_url']
    except Exception as e:
        print(f"Upload failed: {str(e)}")
        return None




