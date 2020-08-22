perms = []
#Recursive function for computing permutation
def permute_str(mystr,sta):
    if len(mystr) == 1:
        perms.append(sta+mystr)
        return
    for i in range(len(mystr)):
        permute_str(mystr[0:i]+mystr[i+1:len(mystr)],sta+mystr[i])
    return

print('Enter the string : ')
s = input()
if len(s) > 0:
    permute_str(s,'')
    print('The permutations are:')
    print(list(set(perms)))
else:
    print('Please provide valid input')
