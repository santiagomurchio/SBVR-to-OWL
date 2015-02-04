class SBVRToOWL:
    """
    This class represents the core of the transformation process.
    """
    OWL_CLASS_TEMPLATE = '<owl:Class rdf:about="{classname}" />'
    OWL_CLASS_AND_SUBCLASS_TEMPLATE = '''<owl:Class rdf:about="{classname}" >
                                           </rdfs:subClassOf rdf:resource="{parent}"/>
                                         </owl:Class>'''

    _sbvr_specification = None
    _output_file = None

    def __init__(self, sbvr_specification, filename):
        """
        Constructor.
        """
        self._sbvr_specification = sbvr_specification
        self._output_file = open(filename, 'w')

    def transform(self):
        """
        Core method that handles the transformation. It writes to the output file as
        OWL expressions.
        """
        owl_classes = self.extract_owl_classes_and_sub_classes()
        owl_object_properties = self.extract_owl_object_properties()

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
        owl_class = self.OWL_CLASS_AND_SUBCLASS_TEMPLATE.format(classname = child_class, parent = parent_class)
        owl_classes.add(owl_class)

    def extract_owl_classes(self, owl_classes, rule):
        """
        Extracts the plain classes from a SBVR rule
        """
        owl_classes.add(self.OWL_CLASS_TEMPLATE.format(classname = rule.domain_noun_concept))
        
        if rule.rule_range.is_noun_concept():
            owl_classes.add(self.OWL_CLASS_TEMPLATE.format(classname = rule.rule_range.get_range()))
        else:
            for rule_range in rule.rule_range.get_range():
                owl_classes.add(self.OWL_CLASS_TEMPLATE.format(classname = rule_range))

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
            
        
