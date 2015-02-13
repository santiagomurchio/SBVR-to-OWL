from owl_file import *

class SBVRToOWL(OWLFile):
    """
    This class represents the core of the transformation process.
    """
    OWL_CLASS_TEMPLATE = '<owl:Class rdf:about="{prefix}#{classname}" />'
    OWL_CLASS_AND_SUBCLASS_TEMPLATE = '''<owl:Class rdf:about="{prefix}#{classname}" >
                                               </rdfs:subClassOf rdf:resource="{prefix}#{parent}"/>
                                             </owl:Class>'''
    OWL_OBJECT_PROPERTY_TEMPLATE = '''<owl:ObjectProperty rdf:about="{prefix}#{op_name}">
                                        <rdfs:range rdf:resource="{prefix}#{op_range}"/>
                                        <rdfs:domain rdf:resource="{prefix}#{op_domain}"/>
                                      </owl:ObjectProperty>'''
    
    OWL_ONTOLOGY = '''<owl:Ontology rdf:about="{prefix}"/>'''

    _sbvr_specification = None
    _output_file = None
    _prefix = None

    def __init__(self, sbvr_specification, filename, prefix):
        """
        Constructor.
        """
        self._sbvr_specification = sbvr_specification
        self._output_file = open(filename, 'w')
        self._prefix = prefix


    def transform(self):
        """
        Core method that handles the transformation. It writes to the output file as
        OWL expressions.
        """
        owl_classes = self.extract_owl_classes_and_sub_classes()
        owl_object_properties = self.extract_owl_object_properties()

        self.write_ontology_to_owl_file(owl_classes, owl_object_properties)

    def write_ontology_to_owl_file(self, owl_classes, owl_object_properties):
        """ 
        Writes the owl specification to the given file.
        """
        owl_content = self.build_owl_content(owl_classes, owl_object_properties)
        
        # header
        self._output_file.write(self.XML_VERSION + '\n')
        
        # doctype
        self._output_file.write(self.OWL_DOCTYPE + '\n')
        
        # rdf namespaces
        rdf_content = self.OWL_RDF_NAMESPACES.format(owl_file_content = owl_content, 
                                                     prefix = self._prefix)
        self._output_file.write(rdf_content + '\n')
        

    def build_owl_content(self, owl_classes, owl_object_properties):
        """
        Builds the owl content to write to the file.
        """
        classes = '\n'.join(owl_classes)
        object_properties = '\n'.join(owl_object_properties)
        owl_ontology = OWL_ONTOLOGY.format(prefix = self._prefix)

        file_content =   + '\n\n' + owl_ontology + '\n\n' + object_properties + '\n\n' + classes + '\n\n'
        return file_content
        

    def extract_owl_classes_and_sub_classes(self):
        """
        Handles the transformation of the General Concepts, which are 'noun concepts that
        classifies things on the basis of their common properties'.
        """
        # A set so we can avoid duplicates
        owl_classes = set()
        for rule in self._sbvr_specification.rules:
            if rule.is_sub_class_of_rule():
                self.extract_owl_sub_class(owl_classes, rule)
            else:
                self.extract_owl_classes(owl_classes, rule)

        return owl_classes

    def extract_owl_sub_class(self, owl_classes, rule):
        """
        Extracts a sub-class-of relationship.
        """
        # for now assume that the rule is a noun concept only 
        # and no conjunction nor disjunction
        child_class = rule.domain_noun_concept
        parent_class = rule.rule_range.get_range() 
        owl_class = self.OWL_CLASS_AND_SUBCLASS_TEMPLATE.format(classname = child_class, 
                                                                parent = parent_class,
                                                                prefix = self._prefix)
        owl_classes.add(owl_class)

    def extract_owl_classes(self, owl_classes, rule):
        """
        Extracts the plain classes from a SBVR rule
        """
        owl_classes.add(self.OWL_CLASS_TEMPLATE.format(classname = rule.domain_noun_concept,
                                                       prefix = self._prefix))
        
        if rule.rule_range.is_noun_concept():
            owl_classes.add(self.OWL_CLASS_TEMPLATE.format(classname = rule.rule_range.get_range(), 
                                                           prefix = self._prefix))
        else:
            for rule_range in rule.rule_range.get_range():
                owl_classes.add(self.OWL_CLASS_TEMPLATE.format(classname = rule_range,
                                                               prefix = self._prefix))

    def extract_owl_object_properties(self):
        """ 
        Extracts the object properties from the sbvr specification
        """
        owl_object_properties = set()
        for rule in self._sbvr_specification.rules:
            self.extract_owl_object_property_from_rule(owl_object_properties, rule)

        return owl_object_properties

    def extract_owl_object_property_from_rule(self, owl_object_properties, rule):
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
        owl_op = self.OWL_OBJECT_PROPERTY_TEMPLATE.format(op_name = op_name,
                                                          op_domain = op_domain,
                                                          op_range = op_range,
                                                          prefix = self._prefix)
        owl_object_properties.add(owl_op)
        

    class OWLClass:
        """
        Holds the characteristics of an OWL class, like it's parent, and also the equivalences.
        """
        OWL_CLASS_TEMPLATE = '<owl:Class rdf:about="{prefix}#{classname}" />'
        OWL_CLASS_AND_SUBCLASS_TEMPLATE = '''<owl:Class rdf:about="{prefix}#{classname}" >
                                               </rdfs:subClassOf rdf:resource="{prefix}#{parent}"/>
                                             </owl:Class>'''
        _owl_class = None
        _owl_parent_class = None
        _owl_equivalence = None


        def __init__(self, owl_class, owl_parent_class, owl_equivalence):
            """
            Initialize the instance
            """
            self._owl_class = owl_class
            self._owl_parent_class = owl_parent_class
            self._owl_equivalence = owl_equivalence

        def to_owl(self):
            """
            Writes the content of this instance to owl (xml) format.
            """
            if self._owl_parent_class != None:
                return self.OWL_CLASS_AND_SUBCLASS_TEMPLATE.format(prefix = self.prefix,
                                                                   classname = self._owl_class,
                                                                   parent = self._owl_parent_class)
            else:
                return self.OWL_CLASS_TEMPLATE.format(prefix = self.prefix,
                                                      classname = self._owl_class)
                
