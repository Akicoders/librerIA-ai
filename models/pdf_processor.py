import pdfplumber as pp

class PDFProcessor:
    def __init__(self, path: str):
        self.path = path
        self.text = ""
        self.process()

    def process(self):
        with pp.open(self.path) as pdf:
            for page in pdf.pages:
                self.text += page.extract_text()
                return self.text

    def get_text(self):
        return self.text

    