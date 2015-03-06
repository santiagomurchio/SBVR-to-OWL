from src.utils.listutils import *

class Rule:
    """
    This class represents an instance of a SBVR Rule.
    """
    SUB_CLASS_OF_VERB = 'es un'

    quantification = None
    domain_noun_concept = ""
    verb = ""
    rule_range = None

    # def __init__(self, quantification_type, quantification_text, domain_noun_concept, verb, rule_range):
    #     """
    #     Constructor for a Fact object
    #     """
    #     self.quantification = Rule.Quantification(quantification_type, quantification_text)
    #     self.domain_noun_concept = domain_noun_concept
    #     self.verb = verb
    #     self.rule_range = rule_range

    def is_sub_class_of_rule(self):
        """ 
        Returns True if this rule is a statement of a subclass relationship.
        """
        return self.verb.lower() == self.SUB_CLASS_OF_VERB.lower()

    def get_verb(self):
        return self.verb

    def set_verb(self, verb):
        self.verb = verb

    def get_quantification(self):
        return self.quantification

    def get_rule_range(self):
        return self.rule_range

    def set_quantification(self, quantification):
        self.quantification = quantification

    def set_verb(self, verb):
        self.verb = verb

    def set_rule_range(self, rule_range):
        self.rule_range = rule_range

    def __eq__(self, another_rule):
        if self.verb != another_rule.verb:
            return False

        another_quantification = another_rule.quantification
        if self.quantification != None:
            if another_quantification == None:
                return False
            else:
                if self.quantification != another_quantification:
                    return False

        another_rule_range = another_rule.rule_range
        if self.rule_range != None:
            if another_rule_range == None:
                return False
            else:
                if self.rule_range != another_rule_range:
                    return False

        return True

    class Quantification:
        """ 
        This class holds the quantification element of the SBVR rules. It has a type, which can be, 
        for example, 'Universal', and a text, which can be, in this case 'Each'.
        """
        
        quantification_type = None
        quantification_value = ''
        
        # def __init__(self, quantification_type, quantification_value):
        #     """
        #     Constructor
        #     """
        #     self.quantification_type = quantification_type
        #     self.quantification_value = quantification_value
        
        def get_type(self):
            return self.quantification_type

        def get_value(self):
            return self.quantification_value
        
        def set_quantification_type(self, quantification_type):
            self.quantification_type = quantification_type

        def set_quantification_value(self, quantification_value):
            self.quantification_value = quantification_value

        def __eq__(self, another_quantification):
            if another_quantification == None:
                return False

            if self._quantification_type != None:
                if another_quantification._quantification_type == None:
                    return False
                else:
                    if self._quantification_type != another_quantification._quantification_type:
                        return False

            if self._quantification_text != None:
                if another_quantification._quantification_text == None:
                    return False
                else:
                    if self._quantification_text != another_quantification._quantification_text:
                        return False

            return True
        


    class RuleRange:
        """
        This class holds the behavior of the range part of the SBVR rule
        """
        # range can be different things
        _range_noun_concept = None
        _disjunction = None
        _conjunction = None

        def __init__(self):
            """
            Default constructor.
            """
            self._range_noun_concept = None
            self._disjunction = None
            self._conjunction = None

        def __eq__(self, another_range):
            
            if self.is_disjunction():
                if another_range.is_disjunction:
                    return ListUtils.same_elements_ignore_order(
                        self._disjunction, another_range._disjunction)
                else:
                    return False

            if self.is_conjunction():
                if another_range.is_conjunction:
                    return ListUtils.same_elements_ignore_order(
                        self._conjunction, another_range._conjunction)
                else:
                    return False

            if self.is_noun_concept():
                if another_range.is_noun_concept():
                    return self._range_noun_concept == another_range._range_noun_concept
                else:
                    return False
        

        def get_range(self):
            """
            Returns the range of the rule, which may be a single string, 
            a disjunction or a conjunction.
            """
            if self._range_noun_concept != None:
                return self._range_noun_concept

            if self._disjunction != None:
                return self._disjunction
                
            if self._conjunction != None:
                return self._conjunction

        def is_disjunction(self):
            """
            Returns True if this RuleRange is a disjunction of noun concepts.
            """
            return self._disjunction != None


        def is_conjunction(self):
            """
            Returns True if this RuleRange is a conjunction of noun concepts.
            """
            return self._conjunction != None


        def is_noun_concept(self):
            """
            Returns True if this RuleRange is a single noun concept.
            """
            return self._range_noun_concept != None


        def set_disjunction(self, disjunction):
            """
            Sets the elements of the disjunctions and sets to None all
            other elements.
            """
            self._disjunction = disjunction
            self._conjunction = None
            self._range_noun_concept = None


        def set_noun_concept(self, noun_concept):
            """
            Sets the noun concept and sets to None all other elements.
            """
            self._disjunction = None
            self._conjunction = None
            self._range_noun_concept = noun_concept


        def set_conjunction(self, conjunction):
            """
            Creates a RuleRange object with the given noun concepts as a disjunction.
            """
            self._disjunction = None
            self._range_noun_concept = None
            self._conjunction = conjunction

