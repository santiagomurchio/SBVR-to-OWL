from src.sbvr.rule import *
from src.sbvr.fact import *
from owl_configuration import *

class OWLSpecification:
    """
    This class holds the information that was retrieved from the SBVRSpecification. 
    It has a map, where the key is the name of an owl class, and the value is a list of facts and 
    rules where that class participates in.
    """
    _classes = None
    _object_properties = None
    _prefix = None

    def __init__(self, prefix):
        """
        Initializes the instance.
        """
        self._prefix = prefix
        self._classes = []
        self._object_properties = []

    def get_classes(self):
        return self._classes

    def get_object_properties(self):
        return self._object_properties

    def add_class_specification(self, class_specification):
        """
        Adds a class specification.
        """
        self._classes.append(class_specification)


    def add_object_property(self, object_property):
        """
        Adds a new Object Property object to the list.
        """
        self._object_properties.append(object_property)


    def get_class_specification(self, owl_class):
        """
        Returns the OWLClassSpecification if the given class already exists in the
        list, otherwise it returns None.
        """
        for owl_class_specification in self._classes:
            if(owl_class_specification.get_classname().lower() == owl_class.lower()):
                return owl_class_specification
        return None


    def add_fact(self, owl_class, fact):
        """
        Adds a fact to the class specification. If the class specification does not
        yet exists, it creates it.
        """
        owl_class_specification = self.get_class_specification(owl_class)
        if owl_class_specification != None:
            owl_class_specification.add_fact(fact)
        else:
            new_owl_class_specification = OWLSpecification.OWLClassSpecification(owl_class)
            new_owl_class_specification.add_fact(fact)
            self.add_class_specification(new_owl_class_specification)


    def add_rule(self, owl_class, rule):
        """
        Adds a rule to the class specification. If the class specification does not
        yet exists, it creates it.
        """
        owl_class_specification = self.get_class_specification(owl_class)
        if owl_class_specification != None:
            owl_class_specification.add_rule(rule)
        else:
            new_owl_class_specification = OWLSpecification.OWLClassSpecification(owl_class)
            new_owl_class_specification.add_rule(rule)
            self.add_class_specification(new_owl_class_specification)

    
    def build_owl_content(self):
        """
        Builds the owl content to write to the file.
        """
        owl_content = ''

        for owl_object_property in self._object_properties:
            owl_content += '\n' + owl_object_property.get_owl_object_property_definition(self._prefix)

        for owl_class in self._classes:
            owl_content  += '\n' + owl_class.to_owl(self._prefix)

        return owl_content
        


    class OWLClassSpecification:
        """ 
        This class is a holder of a single map, where the key is the owl class name, 
        and the value is a list of facts and rules where that class is involved, as a domain
        noun concept.
        """
        OWL_SIMPLE_CLASS_TEMPLATE = '<owl:Class rdf:about="{prefix}#{classname}" />'
        OWL_CLASS_TEMPLATE = '''
        <owl:Class rdf:about="{prefix}#{classname}">
            {sub_class_clauses}
            {synonym_equivalences}
            {equivalence_class_expressions}
        </owl:Class>
        '''

        OWL_SUB_CLASS_OF_TEMPLATE = '<rdfs:subClassOf rdf:resource="{prefix}#{parent}"/>'

        OWL_EQUIVALENCE_CLASS_TEMPLATE = """
        <owl:equivalentClass>
            <owl:Restriction>
                <owl:onProperty rdf:resource="{prefix}#{property_name}"/>
                {all_values_from}
            </owl:Restriction>
        </owl:equivalentClass>
        """

        OWL_ALL_VALUES_FROM_TEMPLATE = """
        <owl:allValuesFrom>
            <owl:Class>
                <owl:{set_type} rdf:parseType="Collection">
                     {descriptions}
                </owl:{set_type}>
             </owl:Class>
        </owl:allValuesFrom>
        """
        OWL_ALL_VALUES_FROM_SINGLE_CLASS_TEMPLATE = """
        <owl:allValuesFrom rdf:resource="{prefix}#{classname}"/>
        """

        OWL_DESCRIPTION_TEMPLATE = '<rdf:Description rdf:about="{prefix}#{classname}"/>'

        OWL_SYNONYM_EQUIVALENCE_TEMPLATE = """
        <owl:equivalentClass rdf:resource="{prefix}#{classname}"/>
        """

        _classname = None
        _synonym_equivalences = None
        _equivalence_rules = None
        _sub_class_of = None
        _sub_class_of_expressions = None

        def __init__(self, owl_class):
            """
            Initialize the instance.
            """
            self._classname = owl_class
            self._synonym_equivalences = []
            self._equivalence_rules = []
            self._sub_class_of = []
            self._sub_class_of_expressions = []

        def to_owl(self, prefix):
            """
            Prints this owl class specification in owl format (xml)
            """
            sub_class_clauses = self.build_sub_class_clauses(prefix)
            equivalence_class_expressions = self.build_equivalence_class_expressions(prefix)
            # sub_class_of_expressions
            synonym_equivalences = self.build_synonym_equivalences(prefix)
            class_expression = self.OWL_CLASS_TEMPLATE.format(
                prefix = prefix,
                classname = self._classname,
                sub_class_clauses = sub_class_clauses,
                synonym_equivalences = synonym_equivalences,
                equivalence_class_expressions = equivalence_class_expressions)
            return class_expression

        def build_synonym_equivalences(self, prefix):
            equivalences = []
            for equivalence in self._synonym_equivalences:
                equivalences.append(
                    self.OWL_SYNONYM_EQUIVALENCE_TEMPLATE.format(
                        prefix = prefix,
                        classname = equivalence))
            return '\n'.join(equivalences)

        def build_sub_class_clauses(self, prefix):
            clauses = []
            for parent in self._sub_class_of:
                clauses.append(
                    self.OWL_SUB_CLASS_OF_TEMPLATE.format(prefix = prefix, parent = parent))
            return '\n'.join(clauses)

        def build_equivalence_class_expressions(self, prefix):
            equivalences = []
            for equivalence in self._equivalence_rules:
                equivalences.append(
                    self.build_equivalence_class_expression(prefix, equivalence))
            return '\n'.join(equivalences)

        def build_equivalence_class_expression(self, prefix, equivalence):
            if equivalence.get_rule_range().is_noun_concept():
                all_values_from = self.build_all_values_from_noun_concept(
                    prefix, equivalence.get_rule_range().get_range())
            else:
                all_values_from = self.build_all_values_from_collection(
                    prefix, equivalence)
            return self.OWL_EQUIVALENCE_CLASS_TEMPLATE.format(
                prefix = prefix,        
                property_name = equivalence.get_verb(), 
                all_values_from = all_values_from)


        def build_all_values_from_noun_concept(self, prefix, classname):
            return self.OWL_ALL_VALUES_FROM_SINGLE_CLASS_TEMPLATE.format(
                prefix = prefix, classname = classname)


        def build_all_values_from_collection(self, prefix, equivalence):
            set_type = 'intersectionOf' if equivalence.get_rule_range().is_conjunction() else 'unionOf'

            descriptions = []
            for classname in equivalence.get_rule_range().get_range():
                descriptions.append(
                    self.OWL_DESCRIPTION_TEMPLATE.format(prefix = prefix, classname = classname))
            joint_descriptions = '\n'.join(descriptions)
            
            return self.OWL_ALL_VALUES_FROM_TEMPLATE.format(
                prefix = prefix, set_type = set_type, descriptions = joint_descriptions)


        def get_classname(self):
            return self._classname

        def get_synonym_equivalences(self):
            return self._synonym_equivalences

        def get_equivalence_rules(self):
            return self._equivalence_rules

        def get_sub_class_of(self):
            return self._sub_class_of

        def get_sub_class_of_expressions(self):
            return self._sub_class_of_expressions

        def add_synonym_equivalence(self, synonym_equivalence):
            self._synonym_equivalences.append(synonym_equivalence)

        def add_equivalence_rule(self, equivalence_rule):
            self._equivalence_rules.append(equivalence_rule)

        def add_parent_class(self, parent_class):
            self._sub_class_of.append(parent_class)

        def add_parent_class_expression(self, parent_class_expression):
            self._sub_class_of_expressions.append(parent_class_expression)


    class OWLObjectPropertySpecification:
        """
        Holds the specification of an owl object property.
        """
        OWL_OBJECT_PROPERTY_TEMPLATE = '''<owl:ObjectProperty rdf:about="{prefix}#{op_name}">
                                        <rdfs:range rdf:resource="{prefix}#{op_range}"/>
                                        <rdfs:domain rdf:resource="{prefix}#{op_domain}"/>
                                      </owl:ObjectProperty>'''

        _name = None
        _domain = None
        _range = None

        def __init__(self, op_name, op_domain, op_range):
            """
            Initializes the instance with the given values.
            """
            self._name = op_name
            self._domain = op_domain
            self._range = op_range


        def get_owl_object_property_definition(self, prefix):
            """
            Gets the owl (xml) format class definition of this object property.
            """
            return self.OWL_OBJECT_PROPERTY_TEMPLATE.format(prefix = prefix, 
                                                            op_name = self._name,
                                                            op_domain = self._domain,
                                                            op_range = self._range)

