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
    st_orgl = str(st)          #original string
    stLow = st_orgl.lower()    #lower case string
    stLowLst = stLow.split()   #words list from lower case string
  
    for item in forb:          #checking the presence of each forbidden string in each element of list
        for i in range(len(stLowLst)):
            if item in stLowLst[i]:       #if this is forbidden string in element, we replace whole word with mute_sign's, even they are punctuation in word
                stLowLst[i] = mute_sign * len(stLowLst[i])

    stLowLst = list(' '.join(stLowLst))  #making char list from censored words list
    st_orgl_lst = list(st_orgl)          #making char list from original list

    for i in range(len(st_orgl_lst)):    #putting in censored list punctuation on the same positions, where they are in original string list. (We do it because we censored them cause they are part of words)
        if st_orgl_lst[i] in string.punctuation:
            stLowLst[i] = st_orgl_lst[i]

    for i in range(len(stLowLst)):    #To return in result original casing, we put in original string list muted_sign's on the same positions, where they are in censored list
        if stLowLst[i] == mute_sign:
            st_orgl_lst[i] = mute_sign

    return ''.join(st_orgl_lst)   #now joining original string list, that is already muted.
 
chat = input('Input some sentence:\n') 
print(censure(chat))
