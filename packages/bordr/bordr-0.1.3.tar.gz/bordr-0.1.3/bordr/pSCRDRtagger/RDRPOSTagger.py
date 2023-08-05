# -*- coding: utf-8 -*-

from multiprocessing import Pool

from ..InitialTagger.InitialTagger4Bo import initializeCorpus, initializeSentence
from ..SCRDRlearner.Object import FWObject
from ..SCRDRlearner.SCRDRTree import SCRDRTree
from ..SCRDRlearner.SCRDRTreeLearner import SCRDRTreeLearner
from ..Utility.Config import NUMBER_OF_PROCESSES, THRESHOLD
from ..Utility.Utils import getWordTag, getRawText, readDictionary
from ..Utility.LexiconCreator import createLexicon


def unwrap_self_RDRPOSTagger(arg, **kwarg):
    return RDRPOSTagger.tagRawSentence(*arg, **kwarg)


class RDRPOSTagger(SCRDRTree):
    """
    RDRPOSTagger for a particular language
    """

    def __init__(self):
        super().__init__()
        self.root = None

    def tagRawSentence(self, DICT, rawLine):
        """

        :param DICT:
        :param rawLine:
        :return:
        """
        line = initializeSentence(DICT, rawLine)
        sen = []
        wordTags = line.split()
        for i in range(len(wordTags)):
            fwObject = FWObject.getFWObject(wordTags, i)
            word, tag = getWordTag(wordTags[i])
            node = self.findFiredNode(fwObject)
            if node.depth > 0:
                sen.append(word + "/" + node.conclusion)
            else:  # Fired at root, return initialized tag
                sen.append(word + "/" + tag)
        return " ".join(sen)

    def tagRawCorpus(self, DICT, rawCorpusPath):
        lines = open(rawCorpusPath, "r", encoding="utf-8-sig").readlines()
        # Change the value of NUMBER_OF_PROCESSES to obtain faster tagging process!
        pool = Pool(processes=NUMBER_OF_PROCESSES)
        taggedLines = pool.map(
            unwrap_self_RDRPOSTagger,
            zip([self] * len(lines), [DICT] * len(lines), lines),
        )
        outW = open(rawCorpusPath + ".TAGGED", "w", encoding="utf-8-sig")
        for line in taggedLines:
            outW.write(line + "\n")
        outW.close()
        return "Output file: " + rawCorpusPath + ".TAGGED"


def rdr(to_process, mode=None, model=None, lexicon=None, string=False, verbose=False):
    """
    :param to_process: either a string(!!!"tag" only!!!) or a filename. if string, be sure to set arg "string" to True
    :param mode: either train or tag
    :param model: !!!"tag" only!!! .RDR file to be used as model to POS tag to_process
    :param lexicon: !!!"tag" only!!! .DICT file to be used as model to POS tag to_process
    :param string: !!!"tag" only!!! considers "to_process" as a string to be tagged if True, considers it a filename otherwise.
    :param verbose: return the messages from training and tagging if True, not otherwise.
    """
    if not mode or mode not in ["train", "tag"]:
        raise SyntaxError("mode should either be train or tag.")

    if mode == "train":
        log = []
        log.append("\n====== Start ======")
        log.append(
            "\nGenerate from the gold standard training corpus a lexicon "
            + to_process
            + ".DICT"
        )
        log.append(createLexicon(to_process, "full"))
        log.append(createLexicon(to_process, "short"))
        log.append(
            "\nExtract from the gold standard training corpus a raw text corpus "
            + to_process
            + ".RAW"
        )
        getRawText(to_process, to_process + ".RAW")
        log.append(
            "\nPerform initially POS tagging on the raw text corpus, to generate "
            + to_process
            + ".INIT"
        )
        DICT = readDictionary(to_process + ".sDict")
        initializeCorpus(DICT, to_process + ".RAW", to_process + ".INIT")
        log.append(
            "\nLearn a tree model of rules for POS tagging from %s and %s"
            % (to_process, to_process + ".INIT")
        )
        rdrTree = SCRDRTreeLearner(THRESHOLD[0], THRESHOLD[1])
        log.extend(rdrTree.learnRDRTree(to_process + ".INIT", to_process, verbose=verbose))
        log.append("\nWrite the learned tree model to file " + to_process + ".RDR")
        rdrTree.writeToFile(to_process + ".RDR")
        log.append("\nDone!")
        return "".join(log) if verbose else 0

    if mode == "tag":
        log = []
        r = RDRPOSTagger()
        log.append("\n=> Read a POS tagging model from " + model)
        r.constructSCRDRtreeFromRDRfile(model)
        log.append("\n=> Read a lexicon from " + lexicon)
        DICT = readDictionary(lexicon)
        log.append("\n=> Perform POS tagging on " + to_process)
        if string:
            r.tagRawSentence(DICT, to_process)
        else:
            r.tagRawCorpus(DICT, to_process)
        return "".join(log) if verbose else 0
