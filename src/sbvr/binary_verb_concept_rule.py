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

    def relates_concept_and_literal(self):
        for role in self._roles:
            if role.get_text() is None and role.get_xsd_type() is not None:
                return True
        return False

    def relates_concepts(self):
        return not self.relates_concept_and_literal()

    class BinaryVerbConceptRuleRole:
        """
        This class holds a role that is a part of a binary verb concept rule.
        """
        _text = None
        _xsd_type = None

        def __init__(self, role_as_xml):
            self._text = role_as_xml.text
            self._xsd_type = role_as_xml.get('xsd-type')

        def get_text(self):
            return self._text

        def get_xsd_type(self):
            return self._xsd_type
