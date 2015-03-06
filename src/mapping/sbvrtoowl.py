from src.owl.owl_file import *
from src.owl.owl_specification import *

class SBVRToOWL(OWLFile):
    """
    This class represents the core of the transformation process.
    """
    OWL_OBJECT_PROPERTY_TEMPLATE = '''<owl:ObjectProperty rdf:about="{prefix}#{op_name}">
                                        <rdfs:range rdf:resource="{prefix}#{op_range}"/>
                                        <rdfs:domain rdf:resource="{prefix}#{op_domain}"/>
                                      </owl:ObjectProperty>'''
    
    OWL_ONTOLOGY = '''<owl:Ontology rdf:about="{prefix}"/>'''

    _sbvr_specification = None
    _owl_specification = None
    _output_file = None
    _prefix = None

    def __init__(self, sbvr_specification, filename, prefix):
        """
        Constructor.
        """
        self._sbvr_specification = sbvr_specification
        self._output_file = open(filename, 'w')
        self._prefix = prefix

    def get_owl_specification(self):
        return self._owl_specification

    def transform(self):
        """
        Core method that handles the transformation. It writes to the output file as
        OWL expressions.
        """
        self.build_owl_specification()
        self.write_ontology_to_owl_file()


    def build_owl_specification(self):
        """
        Iterates over the SBVR specification and builds the corresponding owl_specification.
        """
        self._owl_specification = OWLSpecification(self._prefix)
        for sbvr_term in self._sbvr_specification.get_terms():
            if sbvr_term.is_concept_type():
                owl_class = self.build_owl_class_specification(sbvr_term)
                self._owl_specification.add_class_specification(owl_class)
            else:
                owl_object_property = self.build_owl_object_property(sbvr_term)
                self._owl_specification.add_object_property(owl_object_property)

    def build_owl_class_specification(self, sbvr_term):
        owl_class = OWLSpecification.OWLClassSpecification(sbvr_term.get_name())

        if sbvr_term.get_synonym() != None:
            owl_class.add_synonym_equivalence(sbvr_term.get_synonym())

        if sbvr_term.get_necessity() != None:
            owl_class.add_parent_class_expression(sbvr_term.get_necessity())

        if sbvr_term.get_general_concept() != None:
            owl_class.add_parent_class(sbvr_term.get_general_concept())

        if sbvr_term.get_definition() != None:
            owl_class.add_equivalence_rule(sbvr_term.get_definition())

        return owl_class

    def build_owl_object_property(self, sbvr_term):
        owl_object_property = OWLSpecification.OWLObjectPropertySpecification(
            sbvr_term.get_name(),
            sbvr_term.get_necessity().get_roles()[0],
            sbvr_term.get_necessity().get_roles()[1])
        return owl_object_property

    def write_ontology_to_owl_file(self):
        """ 
        Writes the owl specification to the given file.
        """
        owl_content = self.build_owl_content()

        # header
        self._output_file.write(self.XML_VERSION + '\n')
        
        # doctype
        self._output_file.write(self.OWL_DOCTYPE + '\n')
        
        # rdf namespaces
        rdf_content = self.OWL_RDF_NAMESPACES.format(owl_file_content = owl_content, 
                                                     prefix = self._prefix)
        self._output_file.write(rdf_content + '\n')
        

    def build_owl_content(self):
        """
        Builds the owl content to write to the file.
        """
        owl_content = self._owl_specification.build_owl_content()
        owl_ontology = self.OWL_ONTOLOGY.format(prefix = self._prefix)
        file_content = '\n\n' + owl_ontology + '\n\n' + owl_content + '\n\n'
        return file_content


    def extract_owl_classes_and_sub_classes(self):
        """
        Handles the transformation of the General Concepts, which are 'noun concepts that
        classifies things on the basis of their common properties'.
        """
        # A set so we can avoid duplicates
        owl_classes = set()
        for rule in self._sbvr_specification.rules:
            owl_classes.add(OWLClass(rule))
        return owl_classes


    def extract_owl_object_properties(self):
        """ 
        Extracts the object properties from the sbvr specification
        """
        # for rule in self._sbvr_specification.rules:
        #     self.extract_owl_object_property_from_rule(rule)


    def extract_owl_object_property_from_rule(self, rule):
        """
        Works on a SBVR rule to extract an object property. If the SBVR rule is
        a description of a subclass, this method does not extract it.
        """
        if rule.is_sub_class_of_rule():
            return
            
        # for now we assume that the rule is only a noun concept
        op_range = rule.rule_range.get_range()
        op_domain = rule.domain_noun_concept
        op_name = rule.verb
        self._owl_specification.add_object_property(op_name, op_domain, op_range)
        

