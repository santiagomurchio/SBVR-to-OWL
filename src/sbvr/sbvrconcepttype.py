from enum import Enum

class SBVRConceptType(Enum):
    """
    Enumeration to hold the different types of SBVR concepts.
    """
    GENERAL_CONCEPT = "general concept"
    
    GeneralConcept = 1
    
    def from_string(self, concept_type):
        """
        Returns the concept type that corresponds to this string, or error if it is not found.
        """
        if concept_type.lower() == GENERALCONCEPT:
            return Generalconcept
