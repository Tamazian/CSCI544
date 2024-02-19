# imports

import os
import sys


# stop words
stopWordsL = ["i", "me", "we", "my", "myself", "our", "ourself", "you", "your", "yourself", "he", "him", "hi", "himself", "she", "her", "herself", "it", "itself", "they", "them", "their", "themself", "what", "which", "who", "whom", "thi", "that", "thes", "thos", "am", "are", "wa", "were", "be", "been", "hav", "ha", "had", "do", "did", "a", "an", "the", "and", "but", "if", "or", "because", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "befor", "after", "abov", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "only", "own", "so", "than", "too", "very", "ca", "can", "wo", "will", "just", "should", "now", "th"]
sigL = ['relax', 'stay', 'hotel', 'location', 'room', 'chicago', 'seem', 'final', 'plac', 'walk', 'recommend', 'call', 'husband', 'u', 'great', 'went', 'visit', 'look', 'hour', 'definit', 'smell', 'michigan', 'elevator', 'block', 'charg']


# not just tokenizing but also includes other processes like removing punctuation
def tokenize(text):
    tokensL = text.split()
    i = len(tokensL)

    addTokensL = []

    for token in tokensL[::-1]:
        i -= 1
    #     print(token)
    
        # if a token is completely removed, we just continue through the iterations
        cont = False

        # removing all punctuations (including apostrophies)
        if (not token.isalpha()) and (not token.isdigit()):

            while (not token[-1].isalpha()) and (not token[-1].isdigit()):
                if len(token) <= 1:
    #                 print(token)
                    del tokensL[i]
        
                    cont = True
                    break

                else:
                    token = token[:-1]
                    tokensL[i] = token
    #                 print(token)
            if cont:
                continue
        
            # rewrite to make less redunant (ie more efficient) ???
            while (not token[0].isalpha()) and (not token[0].isdigit()):
                if len(token) <= 1:
    #                 print(token)
                    del tokensL[i]
        
                    cont = True
                    break

                else:
                    token = token[1:]
                    tokensL[i] = token
    #                 print(token)   
            if cont:
                continue


            # I think it is a good idea to keep "not", maybe even create a word pair token
            # Otherwise, "It was not good" -> "good"; we want "not good"
            if token[-3:] == "n't":
                tokensL.insert(i+1, "not")
                token = token[:-3]
                tokensL[i] = token

            if "'" in token:
                idx = token.find("'")
                token = token[:idx]
                tokensL[i] = token


        # lemmatization/stemming: s, ing, ed, ies
            # which is it ???
            # Think of a better way if can
        # Are there other major ones ???
        if token[-3:] == "ies":
            token = token[:-3] + "y"
            tokensL[i] = token
        if token[-1:] == "s":
            token = token[:-1]
            tokensL[i] = token
        if token[-3:] == "ing":
            token = token[:-3]
            tokensL[i] = token
        if token[-2:] == "ed":
            token = token[:-2]
            tokensL[i] = token 
        if token[-2:] == "ly":
            token = token[:-2]
            tokensL[i] = token 


        # removing stop words
        if token in stopWordsL:
            del tokensL[i]
            continue


        if token[-1:] == "e":
            token = token[:-1]
            tokensL[i] = token

        
        if token in sigL:
            addTokensL.append(token)

    tokensL += addTokensL

    # implement "re" library for better preprocessing ???
    # later; if time
    
    return tokensL




# In[6]:


# what to do with cases like: "ago.........i'm"
# Can i just write them off like misplellings ?

# For now yes, 
# reconsider after finishing the rest of there's time and its needed


# In[7]:


# print(chr(65))
# print(ord("a"))


# In[ ]:





# In[11]:


# root_file = "/Users/alaintamazian/DocumentsAT/CSCI544/Coding/train_data"
root_file = sys.argv[1]
# argv[0] is the name of the python file
# argv[1] argument is the directory path of the data set

pathsL = []
for (root, dirs, files) in os.walk(root_file, topdown=False):
    # if there are no subdirectories in a "root" directory (i.e. there are only files), we add it to pathsL
    if not dirs:
        pathsL.append(root)


# In[12]:



# not sure if i need this portion; since based on the given directory they all have the same number of reviews
# so the probability for each should be 0.5
pos_pathsL = []
neg_pathsL = []
true_pathsL = []
false_pathsL = []

for path in pathsL:
    if "positive" in path:
        pos_pathsL.append(path)
    elif "negative" in path:
        neg_pathsL.append(path)
    
    if "truthful" in path:
        true_pathsL.append(path)
    elif "deceptive" in path:
        false_pathsL.append(path)


# number of reviews from each class
pos_count = []
neg_count = []
true_count = []
false_count = []
# adding to an integer in a loop didn't work for some reason

# class_pathsL = [pos_pathsL, neg_pathsL, true_pathsL, false_pathsL]

for class_pathsL, class_count in [(pos_pathsL, pos_count), (neg_pathsL, neg_count), (true_pathsL, true_count),
                                  (false_pathsL, false_count)]:
    for path in class_pathsL:
        for (root, dirs, files) in os.walk(path, topdown=False):
            class_count.append(len(files))

    class_count = sum(class_count)

pos_prob = sum(neg_count)/( sum(pos_count)+sum(neg_count) )
neg_prob = sum(pos_count)/( sum(pos_count)+sum(neg_count) )
true_prob = sum(true_count)/( sum(true_count)+sum(false_count) )
false_prob = sum(false_count)/( sum(true_count)+sum(false_count) )
# Since there is an equal split of the files among the 4 classes, all the probs are 0.5
# I didn't hardcode it though, so that it would be useable for other training data too


# In[ ]:





# In[15]:


# creating a dictionary with all the tokens as keys (and it's counts as values)
# tokensD is the total
tokensD = {}
pos_tokensD = {}
neg_tokensD = {}
true_tokensD = {}
false_tokensD = {}

# why/how are neg and true almost identical ???


for subdir in pathsL:
    for (root, dirs, files) in os.walk(subdir, topdown=False):
        
        for fileName in files:
            if fileName.endswith(".txt"):
                path = root + "/" + fileName

                fileIn = open(path, "r")
                text = fileIn.read()

                fileIn.close()

                text = text.lower()
                tokensL = tokenize(text)

                for token in tokensL:
                    if "positive" in path:
                        pos_tokensD[token] = pos_tokensD.get(token, 0) + 1
                    elif "negative" in path:
                        neg_tokensD[token] = neg_tokensD.get(token, 0) + 1

                    if "truthful" in path:
                        true_tokensD[token] = true_tokensD.get(token, 0) + 1
                    elif "deceptive" in path:
                        false_tokensD[token] = false_tokensD.get(token, 0) + 1

                    tokensD[token] = tokensD.get(token, 0) + 1


# In[ ]:





# In[16]:



uniqTokenCount = len(tokensD)

# We want to get the total number of tokens that appear in all reviews for each class
# This is the denominator for the prob of each token (given the class)
count1 = 0
for word in pos_tokensD.values():
    count1 += word
posTokenCount = count1

count2 = 0
for word in neg_tokensD.values():
    count2 += word
negTokenCount = count2
  
count3 = 0
for word in true_tokensD.values():
    count3 += word
trueTokenCount = count3

count4 = 0
for word in false_tokensD.values():
    count4 += word
falseTokenCount = count4


# In[17]:


# We create a new dictionary that has the probability of each token (not the count)
# We will also apply add-one smoothing
# We will add 1 to the numerator and uniqTokenCount to the denimator (of the prob) ???

pos_tokens_probD = {}
neg_tokens_probD = {}
true_tokens_probD = {}
false_tokens_probD = {}

for token in tokensD:
    # tokensD.get(token, 0) > the get() method returns the value/count of the token key if it exits; otherwise 0
    pos_token_prob = (pos_tokensD.get(token, 0) +1) / (posTokenCount + uniqTokenCount)
    # with smoothing
    pos_tokens_probD[token] = pos_token_prob
    
    neg_token_prob = (neg_tokensD.get(token, 0) +1) / (negTokenCount + uniqTokenCount)
    neg_tokens_probD[token] = neg_token_prob
    
    true_token_prob = (true_tokensD.get(token, 0) +1) / (trueTokenCount + uniqTokenCount)
    true_tokens_probD[token] = true_token_prob
    
    false_token_prob = (false_tokensD.get(token, 0) +1) / (falseTokenCount + uniqTokenCount)
    false_tokens_probD[token] = false_token_prob






# Why did using print(file=) work on Jupyter notebook to write to a text file, but not here ???

# # In[19]:
# fileOut = open("nbmodel.txt", "w")
#
# print("The probability of a positive hotel review is:", pos_prob, file=fileOut)
# print("The probability of a negative hotel review is:", neg_prob, file=fileOut)
 # print("The probability of a false hotel review is:", false_prob, file=fileOut)
# print("", file=fileOut)
#
#
# # In[20]:
# for token in tokensD:
#     print("The probability of token \"" + token + "\" occurring among positive reviews is:", pos_tokens_probD[token], file=fileOut)
#     print("The probability of token \"" + token + "\" occurring among negative reviews is:", neg_tokens_probD[token], file=fileOut)
#     print("The probability of token \"" + token + "\" occurring among truthful reviews is:", true_tokens_probD[token], file=fileOut)
#     print("The probability of token \"" + token + "\" occurring among deceptive reviews is:", false_tokens_probD[token], file=fileOut)


# In[19]:
# fileOut = open("nbmodel.txt", "w")

# use with method ??? : with open("nbmodel.txt", "w") as fileOut
fileOut = open("nbmodel.txt", "w")

fileOut.write(("The probability of a positive hotel review is: " + str(pos_prob) + "\n"))
fileOut.write(("The probability of a positive hotel review is: " + str(neg_prob) + "\n"))
fileOut.write(("The probability of a true hotel review is: " + str(true_prob) + "\n"))
fileOut.write(("The probability of a false hotel review is: " + str(false_prob) + "\n\n"))

for token in tokensD:
    fileOut.write(("The probability of token \"" + token + "\" occurring among positive reviews is: " + str(pos_tokens_probD[token]) + "\n"))
    fileOut.write(("The probability of token \"" + token + "\" occurring among negative reviews is: " + str(neg_tokens_probD[token]) + "\n"))
    fileOut.write(("The probability of token \"" + token + "\" occurring among truthful reviews is: " + str(true_tokens_probD[token]) + "\n"))
    fileOut.write(("The probability of token \"" + token + "\" occurring among deceptive reviews is: " + str(false_tokens_probD[token]) + "\n"))

fileOut.close()

