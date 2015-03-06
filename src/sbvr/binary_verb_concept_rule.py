class BinaryVerbConceptRule:
    """
    Class to hold the rule for necessities of binary verb concept roles.
    """

    _roles = None

    def __init__(self):
        self._roles = []

    def add_role(self, role):
        """
        Adds the given role to the array.
        """
        self._roles.append(role)

    def get_roles(self):
        return self._roles
