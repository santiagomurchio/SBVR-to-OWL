from rule import *
from fact import *
from owl_configuration import *

class OWLSpecification:
    """
    This class holds the information that was retrieved from the SBVRSpecification. 
    It has a map, where the key is the name of an owl class, and the value is a list of facts and 
    rules where that class participates in.
    """
    _owl_specification = None
    _object_properties = None
    _prefix = None

    def __init__(self, prefix):
        """
        Initializes the instance.
        """
        self._prefix = prefix
        self._owl_specification = []
        self._object_properties = []


    def add_class_specification(self, class_specification):
        """
        Adds a class specification.
        """
        if self._owl_specification == None:
            self._owl_specification = []
        self._owl_specification.append(class_specification)


    def add_object_property(self, op_name, op_domain, op_range):
        """
        Adds a new Object Property object to the list.
        """
        op = OWLSpecification.OWLObjectPropertySpecification(op_name, op_domain, op_range)
        self._object_properties.append(op)


    def get_class_specification(self, owl_class):
        """
        Returns the OWLClassSpecification if the given class already exists in the
        list, otherwise it returns None.
        """
        for owl_class_specification in self._owl_specification:
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

        for owl_specification in self._owl_specification:
            owl_content  += '\n' + owl_specification.get_owl_class_definition(self._prefix)

        return owl_content
        


    class OWLClassSpecification:
        """ 
        This class is a holder of a single map, where the key is the owl class name, 
        and the value is a list of facts and rules where that class is involved, as a domain
        noun concept.
        """
        OWL_CLASS_TEMPLATE = '<owl:Class rdf:about="{prefix}#{classname}" />'
        OWL_CLASS_AND_SUBCLASS_TEMPLATE = '''<owl:Class rdf:about="{prefix}#{classname}" >
                                               {sub_class_clauses}
                                             </owl:Class>'''
        OWL_SUB_CLASS_OF_TEMPLATE = '</rdfs:subClassOf rdf:resource="{prefix}#{parent}"/>'

        _classname = None
        _facts = None
        _rules = None
        
        def __init__(self, owl_class):
            """
            Initialize the instance.
            """
            self._classname = owl_class
            self._facts = []
            self._rules = []


        def get_owl_class_definition(self, prefix):
            """
            Gets the owl (xml) format class definition of this class. It iterates over the 
            facts and the rules where this class is the domain noun and calculates the inheritance rules.
            """
            parents = self.get_parents()
            if len(parents) == 0:
                return self.OWL_CLASS_TEMPLATE.format(prefix = prefix, classname = self._classname)
            else:
                sub_class_of_clauses = []
                for parent in parents:
                    sub_class_of_clauses.append(self.OWL_SUB_CLASS_OF_TEMPLATE.format(prefix = prefix, 
                                                                                      parent = parent))
                sub_class_clauses = '\n'.join(sub_class_of_clauses)
                return self.OWL_CLASS_AND_SUBCLASS_TEMPLATE.format(prefix = prefix,
                                                                   classname = self._classname,
                                                                   sub_class_clauses = sub_class_clauses)


        def get_facts(self):
            """
            Retrieves only the facts for this owl class.
            """
            return _facts

        def add_fact(self, fact):
            """
            Adds a fact to the list.
            """
            self._facts.append(fact)

        def add_rule(self, rule):
            """
            Adds a rule to the list.
            """
            self._rules.append(rule)

        def get_rules(self):
            """
            Retrieves only the rules for this owl class.
            """
            return _rules

        def get_classname(self):
            """
            Returns the class name that this instances corresponds to.
            """
            return self._classname

        def get_parents(self):
            """
            Iterates over the rules to identify the parents of this class.
            """
            parents = []
            for rule in self._rules:
                if OWLConfiguration.OWL_SUB_CLASS_OF_VERB == rule.verb.lower():
                    parents.append(rule.rule_range.get_range())
            return parents
            


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

