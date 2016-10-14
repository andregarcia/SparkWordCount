
import re

def normalize_text(s):
    s = re.sub("[^\w\d\s]", "", s)
    s = re.sub("\s+", " ", s)
    s = s.lower()
    return s


