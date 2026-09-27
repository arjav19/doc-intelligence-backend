import os 
from pypdf import PdfReader

class DocumentExtractor:
    @staticmethod
    def extract_text(file_path: str,max_pages: int= 10) -> tuple[str,int]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = os.path.splitext(file_path)[1].lower()

        if ext == '.txt':
            with open(file_path,'r',encoding='utf-8',errors='ignore') as f:
                return f.read(), 1

        elif ext == '.pdf':
            reader =PdfReader(file_path)
            total_pages = len(reader.pages)
            pages_to_read = min(total_pages, map_pages)

            text_parts = []
            for i in range(pages_to_read):
                page_text = reader.pages[i].extract_text()
                if page_text;
                    text_parts.append(page_text.strip())

            return "\n\n".join(text_parts),total_pages

        return "",0