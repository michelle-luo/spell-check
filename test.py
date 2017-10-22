import requests
import keys
import time

def misspell_text(original, misspelled):
    pass

def correct_text(original, corrections):
    if len(corrections['flaggedTokens']) == 0:
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

def main():
    fname = input('provide file for testing data\n')
    try: 
        with open(fname) as fileobj:
            print('correcting', fname)
            for line in fileobj:
                time.sleep(1)
                if len(line) < 3:
                    continue
                url = 'https://api.cognitive.microsoft.com/bing/v7.0/spellcheck?text=' + line
                headers = {'Ocp-Apim-Subscription-Key': keys.key1, 'setLang': 'EN' }
                r = requests.get(url, headers=headers)
                if r.status_code == requests.codes.ok:
                    results = correct_text(line, r.json())
                    print(results)
                else:
                    print(r.text)
    except FileNotFoundError:
        print('file not found')

if __name__ == '__main__':
    main()