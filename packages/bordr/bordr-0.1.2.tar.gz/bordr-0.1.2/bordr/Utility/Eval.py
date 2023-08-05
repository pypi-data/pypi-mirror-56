# -*- coding: utf-8 -*-
from .Utils import getWordTag, readDictionary


def computeAccuracy(goldStandardCorpus, taggedCorpus):
    tagged = open(taggedCorpus, "r", encoding="utf-8-sig").read().split()
    goldStandard = open(goldStandardCorpus, "r", encoding="utf-8-sig").read().split()
    if len(tagged) != len(goldStandard):
        msg = f"The numbers of word tokens in {goldStandardCorpus} and {taggedCorpus} are not equal!"
        return 0, msg

    numwords = 0
    count = 0
    for i in range(len(tagged)):
        numwords += 1
        word1, tag1 = getWordTag(tagged[i])
        word2, tag2 = getWordTag(goldStandard[i])
        if word1 != word2 and word1 != "''" and word2 != "''":
            msg = f"Words are not the same in gold standard and tagged corpora, at the index {i}"
            return 0, msg

        if tag1.lower() == tag2.lower():
            count += 1

    return count * 100.0 / numwords


def computeAccuracies(fullDictFile, goldStandardCorpus, taggedCorpus):
    """
    Return known-word accuracy, unknown-word accuracy and the overall accuracy  
    """
    tagged = open(taggedCorpus, "r", encoding="utf-8-sig").read().split()
    goldStandard = open(goldStandardCorpus, "r", encoding="utf-8-sig").read().split()
    if len(tagged) != len(goldStandard):
        return f"The numbers of word tokens in {goldStandardCorpus} and {taggedCorpus} are not equal!"

    fullDICT = readDictionary(fullDictFile)

    numwords = count = 0
    countKN = countUNKN = 0
    countCorrectKN = countCorrectUNKN = 0

    for i in range(len(tagged)):
        numwords += 1
        word1, tag1 = getWordTag(tagged[i])
        word2, tag2 = getWordTag(goldStandard[i])
        if word1 != word2 and word1 != "''" and word2 != "''":
            return (
                "Words are not the same in gold standard and tagged corpora, at the index "
                + str(i)
            )

        if tag1.lower() == tag2.lower():
            count += 1

        if word1 in fullDICT:
            countKN += 1
            if tag1.lower() == tag2.lower():
                countCorrectKN += 1
        else:
            countUNKN += 1
            if tag1.lower() == tag2.lower():
                countCorrectUNKN += 1

    if countUNKN == 0:
        return countCorrectKN * 100.0 / countKN, 0.0, count * 100.0 / numwords
    else:
        return (
            countCorrectKN * 100.0 / countKN,
            countCorrectUNKN * 100.0 / countUNKN,
            count * 100.0 / numwords,
        )


def evaluate(goldStandardCorpus, taggedCorpus, fullDictFile=None):
    if fullDictFile:
        return computeAccuracies(fullDictFile, goldStandardCorpus, taggedCorpus)
    else:
        return computeAccuracy(goldStandardCorpus, taggedCorpus)
