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


def uploadPDF(file_path):
    cloudinary.uploader.upload("library/"+file_path)




