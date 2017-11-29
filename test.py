import requests
import time
import sys
import string
import re
from keys import key

USAGE = 'usage: python3 test.py <test data> <index of letter to remove>'
ENDPT = 'https://api.cognitive.microsoft.com/bing/v7.0/spellcheck?text='
MAXLEN = 1450 - len(ENDPT)

def correct_text(original, corrections):
    """
    given a json of corrections and the original line, returns a string
    of the corrected version of original
    """
    if len(corrections['flaggedTokens']) == 0:
        print('no suggestions')
        return original.replace('\n', '')
    misspelled = corrections['flaggedTokens']
    text = original.replace('\n', '')
    text = text.split(' ')
    for m in misspelled:
        offset = m['offset']
        # how many spaces in substring from 0 -> offset?
        word_to_replace_i = original[0:offset].count(' ')
        suggestion = m['suggestions'][0]['suggestion']
        text[word_to_replace_i] = suggestion
    return ' '.join(text)

def spell_check(text):
    """
    send a string of text to bing for correction & return corrected version
    """
    if len(text) < 3:
        return
    url = ENDPT + text
    headers = {'Ocp-Apim-Subscription-Key': key, 'setLang': 'EN' }
    r = requests.get(url, headers=headers)
    if r.status_code == requests.codes.ok:
        results = correct_text(text, r.json())
        return results
    else:
        return str(r.status_code) + r.text

def misspell_text(line):
    """ 
    systematically misspell each word in a line
    * first try: removing the second letter from each word
    """
    try:
        j = int(sys.argv[2])
    except ValueError as exception:
        print('index of letter to remove must be of type int')
        sys.exit(1)
        
    line = line.split(' ')
    for i in range(len(line)):
        if len(line[i]) > j + 1:
            line[i] = line[i].replace(line[i][j], '', 1)
    return ' '.join(line)

def has_digits(s):
    return any(c.isdigit() for c in s)

def split_into_lines(full_text):
    line = ""
    lines = []
    i = 0
    text_arr = full_text.split(' ')
    for word in text_arr:
        # line = line + word + " "
        if len(line) + len(word + " ") >= MAXLEN:
            lines.append(line)
            line = ""
            i += 1
        line = line + word + " "
    lines.append(line)
    return lines

def read_text(fileobj):
    full_text = ""
    for line in fileobj:
        line = line.lstrip().rstrip()
        line = line.strip(string.punctuation)
        line = re.sub('[^A-Za-z0-9 ]+', '', line)
        for word in line.split(' '):
            if not has_digits(word):
                word = misspell_text(word)
            full_text = full_text + word + " "
    return full_text

def main():
    if len(sys.argv) != 3:
        print(USAGE)
        sys.exit(0)
    
    fname = sys.argv[1]
    try:
        full_text = ''
        text = ''
        with open(fname) as fileobj:
            full_text = read_text(fileobj)
        text_arr = split_into_lines(full_text)
        i = 0
        orig_mode = True
        for line in text_arr:
            if len(line) > MAXLEN:
                print("over", str(MAXLEN), "chars")
            else:
                i += 1
                if orig_mode:
                    text += line
                else:
                    text += spell_check(line)
        print(text)
    except FileNotFoundError:
        print('file not found')

if __name__ == '__main__':
    main()