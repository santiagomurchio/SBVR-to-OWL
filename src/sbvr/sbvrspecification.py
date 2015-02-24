from rule import *
from fact import *
from sbvrterm import *
import xml.etree.ElementTree as ET

class SBVRSpecification:
    """
    This class holds a list of SBVR facts and SBVR rules that form an SBVR specification
    """

    _terms = None
    
    def __init__(self):
        """
        Constructor
        """
        self._terms = []

    def get_terms(self):
        return self._terms

    def from_xml_file(self, filename):
        """
        Parses the xml file given as a parameter.
        """
        root = ET.parse(filename).getroot()
        self.from_xml(root)

    def from_xml(self, root):
        """
        Parses the given file and gets the elements from it
        """
        sbvr_terms = root.findall('sbvr-term')
        for term in sbvr_terms:
            self._terms.append(self.parse_sbvr_term(term))

    def parse_sbvr_term(self, term):
        """
        Creates an SBVRTerm object from the xml representation.
        """
        sbvr_term = SBVRTerm()
        sbvr_term.set_name(term.find('sbvr-term-name').text)
        sbvr_term.set_general_concept(term.find('sbvr-term-general-concept').text)
        sbvr_term.set_concept_type(term.find('sbvr-term-concept-type').text)
        sbvr_term.set_synonym(term.find('sbvr-term-synonym').text)
        
        sbvr_term.set_necessity(self.parse_sbvr_necessity(term))
        
        return sbvr_term

    def parse_sbvr_necessity(self, term):
        """
        Creates a rule from the necessity condition of the given term.
        """
        xml_necessity = term.find('sbvr-term-necessity')

        if xml_necessity == None or len(list(xml_necessity)) == 0:
            return None

        quantification = Rule.Quantification()
        quantification.set_quantification_type(xml_necessity.find('sbvr-quantification').get('type'))
        quantification.set_quantification_value(xml_necessity.find('sbvr-quantification').text)

        necessity_range = self.parse_sbvr_necessity_range(xml_necessity)

        necessity = Rule()
        necessity.set_verb(xml_necessity.find('sbvr-verb').text)
        necessity.set_quantification(quantification)
        necessity.set_rule_range(necessity_range)
        return necessity
       
    def parse_sbvr_necessity_range(self, term):
        """
        Parses and returns the range part of a necessity condition.
        """
        # first try conjunction
        conjunction = term.find('sbvr-conjunction')
        if conjunction != None:
            concepts = []
            for sbvr_concept in conjunction.findall('sbvr-concept'):
                concepts.append(sbvr_concept.text)

            rule_range = Rule.RuleRange()
            rule_range.set_conjunction(concepts)
            return rule_range

        # if not, try disjunction
        disjunction = term.find('sbvr-disjunction')
        if disjunction != None:
            concepts = []
            for sbvr_concept in disjunction.findall('sbvr-concept'):
                concepts.append(sbvr_concept.text)

            rule_range = Rule.RuleRange()
            rule_range.set_disjunction(concepts)
            return rule_range

        # it must be a single concept
        rule_range = Rule.RuleRange()
        rule_range.set_noun_concept(term.find('sbvr-concept').text)
        return rule_range
