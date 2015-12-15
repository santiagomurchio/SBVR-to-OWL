class LogicalOperation:
    """
    This class holds an logical operation, which can be a conjunction, a disjunction, or a single clause.
    """
    _type = None
    _logical_operators = None

    def __init__(self, logical_operation_type):
        self._type = logical_operation_type
        self._logical_operators = []

    def add_logical_operator(self, operator):
        self._logical_operators.append(operator)        

    def get_logical_operators(self):
        return self._logical_operators

    def set_logical_operators(self, logical_operators):
        self._logical_operators = logical_operators
    
    def is_conjunction(self):
        """
        Returns true if this logical operation is a conjunction.
        """
        return 'conjunction' == self._type

    def is_disjunction(self):
        """
        Returns true if this logical operation is a disjunction.
        """
        return 'disjunction' == self._type

    def is_single_clause(self):
        """ 
        Returns true if this term is a single logical clause.
        """
        return not self.is_disjunction() and not self.is_conjunction()
