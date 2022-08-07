'''
Variant 2. Censuring the whole word, that has forbidden substring.
Example:
Forbidden string - "freak"
You are freakboy! --> You are *******!
'''
import string


def censure(st):
    forb = ['freak']
    mute_sign = '♥'
    st_orgl = str(st)            # original string
    st_low = st_orgl.lower()     # lower case string
    st_low_lst = st_low.split()  # words list in lower case

    for item in forb:   
        for i in range(len(st_low_lst)):
            # If the word contains a forbidden substring, then
            # mute the whole word (including punctuation marks)
            if item in st_low_lst[i]:
                st_low_lst[i] = mute_sign * len(st_low_lst[i])

    st_low_lst = list(' '.join(st_low_lst))  # char list from modified string
    st_orgl_lst = list(st_orgl)              # char list from original string

    for i in range(len(st_orgl_lst) - len(st_low_lst)):  
        # Add empty elements to the end of the modified list,
        # so that the lists have the same length and their positions can be matched.
        # (This is necessary so that the indexOutOfRange error does not crash,
        # when there are spaces or hyphens at the end of the line)
        st_low_lst.append('')

    for i in range(len(st_orgl_lst)):  
        # For the list of the changed string, put line breaks and spaces at the same positions,
        # where and y of the original string. (Again, when splitting into a list using the split() method
        # we removed them, so we return)
        if st_orgl_lst[i] == '\n' and st_low_lst[i] == ' ':
            st_low_lst[i] = '\n'
        elif st_orgl_lst[i] == '\n' and st_low_lst[i] != '\n':
            st_low_lst.insert(i, '\n')
        elif st_orgl_lst[i] == ' ' and st_low_lst[i] != ' ':
            st_low_lst.insert(i, st_orgl_lst[i])   
    
    st_low_clean = []               
    # Create a new list based on the censored list,
    # but no padding empty elements added before the previous loop.
    # We do this so that the original and modified list of strings have the same length,
    # and there was no character offset when matching positions.
    for item in st_low_lst:
        if item != '':
            st_low_clean.append(item)
    
    for i in range(len(st_orgl_lst)):  
        # For the changed line, set the punctuation as in
        # of the original string (because along with the forbidden words
        # we censored the punctuation marks that are merged with them)
        if st_orgl_lst[i] in string.punctuation:
            st_low_clean[i] = st_orgl_lst[i]

    for i in range(len(st_low_clean)):    # We put mute_sign's on the original as on the changed line
        if st_low_clean[i] == mute_sign:
            st_orgl_lst[i] = mute_sign

    return ''.join(st_orgl_lst)
 
    
chat = input('Input some sentence:\n') 
print(censure(chat))
