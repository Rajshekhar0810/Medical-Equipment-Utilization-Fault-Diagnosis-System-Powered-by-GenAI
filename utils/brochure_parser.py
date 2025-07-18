# Purpose : Extracts plain text from a PDF brochure using PyMuPDF
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """
    Extracts plain text from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF.
    """
    try:
        # Open the pdf file
        doc = fitz.open(pdf_path)   #doc becomes a document object representing the whole PDF.



        text = ""    #Initializes an empty string text
        for page in doc :
            text += page.get_text()      #get_text() extracts all text content from that page.
            doc.close()  # Close the document after extraction
            return text  # Return the extracted text
        
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from PDF: {e}")    
    


#This function safely opens a PDF file, extracts all text from every page, and returns the full text as a single string
# It handles errors gracefully by raising a clear runtime error if something fails.    