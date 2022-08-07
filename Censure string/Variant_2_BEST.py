'''
Variant 2. Censuring the whole word, that has forbidden substring.
Example:
Forbidden string - "freak"
You are freakboy! --> You are *******!
'''
import string


def censure(st):
    forb = ['freak']
    mute_sign = '*'
    st_orgl = str(st)          # original string
    st_low = st_orgl.lower()    # lower case string
    st_low_lst = st_low.split()   # words list from lower case string
  
    for item in forb:          # checking the presence of each forbidden string in each element of list
        for i in range(len(st_low_lst)):
            if item in st_low_lst[i]:       # if this is forbidden string in element, we replace whole word with mute_sign's, even they are punctuation in word
                st_low_lst[i] = mute_sign * len(st_low_lst[i])

    st_low_lst = list(' '.join(st_low_lst))  # making char list from censored words list
    st_orgl_lst = list(st_orgl)          # making char list from original list
    
    for i in range(len(st_orgl_lst) - len(st_low_lst)):  # We add empty elements to the end of the modified list so that the lists have the same length and their positions can be compared. (This is necessary so that the indexOutOfRange error does not crash when there are spaces at the end of the line)
        st_low_lst.append('')
    
    for i in range(len(st_orgl_lst)):  # for the list of the changed line, we insert spaces, if they were not, at the same positions as they were in the original. (This is necessary for situations where the original string had several spaces between words, and when split into a list using the split() method, we removed them)
        if st_orgl_lst[i] == ' ' and st_low_lst[i] != ' ':
            st_low_lst.insert(i, st_orgl_lst[i])
        
    for i in range(len(st_orgl_lst)):  # for the list of the modified string, we put the line break characters at the same positions as the original string. (Again, when splitting into a list using the split() method, we removed them, so we return)
        if st_orgl_lst[i] == '\n':
            st_low_lst[i] = '\n' 

    for i in range(len(st_orgl_lst)):    # putting in censored list punctuation on the same positions, where they are in original string list. (We do it because we censored them cause they are part of words)
        if st_orgl_lst[i] in string.punctuation:
            st_low_lst[i] = st_orgl_lst[i]

    for i in range(len(st_low_lst)):    # To return in result original casing, we put in original string list muted_sign's on the same positions, where they are in censored list
        if st_low_lst[i] == mute_sign:
            st_orgl_lst[i] = mute_sign

    return ''.join(st_orgl_lst)   # now joining original string list, that is already muted.
 
    
chat = input('Input some sentence:\n') 
print(censure(chat))
