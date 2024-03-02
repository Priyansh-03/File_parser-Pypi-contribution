import chardet
import os
from PyPDF2 import PdfReader, PdfWriter

# from unstructured.partition.auto import partition #detecting file formats and extracting content [to install --> pip install "unstructured[all-docs]"]

def detect_file(file_path): #detect extentions
    if file_path.lower().endswith('.pdf'):
        return 'pdf'
    elif file_path.lower().endswith('.txt'):
        return 'text'
    elif file_path.lower().endswith('.epub'):
        return 'epub'
    else:
        print("Unknown file format.")
        return ""



def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        confidence = result['confidence']
        return encoding

def get_pdf_metadata(pdf_path):
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        info = reader.metadata
    return info

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        results = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                results.append(text)
            else:
                results.append("[Text could not be extracted from this page]")
        return " ".join(results)


def split_pdf_and_output(pdf_path):
    output_dir = "extracted_pages"  # Name of the output folder
    os.makedirs(output_dir, exist_ok=True)  # Create the output folder if it doesn't exist

    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        for page_num in range(len(reader.pages)):
            writer = PdfWriter()
            writer.add_page(reader.pages[page_num])
            
            output_filename = os.path.join(output_dir, f"page_{page_num + 1}.pdf")
            with open(output_filename, "wb") as out:
                writer.write(out)
            
            print(f"Created: {output_filename}")

def read_text_file(file_path):
    with open(file_path, "r", encoding=detect_encoding(file_path)) as f:
        text = f.read()
    return text
    
def write_text_output(output_path,content):
    content = "\n".join(content)
    with open(output_path,"w",encoding='utf-8') as f:
        text=f.write(content)
        return text

# def read_file(file_path):
#     elements = partition(file_path)
#     text_content = "\n\n".join([str(el) for el in elements])
#     return text_content


# Example usage
# if __name__ == "__main__":
#     pdf_path = browse_files() # Replace this with the path to your PDF file or use browse_files()
#     # metadata = get_pdf_metadata(pdf_path)
#     # print("Metadata:", metadata)
    
#     extracted_text = extract_text_from_pdf(pdf_path)
#     # print("Extracted Text:", extracted_text)
    
#     split_pdf(pdf_path)