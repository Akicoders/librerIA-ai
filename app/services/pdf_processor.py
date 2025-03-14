import pdfplumber as pp
import pikepdf

class PDFProcessor:
    def __init__(self, path: str):
        self.path = path
        self.text = ""
        self.process()

    def extract_text(self):
        with pp.open(self.path) as pdf:
            for page in pdf.pages:
                self.text += page.extract_text()
                return self.text

    def download(self):
        return self.path

    def optimize_pdf(input_path, output_path):
        with pikepdf.open(input_path) as pdf:
            pdf.save(output_path, optimize_images=True,optimize_memory=True)

    def get_text(self):
        return self.text

    