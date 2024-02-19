import sys
import numpy as np



# path = "/Users/alaintamazian/DocumentsAT/CSCI544/HWs/HW2_Hidden_Markov_Models/hmm-training-data/it_isdt_train_tagged.txt"
path = sys.argv[1]
# argv[0] is the name of the python file
# argv[1] argument is the directory path of the training data



fileIn = open(path, "r")
# text = fileIn.read()

# has the text seperated line by line into a list
linesL = fileIn.readlines()

text = fileIn.read()

fileIn.close()


# In[4]:


tokens_posL = []

for line in linesL:
    # turns each line into a list, where each element is a list with 0 being the word and 1 the POS
    tokensL = [word.split("/") for word in line.split()]
    
    # incase there are "/" inside a sentence, this block of code joins them together again
    # think of more efficient method ???
    for i, pair in enumerate(tokensL):
        if len(pair) > 2:
            tokensL[i] = [ "/".join(pair[:-1]), pair[-1] ]
    
    tokens_posL.append(tokensL)

# for line in linesL:
#     # turns each line into a list, where each element is a list with 0 being the word and 1 the POS
#     tokensL = [tuple(word.split("/")) for word in line.split()]
#     tokens_posL.append(tokensL)


# In[5]:


# vocabulary (i.e. word) in the training set, with its count as the value
vocabD = {}
# will use these counts to get the emission and transition probabilities

# the POS's in the training set, with its count as the value
posD = {}
# will use these counts to get the emission and transition probabilities

# emission matrix (as a dictionary)
# Every POS tag (ie states) will be a dictionary key
# The value will be a dictionary; where every key is a possible word (ie observation) and the value is the POS-word emission count 
emissionD = {}
# count(Wi | Ti) ; count of a word (ie observation) Wi, given that it's state (ie POS tag) is Ti
# Will use it to get, P(Wi | Ti) ; probability a word (ie observation) will be Wi given that it's state (ie POS tag) is Ti
# ??? Don't we want the inverse ???

# transition matrix (as a dictionary)
# Every POS tag (ie states) will be a dictionary key
# The value will be a dictionary; where every key is a possible preceding POS tag (ie preceding state) and the value is the PreviousPOS-POS count 
transitionD = {}
# count(Ti | Ti-1) ; count of a POS tag (ie state) Ti, given that it's preceding state (ie POS tag) is Ti-1
# Will use it to get, P(Ti | Ti-1) ; probability a POS tag (ie state) will be Ti given that it's preceding state (ie POS tag) is Ti-1

# the POS's in the training set, with its value being the number of times it is the initial (ie start) state
# technically can be considered part of the transition matrix; intuitively, I prefered having it seperate
startD = {}
# count(POS Tag | start) ; count of a POS tag (ie state), given it is a sentence's initial state
# P(POS Tag | start) ; probability of a POS tag (ie state), given it is a sentence's initial state

# the POS's in the training set, with its value being the number of times it is the end (ie last) state 
# technically can be considered part of the transition matrix; intuitively, I prefered having it seperate
endD = {}
# count(POS Tag | end) ; count of a POS tag (ie state), given it is a sentence's end state
# Will use it to get P(POS Tag | start) ; probability of a POS tag (ie state), given it is a sentence's end state


# In[6]:


# make more efficient


# In[7]:


for tokensL in tokens_posL:
    # tokensL is a line/sentence
    for i, token_pos in enumerate(tokensL):
        # tokensD.get(token, 0); the get() method returns the value/count of the token key if it exits; otherwise 0
        vocabD[token_pos[0]] = vocabD.get(token_pos[0], 0)+1
        posD[token_pos[1]] = posD.get(token_pos[1], 0)+1
        
#         print(i, token_pos, token_pos[1])
        
        if i == ( len(tokensL)-1 ):
            endD[token_pos[1]] = endD.get(token_pos[1], 0)+1
        
        if i == 0:
            startD[token_pos[1]] = startD.get(token_pos[1], 0)+1
        
                
        if token_pos[1] not in emissionD:
            emissionD[token_pos[1]] = {}
        if token_pos[0] in emissionD[token_pos[1]]:
            emissionD[token_pos[1]][token_pos[0]] += 1
        else:
            emissionD[token_pos[1]][token_pos[0]] = 1

        
#         emissionD[token_pos[1]] = {token_pos[0]: emissionD.get(token_pos[1], {token_pos[0]: 0})[token_pos[0]] +1 }
#         emissionD[token_pos[1]] = {token_pos[0]: emissionD[token_pos[1]].get(token_pos[0], 0) + 1 }

        
        if token_pos[1] not in transitionD:
            transitionD[token_pos[1]] = {}
        if tokensL[i-1][1] in transitionD[token_pos[1]]:
            transitionD[token_pos[1]][tokensL[i-1][1]] += 1
        else:
            transitionD[token_pos[1]][tokensL[i-1][1]] = 1
            
#         transitionD[token_pos[1]] = { tokensL[i-1][1]: transitionD.get(token_pos[1], {tokensL[i-1][1]: 0})[ tokensL[i-1][1] ] +1 }
#         transitionD[token_pos[1]] = {tokensL[i-1][1]: transitionD[token_pos[1]].get(tokensL[i-1][1], 0) + 1 }


#         print(tokensL[i-1][1], token_pos[1])
        

        
        
    
    
    
    


# In[ ]:





# In[8]:


# transforming counts into probabilities


# In[9]:


# # vocabulary (i.e. word) in the training set, with its count as the value
# vocabD = {}
# # will use these counts to get the emission and transition probabilities

# # the POS's in the training set, with its count as the value
# posD = {}
# # will use these counts to get the emission and transition probabilities

# ??? was it pointless to create the above dicts ?


# emission matrix (as a dictionary)
# Every POS tag (ie states) will be a dictionary key
# The value will be a dictionary; where every key is a possible word (ie observation) and the value is the POS-word emission probability 
emission_probD = {}
# P(Wi | Ti) ; probability a word (ie observation) will be Wi given that it's state (ie POS tag) is Ti
# ??? Don't we want the inverse ???
# count( word | tag) / Σ count(wordᵢ | tag)
# count( word | tag) / count(tag)


# transition matrix (as a dictionary)
# Every POS tag (ie states) will be a dictionary key
# The value will be a dictionary; where every key is a possible preceding POS tag (ie preceding state) and the value is the transition probability (between the child dict key and parent dict key)
transition_probD = {}
# P(Ti | Ti-1) ; probability a POS tag (ie state) will be Ti given that it's preceding state (ie POS tag) is Ti-1
# count( tag | previous tag) / Σ count(tagᵢ | previous tag)
# count( tag | previous tag) / count(previous tag)

# keys are the POS's in the training set, with its value being the probability that the POS is an initial (ie start) state 
# technically can be considered part of the transition matrix; intuitively, I prefered having it seperate
start_probD = {}
# P(POS Tag | start) ; probability of a POS tag (ie state), given it is a sentence's initial state
# count( tag | start state) / Σ count(tagᵢ | start state)
# count( tag | start state) / count(start state)

# keys are the POS's in the training set, with its value being the probability that the POS is an end (ie last) state 
# technically can be considered part of the transition matrix; intuitively, I prefered having it seperate
end_probD = {}
# P(POS Tag | end) ; probability of a POS tag (ie state), given it is a sentence's end state
# count( tag | end state) / count(end state)


# In[ ]:





# In[ ]:





# In[10]:


# count(end state) and count(start state) == len(tokens_posL)

total_lines = len(tokens_posL)

for pos, count in startD.items():
    start_probD[pos] = count/total_lines
    
for pos, count in endD.items():
    end_probD[pos] = count/total_lines
    


# In[11]:

# print(transitionD)
# print()

# creating transition_probD[cur_pos][prev_pos] = prob

for cur_pos in transitionD:
    prev_posD = transitionD[cur_pos]
    
    for prev_pos in prev_posD:
        trans_count = prev_posD[prev_pos]
        # ??? !!!
        prob = (trans_count) / (posD[prev_pos])
        
        if cur_pos not in transition_probD:
            transition_probD[cur_pos] = {prev_pos: prob}
        else:
            transition_probD[cur_pos][prev_pos] = prob




# creating emission_probD
for cur_pos in emissionD:
    wordsD = emissionD[cur_pos]
    
    for word in wordsD:
        emiss_count = wordsD[word]
        prob = (emiss_count) / (posD[cur_pos])
        
        if cur_pos not in emission_probD:
            emission_probD[cur_pos] = {word: prob}
        else:
            emission_probD[cur_pos][word] = prob
            


# In[13]:


# inverse of previous one: emission_probD
# parent key becomes the word and child key becomes the pos
emiss_probD = {}

for pos, wordsD in emission_probD.items():
    # print(pos)
    for word, prob in wordsD.items():
        if word not in emiss_probD:
            emiss_probD[word] = {}
        emiss_probD[word][pos] = prob
#         print(word)
#         break
#     break


# In[14]:


emission_probD = emiss_probD.copy()




# # In[15]:



# inverse of previous one; transition_probD
# parent key becomes the prev POS and child key becomes the cur POS
trans_probD = {}

for pos, prev_posD in transition_probD.items():
    for prev_pos, prob in prev_posD.items():
        if prev_pos not in trans_probD:
            trans_probD[prev_pos] = {}
        trans_probD[prev_pos][pos] = prob


transition_probD = trans_probD.copy()




# make more efficient; either set up transition and emission the correct way immediately
# or change it to the useful way after recreating the dict from text


# In[ ]:




open_cl_posL = []
# one way to define open-class words I think is:
# (# of unique tokens in state)/(# total unique tokens) >= 0.1
# 0.1 is arbitrary

for pos in posD:
    # number of unique tokens for this POS
    if ( len(emissionD[pos])/len(vocabD) ) >= 0.1:
        open_cl_posL.append(pos)


if len(open_cl_posL) < 4:
    
    open_cl_posL = []
    # one way to define open-class words I think is:
    # (# of unique tokens in state)/(# total unique tokens) >= 0.1
    # 0.1 is arbitrary

    for pos in posD:
        # number of unique tokens for this POS
        open_cl_posL.append((pos, len(emissionD[pos])/len(vocabD)))

    open_cl_posL.sort(key=lambda x:x[1], reverse=True)
    # 4 or 5 or 6; arbitrary, just like the 4 and 0.1 above
    open_cl_posL = [pos[0] for pos in open_cl_posL[:5]] 



    
# In[17]:


# transforming probabilities into text for output

# total_lines, posD, start_probD, end_probD, transition_probD, emission_probD
# dont need vocabD ???; we do to check if its a new word
# also the open-class pos list


# use with method ??? : with open("nbmodel.txt", "w") as fileOut
fileOut = open("hmmmodel.txt", "w")

fileOut.write(("This HMM was trained on a corpus with " + str(total_lines) + " lines\n\n"))

for pos, count in posD.items():
    fileOut.write(("The POS '" + pos + "' appears " + str(count) + " times\n"))
fileOut.write("\n")

fileOut.write(("The open-class labels are: " + str(open_cl_posL)[1:-1] + ".\n\n"))

for token, count in vocabD.items():
    fileOut.write(("The vocabulary token '" + token + "' is seen " + str(count) + " times\n"))
fileOut.write("\n")

for pos, prob in start_probD.items():
    fileOut.write(("The initial state probability of POS '" + pos + "' is: " + str(prob) + "\n"))
fileOut.write("\n")

for pos, prob in end_probD.items():
    fileOut.write(("The end state probability of POS '" + pos + "' is: " + str(prob) + "\n"))
fileOut.write("\n")

for prev_pos in transition_probD:
    for cur_pos in transition_probD[prev_pos]:
        fileOut.write(("The transition probability for '" + prev_pos + "' --> '" + cur_pos + "' is: " + str(transition_probD[prev_pos][cur_pos]) + "\n"))
fileOut.write("\n")

for token in emission_probD:
    for pos in emission_probD[token]:
        fileOut.write(("The emission probability for POS '" + pos + "' --> token '" + token + "' is: " + str(emission_probD[token][pos]) + "\n"))

fileOut.close()
