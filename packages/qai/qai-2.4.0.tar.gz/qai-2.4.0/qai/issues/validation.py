import re
from nltk import sent_tokenize

class Validator:
    
    html_pattern = re.compile("<.*?>")

    def __init__(
        self,
        sentence_token_limit=1024,
        ignore_html=True,
    ):
        self.sentence_token_limit = sentence_token_limit
        self.ignore_html = ignore_html

    def has_html(self, segment:str):
        return self.html_pattern.match(segment)!=None

    def is_empty(self, segment:str):
        return len(segment.strip())==0

    def too_long(self, segment:str):
        if len(sent_tokenize(segment))==1:     
            if len(segment.strip().split())>self.sentence_token_limit:
                return True
        return False
            
    def __call__(self, segment:str):
        
        # filter out segments containing html tags
        if self.ignore_html and self.has_html(segment) is True:
            return False

        # filter out whitespaces, empty segments
        if self.is_empty(segment):
            return False
        
        # filter out too long sentences
        if self.too_long(segment):
            return False
        
        return True