# decoding script

import sys
import numpy as np



# converting back from text to dictionary
hmmmodel = open("hmmmodel.txt", "r")

total_lines = int( hmmmodel.readline().split()[-2] )

posD = {}
vocabD = {}
start_probD = {}
end_probD = {}
transition_probD = {}
emission_probD = {}
open_cl_posL = []

for line in hmmmodel:
    if "POS" and "appears" in line.split():
        pos = line.split()[2][1:-1]
        count = int(line.split()[4])
        posD[pos] = count


    elif "open-class" in line.split():
        for i, word in enumerate(line.split()):
            if i > 3:
                open_cl_posL.append(word[1:-2])
    
    elif "vocabulary" in line.split():
        token = line.split()[3][1:-1]
        count = int(line.split()[-2])
        vocabD[token] = count

    elif "initial" in line.split():
        pos = line.split()[-3][1:-1]
        prob = line.split()[-1]
        start_probD[pos] = float(prob)

    elif "end" in line.split():
        pos = line.split()[-3][1:-1]
        prob = float(line.split()[-1])
        end_probD[pos] = prob

    elif "transition" in line.split():
        prev_pos = line.split()[4][1:-1]
        cur_pos = line.split()[6][1:-1]
        prob = float(line.split()[-1])
        if prev_pos not in transition_probD:
            transition_probD[prev_pos] = {cur_pos: prob}
        else:
            transition_probD[prev_pos][cur_pos] = prob

    elif "emission" in line.split():
        pos = line.split()[5][1:-1]
        token = line.split()[8][1:-1]
        prob = float(line.split()[-1])
        if token not in emission_probD:
            emission_probD[token] = {pos: prob}
        else:
            emission_probD[token][pos] = prob

hmmmodel.close()




# path = "/Users/alaintamazian/DocumentsAT/CSCI544/HWs/HW2_Hidden_Markov_Models/hmm-training-data/it_isdt_dev_raw.txt"
path = sys.argv[1]
# argv[0] is the name of the python file
# argv[1] argument is the directory path of the test data



fileIn = open(path, "r")

fileOut = open("hmmoutput.txt", "w")

# viterbi decoding

# tagsL will have the following structure: [ {series: [ pos1, pos2, … ], prob: integer }, … ]
tagsL = []
tagsL_new = []
# redundant ?


for sentence in fileIn:

    tagsL = []
    tagsL_new = []

    for i, token in enumerate(sentence.split()):
        if token in vocabD:

            if i == 0:
                for pos in emission_probD[token]:


                    emiss_prob = emission_probD[token][pos]

                    # start and end are treated as states, so their probs are transition probs
                    # So we should apply smoothing for it ???
                    # try different types ???

                    if pos not in start_probD:
                        start_prob = 0.001
                    else:
                        start_prob = start_probD[pos] + 0.001

                    newProb = np.log(start_prob) + np.log(emiss_prob)

                    tagsL.append({"series": [(token, pos, newProb)], "prob": newProb})

            else:
                for pos in emission_probD[token]:

                    emiss_prob = emission_probD[token][pos]

                    newCombos = []

                    for sequence_infoD in tagsL:

                        sequenceL = sequence_infoD["series"]
                        prev_prob = sequence_infoD["prob"]
                        prev_pos = sequenceL[-1][1]

                        # doing smoothing for transition probs
                        if (prev_pos not in transition_probD) or (pos not in transition_probD[prev_pos]):
                            trans_prob = 0.001
                        else:
                            trans_prob = transition_probD[prev_pos][pos] + 0.001

                        # make calcuation logarithmic
                        newProb = prev_prob + np.log(trans_prob) + np.log(emiss_prob)

                        newCombos.append(newProb)

                    # backtracking and identifying the best previous POS based on the current POS (prob path)
                    best_idx = np.argmax(newCombos)
                    best_prob = newCombos[best_idx]

                    sequenceL_best = tagsL[best_idx]["series"].copy()

                    sequenceL_best.append((token, pos, best_prob))

                    tagsL_new.append({"series": sequenceL_best, "prob": best_prob})

                    sequenceL_best = []

                tagsL = tagsL_new.copy()
                tagsL_new = []

                # can make a lot more efficient
                if i == (len(sentence.split()) - 1):

                    for i, sequenceD in enumerate(tagsL):
                        last_pos = sequenceD["series"][-1][1]

                        # do we just skip if our training data doesn't have a specific emission ???
                        # We do this first to avoid unnecessary computation
                        if (token not in emission_probD) or (last_pos not in emission_probD[token]):
                            # emission = 0; so we skip it
                            continue
                        else:
                            emiss_prob = emission_probD[token][last_pos]
                        #                     print(emiss_prob)

                        # start and end are treated as states, so their probs are transition probs
                        if last_pos not in end_probD:
                            end_prob = 0.001
                        else:
                            end_prob = end_probD[last_pos] + 0.001

                        newProb = np.log(end_prob) + np.log(emiss_prob)

                        oldProb = sequenceD["prob"]
                        lastProb = oldProb + newProb

                        tagsL[i]["prob"] = lastProb

        # if we see an known word in the test data, we ignore all emission probs
        # implement open class tranistion probs weighting
        else:

            if i == 0:
                for pos in open_cl_posL:
                    if pos not in start_probD:
                        start_prob = 0.001
                    else:
                        start_prob = start_probD[pos] + 0.001

                    newProb = np.log(start_prob)

                    tagsL.append({"series": [(token, pos, newProb)], "prob": newProb})

            else:
                for pos in open_cl_posL:

                    newCombos = []

                    for sequence_infoD in tagsL:

                        sequenceL = sequence_infoD["series"]
                        prev_prob = sequence_infoD["prob"]
                        prev_pos = sequenceL[-1][1]

                        # doing smoothing for transition probs
                        if (prev_pos not in transition_probD) or (pos not in transition_probD[prev_pos]):
                            trans_prob = 0.001
                        else:
                            trans_prob = transition_probD[prev_pos][pos] + 0.001

                        # make calcuation logarithmic
                        newProb = prev_prob + np.log(trans_prob)

                        newCombos.append(newProb)

                    # backtracking and identifying the best previous POS based on the current POS (prob path)
                    best_idx = np.argmax(newCombos)
                    best_prob = newCombos[best_idx]

                    sequenceL_best = tagsL[best_idx]["series"].copy()

                    sequenceL_best.append((token, pos, best_prob))

                    tagsL_new.append({"series": sequenceL_best, "prob": best_prob})

                    sequenceL_best = []

                tagsL = tagsL_new.copy()
                tagsL_new = []

                # can  make a lot more efficient
                if i == (len(sentence.split()) - 1):

                    for i, sequenceD in enumerate(tagsL):
                        last_pos = sequenceD["series"][-1][1]

                        # start and end are treated as states, so their probs are transition probs
                        if last_pos not in end_probD:
                            end_prob = 0.001
                        else:
                            end_prob = end_probD[last_pos] + 0.001

                        newProb = end_prob

                        oldProb = sequenceD["prob"]
                        lastProb = oldProb + np.log(newProb)

                        tagsL[i]["prob"] = lastProb

    best_seq_idx = np.argmax([sequenceD["prob"] for sequenceD in tagsL])
    # print()
    for word, tag, prob in (tagsL[best_seq_idx]["series"]):

        if (word, tag, prob) == tagsL[best_seq_idx]["series"][-1]:
            fileOut.write((word + "/" + tag))
        else:
            fileOut.write((word + "/" + tag + " "))
            fileOut.write(" ")
            # find better alternative ???
            # Is it possible for the condition to ==, but not actually be at -1
    fileOut.write("\n")


# make sure my encoding is correct

fileOut.close()
fileIn.close()


