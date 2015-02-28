from sbvrspecification import SBVRSpecification

class SBVRToOWLTransformer:
    """
    Takes a SBVRSpecification and applies design patterns to build an OWL ontology.
    """
    _sbvr_specification = None
    _output_filename = ""
    _owl_classes = {}

    def __init__(self, sbvr_specification, output_filename):
        """
        Initialize the object with the given SBVR specification and the output file name
        """
        self._sbvr_specification = sbvr_specification
        self._output_filename = output_filename


    def apply_transformations(self):
        """
        Applies the Design pattern to the specification to obtain the owl ontology
        """
        self.read_owl_classes()
        

    def read_owl_classes(self):
        """
        A general concept (a noun concept in SBVR) is mapped to an OWL class. This noun
        concepts that will be transformed to classes are taken from SBVR Rules.
        """
        for rule in self._sbvr_specification.rules:
            self._owl_classes.add(rule.domain_noun_concept)
            self._owl_classes.add(rule.range_noun_concept)

    
    def write_owl_expressions(self):
        """
        Writes the owl expressions to the output file, one expression per line.
        """
        output_file = open_file_for_writing()
        write_owl_classes(output_file)


    def open_file_for_writing(self):
        """
        If the file with the given _filename does not exists, it is created and returned 
        for writing.
        """
        return open(self._filename, 'w')

    
    def write_owl_classes(self, output_file):
        """
        Writes the expressions corresponding to the identified OWL Classes to the output file.
        Example of the expressions:
        OWLClass(Classname)
        """
        classes = []
        classes.append('OWL CLasses\n')
        for owl_class in self._owl_classes:
            classes.append('OWLClass(' + owl_class + ')\n')
        output_file.write(''.join(classes))
