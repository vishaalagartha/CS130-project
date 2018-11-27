import os
import nltk
from nltk.tree import ParentedTree, Tree
from nltk.parse import stanford
import nltk.data
import nltk.draw
import re
import sys
import stanford_parser_env as spe

os.environ['STANFORD_PARSER'] = spe.STANFORD_PARSER
os.environ['STANFORD_MODELS'] = spe.STANFORD_MODEL

class SVO(object):
    """
    Class Methods to Extract Subject Verb Object Tuples from a Sentence
    """
    def __init__(self):
        """
        Initialize the SVO Methods
        """
        self.noun_types = ["NN", "NNP", "NNPS","NNS","PRP"]
        self.verb_types = ["VB","VBD","VBG","VBN", "VBP", "VBZ"]
        self.adjective_types = ["JJ","JJR","JJS"]
        self.pred_verb_phrase_siblings = None
        self.parser = stanford.StanfordParser()
        self.sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

    def get_attributes(self,node,parent_node, parent_node_siblings):
        """
        returns the Attributes for a Node
        """

    def get_subject(self,sub_tree):
        """
        Returns the Subject and all attributes for a subject, sub_tree is a Noun Phrase
        """
        sub_nodes = []
        sub_nodes = sub_tree.subtrees()
        sub_nodes = [each for each in sub_nodes if each.pos()]
        subject = None

        for each in sub_nodes:

            if each.label() in self.noun_types:
                subject = each.leaves()
                break

        return {'subject':subject}

    def get_object(self,sub_tree):
        """
        Returns an Object with all attributes of an object
        """
        Object = None
        for each_tree in sub_tree:
            if each_tree.label() in ["NP","PP"]:
                sub_nodes = each_tree.subtrees()
                sub_nodes = [each for each in sub_nodes if each.pos()]

                for each in sub_nodes:
                    if each.label() in self.noun_types:
                        Object = each.leaves()
                        break
                break
            else:
                sub_nodes = each_tree.subtrees()
                sub_nodes = [each for each in sub_nodes if each.pos()]
                for each in sub_nodes:
                    if each.label() in self.adjective_types:
                        Object = each.leaves()
                        break
                # Get first noun in the tree
        self.pred_verb_phrase_siblings = None
        return {'object':Object}

    def get_predicate(self, sub_tree):
        """
        Returns the Verb along with its attributes, Also returns a Verb Phrase
        """

        sub_nodes = []
        sub_nodes = sub_tree.subtrees()
        sub_nodes = [each for each in sub_nodes if each.pos()]
        predicate = None
        pred_verb_phrase_siblings = []
        sub_tree  = ParentedTree.convert(sub_tree)
        for each in sub_nodes:
            if each.label() in self.verb_types:
                sub_tree = each
                predicate = each.leaves()

        #get all predicate_verb_phrase_siblings to be able to get the object
        sub_tree  = ParentedTree.convert(sub_tree)
        if predicate:
             pred_verb_phrase_siblings = self.tree_root.subtrees()
             pred_verb_phrase_siblings = [each for each in pred_verb_phrase_siblings if each.label() in ["NP","PP","ADJP","ADVP"]]
             self.pred_verb_phrase_siblings = pred_verb_phrase_siblings

        return {'predicate':predicate}

    def process_parse_tree(self,parse_tree):
        """
        Returns the Subject-Verb-Object Representation of a Parse Tree.
        Can Vary depending on number of 'sub-sentences' in a Parse Tree
        """
        self.tree_root = parse_tree
        # Step 1 - Extract all the parse trees that start with 'S'
        output_list = []
        output_dict ={}
        # i=0

        for subtree in parse_tree[0].subtrees():
            subject =None
            predicate = None
            Object = None
            if subtree.label() in ["S", "SQ", "SBAR", "SBARQ", "SINV", "FRAG"]:
                children_list = subtree
                children_values = [each_child.label() for each_child in children_list]
                children_dict = dict(zip(children_values,children_list))


                # Extract Subject, Verb-Phrase, Objects from Sentence sub-trees
                if children_dict.get("NP") is not None:
                    subject = self.get_subject(children_dict["NP"])

                if children_dict.get("VP") is not None:
                    predicate = self.get_predicate(children_dict["VP"])
                    Object = self.get_object(children_dict["VP"])

                try:
                    if subject['subject'] and predicate['predicate'] and Object['object']:
                        output_dict['subject'] = subject['subject']
                        output_dict['predicate'] = predicate['predicate']
                        output_dict['object'] = Object['object']
                        output_list.append(output_dict)
                except Exception as e:
                        print(e)
                        continue
        return output_list


    def traverse(self,t):
        try:
            t.label()
        except AttributeError:
            print(t)
        else:
            # Now we know that t.node is defined
            print('(', t.label())
            for child in t:
                self.traverse(child)
            print(')')

    def sentence_split(self,text):
        """
        returns the Parse Tree of a Sample
        """
        sentences = self.sent_detector.tokenize(text)
        return sentences


    def get_parse_tree(self,sentence):
        """
        returns the Parse Tree of a Sample
        """
        parse_tree = self.parser.raw_parse(sentence)

        return parse_tree


if __name__=="__main__":
    svo = SVO()
    # sentence = "Andreas loves soccer. He is also very good at it. Barack Obama likes the legislation"
    #sentence = 'This is the problem with the max contracts.'
    sentence = 'I like eggs and bacon and turkey but not chicken'
                # 'It means that a guy like ' + \
                # 'John Wall or Kyle Lowry are worth the same as Lebron or KD. ' + \
                # "Which is kind of nuts. I feel like it'd help league parity if " + \
                # "they uncapped contracts, and just told players you can get paid "+ \
                # "99.9% of your teams cap, but enjoy being on the shittiest team " + \
                # "in basketball. Then you'd get guys to spread out and go for " + \
                # "their money while others decide they'll take a more moderate " + \
                # 'amount to have a good team.'
    # sentences =  svo.sentence_split(sentence)

    sentences = re.split(" and | but | , | ; ", sentence)
    val = []
    for sent in sentences:
        root_tree = svo.get_parse_tree(sent)
        val.append(svo.process_parse_tree(next(root_tree)))

    subject = ""
    predicate = ""
    obj = ""
    org_phrase = ""

    list_phrase = []
    for ind, j in enumerate(val):
        new_phrase = ""
        if j:
            i = j[0]
            subject = i["subject"][0]
            predicate = i["predicate"][0]
            obj = i["object"][0]
            list_phrase.append(sentences[ind])
            org_phrase = sentences[ind]
        else:
            new_phrase = org_phrase.replace(obj, sentences[ind])
            list_phrase.append(new_phrase)
    print(list_phrase)
    print()
