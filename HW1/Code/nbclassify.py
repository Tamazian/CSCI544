# imports

import os
import sys
import numpy as np


# # local file import, for preprocesing function
# from nblearn import tokenize

# # It works, but maybe we aren't supposed to do this ???
# # Should I just copy and paste the whole function

# # Otherwise, why recreate a token probability dictionary from the text file
# # When it exists in the nblearn.py file ???


# In[ ]:


# Not sure if we were allowed to do a local file import like the cell above;
# The following function is just a copy and paste from nblearn.py

# not just tokenizing but also includes other processes like removing punctuation
def tokenize(text):
    tokensL = text.split()
    i = len(tokensL)

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

            
    # implement "re" library for better preprocessing ???
    # later; if time
    
    return tokensL




# turn the nbmodel text into a dictionary (as well as create variables for the prior probs)

# ???
# nblearn should output "nbmodel.txt" in it's own directory
# what if nbclassify and nblearn aren't in the same directory
probs_file = "nbmodel.txt"
nbmodel = open(probs_file, "r")

pos_prob = float( nbmodel.readline().split()[-1] )
neg_prob = float( nbmodel.readline().split()[-1] )
true_prob = float( nbmodel.readline().split()[-1] )
false_prob = float( nbmodel.readline().split()[-1] )
nbmodel.readline()

pos_tokens_probD = {}
neg_tokens_probD = {}
true_tokens_probD = {}
false_tokens_probD = {}


for line in nbmodel:
    lineL = line.split()
    prob = float(lineL[-1])
    
    for word in lineL:
        if "\"" in word:
            token = word[1:-1]
    
    if "positive" in lineL:
        pos_tokens_probD[token] = prob
    elif "negative" in lineL:
        neg_tokens_probD[token] = prob
    elif "truthful" in lineL:
        true_tokens_probD[token] = prob
    elif "deceptive" in lineL:
        false_tokens_probD[token] = prob
    
#     break


# In[5]:



# test_file = "/Users/alaintamazian/DocumentsAT/CSCI544/Coding/test_data"
test_file = sys.argv[1]
# argv[0] is the name of the python file
# argv[1] argument is the directory path of the data set

pathsL = []
for (root, dirs, files) in os.walk(test_file, topdown=False):    
    # if there are no subdirectories in a "root" directory (i.e. there are only files), we add it to pathsL
    if not dirs:
        pathsL.append(root)


# In[6]:


stopWordsL = ["i", "me", "we", "my", "myself", "our", "ourself", "you", "your", "yourself", "he", "him", "hi", "himself", "she", "her", "herself", "it", "itself", "they", "them", "their", "themself", "what", "which", "who", "whom", "thi", "that", "thes", "thos", "am", "are", "wa", "were", "be", "been", "hav", "ha", "had", "do", "did", "a", "an", "the", "and", "but", "if", "or", "because", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "befor", "after", "abov", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "only", "own", "so", "than", "too", "very", "ca", "can", "wo", "will", "just", "should", "now", "th"]


# In[7]:


# Now we need to use the Naive Bayes probability function for our two binary classifications: pos/neg vs true/false
# Let's say we want to find P(+ | sentence) = P(sentence | +)*P(+)/P(sentence)
    # We can ignore the denominator for class prob comparison. Doesn't make a difference ???
# P(sentence | +) = P(token1 | +) * P(token2 | +) * ... 
    # These are the probabilities from the dictionary we created using the nbmodel.txt file
# Technically, we are doing a slight variation since we are adding the prob logs instead of multiplying the probs
# We are adding the logarithms of the probabilities instead of multiplying them because it can result in floating-point underflow.
    # Just taking the log and adding them is what it is right ???

# The following loop is essentially the classifier (for the sentiment analysis)

# creating a list of tuples that includes the two classes of each review (and its file path)
reviewClassificationL = []

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

                # From the following loop, we will be adding the log conditional probabilities of the tokens to get our posterior (nb) probabilities
                pos_post_prob = np.log( pos_prob )
                neg_post_prob = np.log( neg_prob )
                true_post_prob = np.log( true_prob )
                false_post_prob = np.log( false_prob )

                # be iterate through thist list of tokens and calculate it's Bayes prob
                for token in tokensL:
                    # If a token hasn't been seen during training, we ignore it
                    if token in pos_tokens_probD:
                        pos_post_prob += np.log( pos_tokens_probD[token] )
                        neg_post_prob += np.log( neg_tokens_probD[token] )
                        true_post_prob += np.log( true_tokens_probD[token] )
                        false_post_prob += np.log( false_tokens_probD[token] )

                # This is treated as two binary classifications; so now we compare the two label probs for the two classification tasks
                pn_class = ""
                td_class = ""

                if pos_post_prob >= neg_post_prob:
                    pn_class = "positive"
                else:
                    pn_class = "negative"

                if true_post_prob >= false_post_prob:
                    td_class = "truthful"
                else:
                    td_class = "deceptive"

                reviewClassificationL.append( (pn_class, td_class, path) )

fileOut = open("nboutput.txt", "w")

for label_a, label_b, path in reviewClassificationL:
    fileOut.write(( str(label_b) + " " + str(label_a) + " " + path + "\n"))

fileOut.close()





