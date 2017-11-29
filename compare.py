"""
1. open two files 
2. check that two files have same number of words
3. comparing word by word:
    - are we comparing the same word? how to double check that we're comparing
      corresponding words (i.e. if msft returns a phrase as opposed to a single
      word)?
"""
import sys

USAGE = 'usage: python3 compare.py <text file 1> <text file 2>'

def similarity_of(f1, f2):
    """
    todo:
    * how to compare words? levenshtein distance?
    """
    txt1 = ''
    txt2 = ''
    all_c = 0
    mismatch = 0
    for line in f1:
        txt1 += line
    for line in f2:
        txt2 += line
    txt1 = txt1.split(' ')
    txt2 = txt2.split(' ')
    for w1, w2 in zip(txt1, txt2):
        for a, b in zip(w1, w2):
            all_c += 1
            if a != b:
                mismatch += 1
    print('1st file has', str(len(txt1)), 'words; 2nd file has', str(len(txt2)),
          'words')
    print('all chars:', str(all_c), 'mismatch:', str(mismatch))
    return
    
def main():
    if len(sys.argv) != 3:
        print(USAGE)
        return
    fname1 = sys.argv[1]
    fname2 = sys.argv[2]

    try:
        with open(fname1) as f1:
            with open(fname2) as f2:
                similarity_of(f1, f2)
    except FileNotFoundError:
        print ("file not found")
    return

if __name__ == '__main__':
    main()