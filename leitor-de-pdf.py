# Leitor de PDF
from langflow.custom import Component
from langflow.io import Output, DropdownInput, FileInput
from langflow.schema import Data
import fitz  # PyMuPDF
import json

class PdfToJsonComponent(Component):
    display_name = "PDF to JSON Component"
    description = "Convert a PDF file into a structured JSON format."
    documentation: str = "http://docs.langflow.org/components/pdf-to-json"
    icon = "file-text"
    name = "PdfToJsonComponent"

    # Definindo os inputs e outputs do componente
    inputs = [
        FileInput(
            name="path", 
            display_name="PDF Path", 
            file_types=["pdf"],
            info="Upload a PDF file for conversion.",
        ),
        DropdownInput(
            name="output_format", 
            display_name="Output Format", 
            info="Choose the output format for the PDF conversion.",
            options=["JSON", "Text"],
            value="JSON",  # Valor inicial
            tool_mode=True,
        ),
    ]

    outputs = [
        Output(display_name="JSON Output", name="output", method="build_output"),
    ]

    def build_output(self) -> Data:
        # Obtém os valores dos inputs corretamente
        pdf_path = self.path  # Acesso correto ao valor do input path
        output_format = self.output_format  # Acesso correto ao valor do input output_format
        
        # Função para converter PDF em JSON
        def pdf_to_json(pdf_path):
            try:
                doc = fitz.open(pdf_path)
                pdf_data = {}
                
                pdf_data["pages"] = []
                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)
                    page_text = page.get_text("text")
                    pdf_data["pages"].append({
                        "page_number": page_num + 1,
                        "text": page_text.strip()
                    })
                
                return pdf_data
            except Exception as e:
                # Retorna erro caso o arquivo PDF não possa ser lido
                raise ValueError(f"Error reading the PDF: {str(e)}")

        # Processa o PDF e gera o JSON
        try:
            json_data = pdf_to_json(pdf_path)
        except ValueError as e:
            return Data(value=str(e))  # Caso ocorra um erro, retornamos a mensagem de erro

        # Se o formato de saída for 'Text', apenas o texto é retornado
        if output_format == "Text":
            text_data = "\n".join([page["text"] for page in json_data["pages"]])
            data = Data(value=text_data)
        else:
            # Caso contrário, retorna o JSON
            data = Data(value=json.dumps(json_data, indent=4, ensure_ascii=False))

        self.status = data
        return data
