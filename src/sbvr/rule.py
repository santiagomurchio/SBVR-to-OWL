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
        Returns true if this rule is a statement of a subclass relationship.
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
            Returns true if this RuleRange is a disjunction of noun concepts.
            """
            return self._disjunction != None


        def is_conjunction(self):
            """
            Returns true if this RuleRange is a conjunction of noun concepts.
            """
            return self._conjunction != None


        def is_noun_concept(self):
            """
            Returns true if this RuleRange is a single noun concept.
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

