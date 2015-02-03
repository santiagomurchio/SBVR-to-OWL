class Fact:
    """
    This class represents an instance of a SBVR Fact.
    """
    domain_noun_concept = ""
    verb = ""
    fact_range = ""

    def __init__(self, domain_noun_concept, verb, fact_range):
        """
        Constructor for a Fact object
        """
        self.domain_noun_concept = domain_noun_concept
        self.verb = verb
        self.fact_range = fact_range


    class FactRange:
        """
        This class holds the behavior of the range part of the SBVR fact
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

        def get_range(self):
            """
            Returns the range of the rule, which may be a single string, 
            a disjunction or a conjunction.
            """
            if self._range_noun_concept != None:
                return self._range_noun_concept

            if self._disjunction != None:
                return self._disjunction
                
            if self._disjunction != None:
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

