from rule import *
from fact import *
import xml.etree.ElementTree as ET

class SBVRSpecification:
    """
    This class holds a list of SBVR facts and SBVR rules that form an SBVR specification
    """

    facts = None
    rules = None
    
    def __init__(self):
        """
        Constructor
        """
        self.facts = []
        self.rules = []

    def from_xml(self, root):
        """
        Parses the give file and gets the elements from it
        """
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
                self.facts.append(self.parse_fact(raw_fact))

    def parse_fact(self, raw_fact):
        """
        Iterates over xml facts representations and creates facts objects
        """
        domain_noun_concept = raw_fact.find('domain-noun-concept').text
        verb = raw_fact.find('verb').text
        fact_range = self.parse_rule_range(raw_fact)
        return Fact(domain_noun_concept, verb, fact_range)


    def parse_rules(self, root):
        """
        Iterates over xml facts representations and creates rules objects
        """
        sbvr_rules = root.findall('sbvr-rules')
        for sbvr_rule in sbvr_rules:
            raw_rules = sbvr_rule.findall('sbvr-rule')
            for raw_rule in raw_rules:
                self.rules.append(self.parse_rule(raw_rule))


    def parse_rule(self, raw_rule):
        """
        Receives an xml element and return the parsed sbvr rule
        """
        quantification_text = ''
        quantification_type = ''
        
        quantification = raw_rule.find('quantification')
        if(quantification != None):
            quantification_text = quantification.text
            quantification_type = quantification.get('type')

        domain_noun_concept = raw_rule.find('domain-noun-concept').text
        verb = raw_rule.find('verb').text
        rule_range = self.parse_rule_range(raw_rule)
        
        return Rule(quantification_type, quantification_text, domain_noun_concept, verb, rule_range)

    def parse_rule_range(self, raw_rule):
        """
        Parses the rule range, which can have a disjunction, a single noun concept
        or a conjunction.
        """
        # if disjunction has noun concepts, the rule is a disjunction
        raw_disjunction = raw_rule.find('disjunction')
        if raw_disjunction != None:
            raw_noun_concepts = raw_disjunction.findall('range-noun-concept')
            disjunction_nouns = []
            for noun_concept in raw_noun_concepts:
                disjunction_nouns.append(noun_concept.text)
            rule_range = Rule.RuleRange()
            rule_range.set_disjunction(disjunction_nouns)
            return rule_range

        # if conjunction has noun concepts, the rule is a conjunction
        raw_conjunction = raw_rule.find('conjunction')
        if raw_conjunction != None:
            raw_noun_concepts = raw_conjunction.findall('range-noun-concept')
            conjunction_nouns = []
            for noun_concept in raw_noun_concepts:
                conjunction_nouns.append(noun_concept.text)
            rule_range = Rule.RuleRange()
            rule_range.set_conjunction(conjunction_nouns)
            return rule_range

        # it must have only one noun concept then
        noun_concept = raw_rule.find('range-noun-concept').text
        rule_range = Rule.RuleRange()
        rule_range.set_noun_concept(noun_concept)
        return rule_range
                
            

    def parse_rules_old(self, root):
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
