class SBVRTerm:
    """
    This class holds an sbvr entry of the sbvr glossary.
    """
    _name = None
    _definition = None
    _general_concept = None
    _concept_type = None
    _synonym = None
    _necessity = None

    def __init__(self):
        self._name = ''
        self._definition = None
        self._general_concept = ''
        self._concept_type = ''
        self._synonym = ''
        self._necessity = None
    
    def set_name(self, name):
        self._name = name
        
    def set_general_concept(self, general_concept):
        self._general_concept = general_concept
            
    def set_definition(self, definition):
        self._definition = definition
            
    def set_concept_type(self, concept_type):
        self._concept_type = concept_type
                
    def set_synonym(self, synonym):
        self._synonym = synonym
                    
    def set_necessity(self, necessity):
        self._necessity = necessity

    def get_name(self):
        return self._name

    def get_general_concept(self):
        return self._general_concept

    def get_definition(self):
        return self._definition

    def get_concept_type(self):
        return self._concept_type

    def get_synonym(self):
        return self._synonym
    
    def get_necessity(self):
        return self._necessity

