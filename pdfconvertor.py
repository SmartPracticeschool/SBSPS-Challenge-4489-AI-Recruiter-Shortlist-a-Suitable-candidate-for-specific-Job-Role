from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io
import pandas as pd
import spacy
from spacy.matcher import Matcher
from spacy.lang.en import English

# load pre-trained model
nlp = spacy.load('en_core_web_sm')
#doc = nlp(text)
#noun_chunks = doc.noun_chunks

def extract_skills(resume_text):
    nlp_text = nlp(resume_text)

    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text if not token.is_stop]
    
    # reading the csv file
    data = pd.read_csv("skills.csv") 
    #print(data)
    # extract values
    skills = list(data.columns.values)
    #print(tokens)
    skillset = []
    
    # check for one-grams (example: python)
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)
    #print(skillset)
    # check for bi-grams and tri-grams (example: machine learning)
    #for token in noun_chunks:
    #    token = token.text.lower().strip()
    #    if token in skills:
    #        skillset.append(token)
    
    return [i.capitalize() for i in set([i.lower() for i in skillset])]


def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as fh:
        # iterate over all pages of PDF document
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            # creating a resoure manager
            resource_manager = PDFResourceManager()
            
            # create a file handle
            fake_file_handle = io.StringIO()
            
            # creating a text converter object
            converter = TextConverter(
                                resource_manager, 
                                fake_file_handle, 
                                codec='utf-8', 
                                laparams=LAParams()
                        )

            # creating a page interpreter
            page_interpreter = PDFPageInterpreter(
                                resource_manager, 
                                converter
                            )

            # process current page
            page_interpreter.process_page(page)
            
            # extract text
            text = fake_file_handle.getvalue()
            yield text

            # close open handles
            converter.close()
            fake_file_handle.close()
text = ""


# calling above function and extracting text
for page in extract_text_from_pdf("static/images/{}/{}".format("user_rayan","CS5A_44_RIBAJACOB.pdf")):
    text += ' ' + page
print("Skills extracted from user : ",end = " ")
print(extract_skills(text))










