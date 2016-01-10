from fact import *
from rule import *
from logicaloperation import *
from sbvrterm import *
from binary_verb_concept_rule import *
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

    def set_terms(self, terms):
        """
        This method should be used only by unit tests.
        """
        self._terms = terms

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

        sbvr_term.set_definition(self.parse_logical_operation(term.find('sbvr-term-definition')))

        if sbvr_term.is_concept_type():
            sbvr_term.set_necessity(self.parse_logical_operation(term.find('sbvr-term-necessity')))

        if sbvr_term.is_verb_concept():
            sbvr_term.set_necessity(self.parse_sbvr_verb_necessity(term.find('sbvr-term-necessity')))

        return sbvr_term

    def parse_logical_operation(self, necessity_as_xml):
        """
        Tries to parse a necessity, which can be a single logic operator or a conjunction, or disjunction.
        """
        if necessity_as_xml == None or len(list(necessity_as_xml)) == 0:
            return None
        
        # first try conjunction
        conjunction = necessity_as_xml.find('sbvr-conjunction')
        if conjunction is not None:
            logical_operation = LogicalOperation('conjunction')
            logical_operation.set_logical_operators(self.parse_logical_operators(conjunction))
            return logical_operation
        
        # if not, try disjunction
        disjunction = necessity_as_xml.find('sbvr-disjunction')
        if disjunction is not None:
            logical_operation = LogicalOperation('disjunction')
            logical_operation.set_logical_operators(self.parse_logical_operators(disjunction))
            return logical_operation

        # it must be a single concept
        logical_operation = LogicalOperation('single-clause')
        logical_operation.set_logical_operators(self.parse_logical_operators(necessity_as_xml))
        return logical_operation

    def parse_logical_operators(self, logical_operation):
        """
        Parse the operators_as_xml found on a logical operation object
        """
        operators = []
        operators_as_xml = logical_operation.findall('sbvr-logical-operator')
        for operator in operators_as_xml:
            operators.append(self.parse_sbvr_rule(operator))
        return operators 


    def parse_sbvr_rule(self, xml_rule):
        """
        Creates a rule from the given xml rule condition.
        """
        if xml_rule == None or len(list(xml_rule)) == 0:
            return None

        quantification = Rule.Quantification()
        quantification.set_quantification_type(xml_rule.find('sbvr-quantification').get('type'))
        quantification.set_quantification_value(xml_rule.find('sbvr-quantification').text)

        rule_range = self.parse_sbvr_rule_range(xml_rule)

        rule = Rule()
        rule.set_verb(xml_rule.find('sbvr-verb').text)
        rule.set_quantification(quantification)
        rule.set_rule_range(rule_range)
        return rule
       
    def parse_sbvr_rule_range(self, term):
        """
        Parses and returns the range part of a necessity condition.
        """
        # first try conjunction
        conjunction = term.find('sbvr-conjunction')
        if conjunction is not None:
            concepts = []
            for sbvr_concept in conjunction.findall('sbvr-concept'):
                concepts.append(sbvr_concept.text)

            rule_range = Rule.RuleRange()
            rule_range.set_conjunction(concepts)
            return rule_range

        # if not, try disjunction
        disjunction = term.find('sbvr-disjunction')
        if disjunction is not None:
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

    def parse_sbvr_verb_necessity(self, xml_necessity):
        """
        Parses the necessity for a verb concept type.
        """
        if xml_necessity.text is None:
            return None

        position_to_role = dict()
        xml_roles = xml_necessity.findall('sbvr-role')
        
        # first build the map to know the right position
        positions = []
        for xml_role in xml_roles:
            position = int(xml_role.get('position'))
            positions.append(position)
            position_to_role[position] = xml_role

        # iterate over the map using the correct position
        binary_verb_concept_rule = BinaryVerbConceptRule()
        for position in sorted(positions):
            binary_verb_concept_rule.add_role(
                BinaryVerbConceptRule.BinaryVerbConceptRuleRole(position_to_role[position]))

        return binary_verb_concept_rule
