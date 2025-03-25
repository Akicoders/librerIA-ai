import pdfplumber as pp
import pikepdf
import requests
import os
from urllib.parse import urlparse
from upload_cloudinary import uploadPDF



class PDFProcessor:
    def __init__(self, path: str):
        self.path = path
        self.text = ""

    def extract_text(self):
        with pp.open(self.path) as pdf:
            for page in pdf.pages:
                self.text += page.extract_text()
                return self.text

    @staticmethod
    def download_from_url(url: str, name: str) -> str:
        """Download a PDF from a URL and save it to the specified path"""
        try:
            save_path = f"c:/Users/Santiago/Desktop/librerIA-ai/app/pdf/{name}.pdf"
            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status()
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"PDF downloaded successfully to {save_path}")
            print("Uploading to Cloudinary...")
            uploaded_url =  uploadPDF(save_path)
            if uploaded_url:
                print(f"PDF uploaded successfully. URL: {uploaded_url}")
            else:
                print("Failed to upload PDF")
            return save_path
        except Exception as e:
            raise Exception(f"Failed to download PDF: {str(e)}")

    def optimize_pdf(input_path, output_path):
        with pikepdf.open(input_path) as pdf:
            pdf.save(output_path, optimize_images=True,optimize_memory=True)

    def get_text(self):
        return self.text

    