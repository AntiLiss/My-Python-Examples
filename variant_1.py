'''
Variant 1. Censures the part of the word that is forbidden. 
Example: 
Forbidden word - "freak".
You are freakboy! --> You are ****boy!
'''

def censure(sentence):
    forbidden = ['freak']           #forbidden strings
    mute_sign = '*'
    st_orgl = str(sentence)          #original casing string
    st_lwr = str(sentence).lower()   #lower casing string

    for bword in forbidden:         #muting forbidden substring in st_lwr, if they are
        if bword in st_lwr:
            st_lwr = st_lwr.replace(bword, mute_sign * len(bword))    
    
    #Now to return in the result original string casing do next steps:
    
    st_orgl_lst = list(st_orgl)   #making char lists from both strings (original and muted)
    st_lwr_lst = list(st_lwr)

    for i in range(len(st_lwr_lst)):  #putting mute_signs in original string list in the same positions where they are in censored string
        if st_lwr_lst[i] == mute_sign:
            st_orgl_lst[i] = mute_sign

    return ''.join(st_orgl_lst)    #return joined list
 
inp = input('Input sentence:\n')
print(censure(inp))
