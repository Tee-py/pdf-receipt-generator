from typing import Any
import uuid
from django.template.loader import get_template
from weasyprint import HTML
from django.core.files.base import ContentFile



def generate_id():
    return uuid.uuid4().hex

def generate_rid():
    return uuid.uuid4().hex[:11].upper()

class PDFGenerator:

    def __init__(self, template_path: str) -> None:
        self.template = get_template(template_path)

    def generate_pdf(self,  data: dict) -> Any:
        html = HTML(string=self.template.render(data))
        pdf = ContentFile(html.write_pdf(), name=f'recpt-{data["receipt_id"]}.pdf')
        return pdf
