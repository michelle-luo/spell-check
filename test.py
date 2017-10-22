import requests
import time
import sys
from keys import key

def correct_text(original, corrections):
    """
    given a json of corrections and the original line, returns
    a string of the corrected version of original
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
    send a string of text to bing for correction
    """
    if len(text) < 3:
        return
    url = 'https://api.cognitive.microsoft.com/bing/v7.0/spellcheck?text=' + text
    headers = {'Ocp-Apim-Subscription-Key': key, 'setLang': 'EN' }
    r = requests.get(url, headers=headers)
    if r.status_code == requests.codes.ok:
        results = correct_text(text, r.json())
        return results
    else:
        return r.text

def misspell_text(line):
    """ 
    systematically misspell each word in a line: 
    first try: removing the second letter from each word    
    """
    line = line.split(' ')
    for i in range(len(line)):
        if len(line[i]) > 2:
            line[i] = line[i].replace(line[i][1], '')
    return ' '.join(line)

def main():
    if len(sys.argv) != 2:
        print("usage: python3 test.py <test-data>")
        return
    fname = sys.argv[1]
    try: 
        with open(fname) as fileobj:
            print('correcting', fname)
            for line in fileobj:
                # one request to msft per second :(
                time.sleep(1.25)
                line = misspell_text(line)
                print(spell_check(line))
    except FileNotFoundError:
        print('file not found')

if __name__ == '__main__':
    main()