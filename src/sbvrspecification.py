from fact import Fact
from rule import Rule
import xml.etree.ElementTree as ET

class SBVRSpecification:
    """
    This class holds a list of SBVR facts and SBVR rules that form an SBVR specification
    """

    facts = []
    rules = []

    def from_xml_file(self):
        """
        Parses the give file and gets the elements from it
        """
        root = self.parse_input_file().getroot()
        self.parse_facts(root)
        self.parse_rules(root)

    def parse_facts(self, root):
        """
        Iterates over xml facts representations and creates facts objects
        """
        sbvr_facts = root.findall('sbvr-facts')
        for sbvr_fact in sbvr_facts:
            raw_facts = sbvr_fact.findall('sbvr-fact')
            for raw_fact in raw_facts:
                domain_noun_concept = raw_fact.find('domain-noun-concept')
                verb = raw_fact.find('verb').text
                range_noun_concept = raw_fact.find('range-noun-concept')
                self.facts.append(Fact(domain_noun_concept, verb, range_noun_concept))

    def parse_rules(self, root):
        """
        Iterates over xml facts representations and creates facts objects
        """
        sbvr_rules = root.findall('sbvr-rules')
        for sbvr_rule in sbvr_rules:
            raw_rules = sbvr_rule.findall('sbvr-rule')
            for raw_rule in raw_rules:
                quantification = raw_rule.find('quantification').text
                if(quantification == None):
                    quantification = ''
                domain_noun_concept = raw_rule.find('domain-noun-concept').text
                verb = raw_rule.find('verb').text
                range_noun_concept = raw_rule.find('range-noun-concept').text
                self.rules.append(Rule(quantification, domain_noun_concept, verb, range_noun_concept))

    def parse_input_file(self):
        """ 
        Parse the xml file indicated by the user and returns its tree object.
        """
        filename = raw_input("Enter SBVR specification filename (default: rules.xml): ")
        if filename == "":
            filename = "rules.xml"
        return ET.parse(filename)
