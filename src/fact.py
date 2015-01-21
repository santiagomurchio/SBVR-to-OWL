class Fact:
    """
    This class represents an instance of a SBVR Fact.
    """
    domain_noun_concept = ""
    verb = ""
    range_noun_concept = ""

    def __init__(self, domain_noun_concept, verb, range_noun_concept):
        """
        Constructor for a Fact object
        """
        self.domain_noun_concept = domain_noun_concept
        self.verb = verb
        self.range_noun_concept = range_noun_concept


