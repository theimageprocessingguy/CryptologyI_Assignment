import requests
import re
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import numpy as np

# Web scrapping
corpus=''
url = ['https://en.wikipedia.org/wiki/India',
       'https://en.wikipedia.org/wiki/Barack_Obama',
       'https://en.wikipedia.org/wiki/Lionel_Messi',
       'https://en.wikipedia.org/wiki/Stephen_Hawking',
       'https://en.wikipedia.org/wiki/Harry_Potter',
       'https://en.wikipedia.org/wiki/Leonardo_DiCaprio',
       'https://en.wikipedia.org/wiki/Albert_Einstein',
       'https://en.wikipedia.org/wiki/William_Shakespeare',
       'https://en.wikipedia.org/wiki/Bill_Gates',
       'https://en.wikipedia.org/wiki/Elon_Musk',
       'https://en.wikipedia.org/wiki/Tom_Cruise',
       'https://en.wikipedia.org/wiki/New_York_City',
       'https://en.wikipedia.org/wiki/World_War_I',
       'https://en.wikipedia.org/wiki/Adolf_Hitler',
       'https://en.wikipedia.org/wiki/Cristiano_Ronaldo',
       'https://en.wikipedia.org/wiki/Steve_Jobs',
       'https://en.wikipedia.org/wiki/World_War_II',
       'https://en.wikipedia.org/wiki/Google',
       'https://en.wikipedia.org/wiki/Facebook',
       'https://en.wikipedia.org/wiki/YouTube']
for webpage in url:
    print('Parsing: ',webpage)
    res = requests.get(webpage)
    soup = BeautifulSoup(res.text, 'html.parser')
    for i in soup.find_all('p'):
        corpus = corpus + i.text

# Pre-processing
corpus = corpus.lower()       
corpus = re.sub('[^a-z]+', '', corpus)

# Frequency counter
freq_dict = {}
for i in corpus:
    if i in freq_dict.keys():
        freq_dict[i] += 1
    else:
        freq_dict[i] = 1

# Frequency Percentage 
k = []
val = []  
for i,j in freq_dict.items():
    k.append(i)
    val.append(j/len(corpus) * 100)
    
temp_list = sorted(zip(k,val))
k = []
val = []  
for i,j in temp_list:
    k.append(i)
    val.append(j)

# Plotting the graph    
x_pos = [i for i, _ in enumerate(k)]

plt.bar(x_pos, val, color='green')
plt.xlabel("Letters")
plt.ylabel("Frequency")
plt.title("Frequency Analysis")
val1 = ['%d'%ii+'%' for ii in (np.arange(0,14,2)).tolist()]
plt.xticks(x_pos, k)
plt.yticks((np.arange(0,14,2)).tolist(), val1)

plt.savefig('freq_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

    
    

    
        
        
    