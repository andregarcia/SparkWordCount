
import re

def normalize_text(s):
    s = re.sub("[^\w\d\s]", "", s)
    s = re.sub("\s+", " ", s)
    s = s.lower()
    return s


import unicodedata
def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')