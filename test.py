import requests
import sys
import string
import re
import os.path
from keys import key

USAGE = 'usage: python3 test.py <test data> <index of letter to remove>'
ENDPT = 'https://api.cognitive.microsoft.com/bing/v7.0/spellcheck?text='
MAXLEN = 1450 - len(ENDPT)

def correct_text(orig, corrections):
    """
    given a json of corrections and the orig line, returns a string
    of the corrected version of orig
    """
    if not corrections:
        print('no suggestions')
        return orig.replace('\n', '')
    
    misspelled = corrections['flaggedTokens']
    text = orig.replace('\n', '')
    text = text.split(' ')
    for m in misspelled:
        offset = m['offset']
        i = orig[0:offset].count(' ')   # num spaces in substr from 0 -> offset
        suggestion = m['suggestions'][0]['suggestion']
        text[i] = suggestion
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
    """
    splits into lines with length 1450 (largest possible size for msft)
    """
    line = ""
    lines = []
    i = 0
    text_arr = full_text.split(' ')
    for word in text_arr:
        if len(line) + len(word + " ") >= MAXLEN:
            lines.append(line)
            line = ""
            i += 1
        line = line + word + " "
    lines.append(line)
    return lines

def read_text(fileobj):
    full_text = ""
    fname_og, fext = os.path.splitext(sys.argv[1])
    fname_og = os.path.basename(fname_og)
    orig_text = ''
    for line in fileobj:
        line = line.lstrip().rstrip()
        line = line.strip(string.punctuation)
        line = re.sub('[^A-Za-z0-9 ]+', '', line)
        orig_text = orig_text + line + ' '
        for word in line.split(' '):
            if not has_digits(word):
                word = misspell_text(word)
            full_text = full_text + word + " "
    orig_file = open(fname_og + '_orig' + fext, 'w+')
    orig_file.write(orig_text)
    orig_file.close()
    return full_text

def main():
    if len(sys.argv) != 3:
        print(USAGE)
        sys.exit(0)
    fname = sys.argv[1]
    fname_og, fext = os.path.splitext(fname)
    fname_og = os.path.basename(fname_og)
    try:
        full_text = ''
        original = ''
        compressed = ''
        corrected = ''        
        with open(fname) as fileobj:
            full_text = read_text(fileobj)
        text_arr = split_into_lines(full_text)
        for line in text_arr:
            if len(line) > MAXLEN:
                print("over", str(MAXLEN), "chars")
            else:
                compressed += line
                corrected += spell_check(line)
        comp_file = open(fname_og + '_compressed' + fext, 'w+')
        comp_file.write(compressed)
        comp_file.close()
        corr_file = open(fname_og + '_corrected' + fext, 'w+')
        corr_file.write(corrected)
        corr_file.close()
        
    except FileNotFoundError:
        print('file not found')

if __name__ == '__main__':
    main()