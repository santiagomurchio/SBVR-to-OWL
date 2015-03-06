import unittest
from src.sbvr.sbvrspecification import *
from src.mapping.sbvrtoowl import *
from src.sbvr.fact import *
import xml.etree.ElementTree as ET


class SBVRToOWLTest(unittest.TestCase):
    """
    Test cases for the SBVR To OWL core mappings.
    """

    def test_extract_owl_classes_and_sub_classes_no_classes(self):
        xml = '''<?xml version="1.0"?> 
                 <sbvr-specification>
                 </sbvr-specification>'''

        sbvr_specification = self.get_sbvr_specification_from_string(xml)
        transformer = SBVRToOWL(sbvr_specification, 'output.test', '')
        transformer.transform()
        owl_specification = transformer.get_owl_specification()
        
        self.assert_set_len(0, owl_specification.get_classes())
        self.assert_set_len(0, owl_specification.get_object_properties())        


    def test_transform_with_simple_classes(self):
        term = self.SBVRTermBuilder().build()
        sbvr_specification = SBVRSpecification()
        sbvr_specification.set_terms([term])
        transformer = SBVRToOWL(sbvr_specification, 'output.test', '')
        transformer.transform()
        owl_specification = transformer.get_owl_specification()
        
        self.assert_set_len(1, owl_specification.get_classes())
        self.assert_set_len(0, owl_specification.get_object_properties())        

        owl_class = owl_specification.get_classes()[0]
        self.assertEquals(term.get_name(), owl_class.get_classname())
        self.assertEquals([], owl_class.get_synonym_equivalences())
        self.assertEquals([], owl_class.get_equivalence_rules())
        self.assertEquals([], owl_class.get_sub_class_of())


    def test_transform_with_subclass(self):
        term = self.SBVRTermBuilder().\
               set_name('RegimenAlimentario').\
               set_general_concept('Alimento').\
               build()
        sbvr_specification = SBVRSpecification()
        sbvr_specification.set_terms([term])
        transformer = SBVRToOWL(sbvr_specification, 'output.test', '')
        transformer.transform()
        owl_specification = transformer.get_owl_specification()
        
        self.assert_set_len(1, owl_specification.get_classes())
        self.assert_set_len(0, owl_specification.get_object_properties())        

        owl_class = owl_specification.get_classes()[0]
        self.assertEquals(term.get_name(), owl_class.get_classname())
        self.assertEquals([], owl_class.get_synonym_equivalences())
        self.assertEquals([], owl_class.get_equivalence_rules())
        self.assertEquals([], owl_class.get_equivalence_rules())
        self.assertEquals(['Alimento'], owl_class.get_sub_class_of())


    def test_transform_with_definition(self):
        definition = self.SBVRRuleBuilder().build()
        term = self.SBVRTermBuilder().\
               set_name('RegimenAlimentario').\
               set_general_concept('Alimento').\
               set_definition(definition).\
               build()
        sbvr_specification = SBVRSpecification()
        sbvr_specification.set_terms([term])
        transformer = SBVRToOWL(sbvr_specification, 'output.test', '')
        transformer.transform()
        owl_specification = transformer.get_owl_specification()
        
        self.assert_set_len(1, owl_specification.get_classes())
        self.assert_set_len(0, owl_specification.get_object_properties())        

        owl_class = owl_specification.get_classes()[0]
        self.assertEquals(term.get_name(), owl_class.get_classname())
        self.assertEquals([], owl_class.get_synonym_equivalences())
        self.assertEquals([], owl_class.get_sub_class_of_expressions())
        self.assertEquals(['Alimento'], owl_class.get_sub_class_of())

        self.assert_set_len(1, owl_class.get_equivalence_rules())
        equivalence_rule = owl_class.get_equivalence_rules()[0]
        self.assertEquals(definition, equivalence_rule)
        

    def test_transform_with_necessity(self):
        necessity = self.SBVRRuleBuilder().build()
        term = self.SBVRTermBuilder().\
               set_name('RegimenAlimentario').\
               set_general_concept('Alimento').\
               set_necessity(necessity).\
               build()
        sbvr_specification = SBVRSpecification()
        sbvr_specification.set_terms([term])
        transformer = SBVRToOWL(sbvr_specification, 'output.test', '')
        transformer.transform()
        owl_specification = transformer.get_owl_specification()
        
        self.assert_set_len(1, owl_specification.get_classes())
        self.assert_set_len(0, owl_specification.get_object_properties())        

        owl_class = owl_specification.get_classes()[0]
        self.assertEquals(term.get_name(), owl_class.get_classname())
        self.assertEquals([], owl_class.get_synonym_equivalences())
        self.assertEquals([], owl_class.get_equivalence_rules())
        self.assertEquals(['Alimento'], owl_class.get_sub_class_of())

        self.assert_set_len(1, owl_class.get_sub_class_of_expressions())
        sub_class_of_expression = owl_class.get_sub_class_of_expressions()[0]
        self.assertEquals(necessity, sub_class_of_expression)


    class SBVRTermBuilder():
        """
        Builder for sbvr Terms object
        """
        _name = 'Alimento'
        _definition = None
        _general_concept = None
        _concept_type = 'general concept'
        _synonym = None
        _necessity = None

        def set_name(self, name):
            self._name = name
            return self

        def set_definition(self, definition):
            self._definition = definition
            return self

        def set_general_concept(self, general_concept):
            self._general_concept = general_concept
            return self

        def set_concept_type(self, concept_type):
            self._concept_type = concept_type
            return self

        def set_synonym(self, synonym):
            self._synonym = synonym
            return self

        def set_necessity(self, necessity):
            self._necessity = necessity
            return self

        def build(self):
            term = SBVRTerm()
            term.set_name(self._name)
            term.set_definition(self._definition)
            term.set_general_concept(self._general_concept)
            term.set_concept_type(self._concept_type)
            term.set_synonym(self._synonym)
            term.set_necessity(self._necessity)
            return term
        
    class SBVRQuantificationBuilder:
        """ 
        Builder for quantification objects.
        """
        _quantification_type = 'at-least-N'
        _quantification_value = '1'
        
        def set_quantification_type(self, quantification_type):
            self._quantification_type = quantification_type
            return self
        
        def set_quantification_value(self, quantification_value):
            self._quantification_value = quantification_value
            return self
        
        def build(self):
            quantification = Rule.Quantification()
            quantification.set_quantification_type(self._quantification_type)
            quantification.set_quantification_value(self._quantification_value)
            return quantification


    class SBVRRuleRangeBuilder:
        """ 
        Builder to use when creating rule ranges.
        """
        _range_noun_concept = 'AlimentoOrigenVegetal'
        _disjunction = None
        _conjunction = None

        def set_range_noun_concept(self, noun_concept):
            self._range_noun_concept = noun_concept
            self._conjunction = None
            self._disjunction = None
            return self

        def set_disjunction(self, disjunction):
            self._range_noun_concept = None
            self._conjunction = None
            self._disjunction = disjunction
            return self

        def set_conjunction(self, conjunction):
            self._range_noun_concept = None
            self._disjunction = None
            self._conjunction = conjunction
            return self

        def build(self):
            rule_range = Rule.RuleRange()

            if self._range_noun_concept != None:
                rule_range.set_noun_concept(self._range_noun_concept)

            if self._disjunction != None:
                rule_range.set_disjunction(self.disjunction)

            if self._conjunction != None:
                rule_range.set_conjunction(self.conjunction)

            return self


    class SBVRRuleBuilder:
        """
        Builder for sbvr rules.
        """
        _quantification = None
        _verb = None
        _rule_range = None

        def __init__(self):
            self._quantification = SBVRToOWLTest.SBVRQuantificationBuilder().build()
            self._verb = 'solo_permite_consumo_de'
            self._rule_range = SBVRToOWLTest.SBVRRuleRangeBuilder().build()
            
        def set_quantification(self, quantification):
            self._quantification = quantification
            return self
        
        def set_verb(self, verb):
            self._verb = verb
            return self
            
        def set_rule_range(self, rule_range):
            self._rule_range = rule_range
            return self

        def build(self):
            rule = Rule()
            rule.set_quantification(self._quantification)
            rule.set_verb(self._verb)
            rule.set_rule_range(self._rule_range)
            return rule
        
    # def test_extract_owl_classes_and_sub_classes_with_classes(self):
    #     xml = '''<?xml version="1.0"?> 
    #                <sbvr-specification>
    #                  <sbvr-facts>
    #                  </sbvr-facts>

    #                  <sbvr-rules>

    #                    <sbvr-rule>
    #                       <quantification type="universal">Each</quantification>
    #                       <domain-noun-concept>LactoVegetarianismo</domain-noun-concept>
    #                       <verb>solo permite consumo de</verb>
    #                       <range-noun-concept>Lacteo</range-noun-concept>
    #                     </sbvr-rule>

    #                  </sbvr-rules>
    #              </sbvr-specification>'''

    #     sbvr_specification = self.get_sbvr_specification_from_string(xml)
    #     transformer = SBVRToOWL(sbvr_specification, 'output.test', '')
    #     owl_classes = transformer.extract_owl_classes_and_sub_classes()

    #     self.assert_set_len(2, owl_classes)
    #     expected_classes = set()
    #     expected_classes.add(SBVRToOWL.OWL_CLASS_TEMPLATE.format(classname = 'LactoVegetarianismo',
    #                                                              prefix = ''))
    #     expected_classes.add(SBVRToOWL.OWL_CLASS_TEMPLATE.format(classname = 'Lacteo',
    #                                                              prefix = ''))
    #     self.assert_sets_are_equal(expected_classes, owl_classes)


    # def test_extract_owl_classes_and_sub_classes_disjunction(self):
    #     xml = '''<?xml version="1.0"?> 
    #                <sbvr-specification>
    #                  <sbvr-facts>
    #                  </sbvr-facts>

    #                  <sbvr-rules>

    #                    <sbvr-rule>
    #                       <quantification type="universal">Each</quantification>
    #                       <domain-noun-concept>LactoVegetarianismo</domain-noun-concept>
    #                       <verb>solo permite consumo de</verb>
    #                       <disjunction>
    #                         <range-noun-concept>Lacteo</range-noun-concept>
    #                 	    <range-noun-concept>AlimentoOrigenVegetal</range-noun-concept>
    #                       </disjunction>
    #                     </sbvr-rule>

    #                  </sbvr-rules>
    #              </sbvr-specification>'''

    #     sbvr_specification = self.get_sbvr_specification_from_string(xml)
    #     transformer = None
    #     transformer = SBVRToOWL(sbvr_specification, 'output.test', '')
    #     owl_classes = transformer.extract_owl_classes_and_sub_classes()

    #     self.assert_set_len(3, owl_classes)
    #     expected_classes = set()
    #     expected_classes.add(SBVRToOWL.OWL_CLASS_TEMPLATE.format(classname = 'LactoVegetarianismo',
    #                                                              prefix = ''))
    #     expected_classes.add(SBVRToOWL.OWL_CLASS_TEMPLATE.format(classname = 'Lacteo',
    #                                                              prefix = ''))
    #     expected_classes.add(SBVRToOWL.OWL_CLASS_TEMPLATE.format(classname = 'AlimentoOrigenVegetal',
    #                                                              prefix = ''))
    #     self.assert_sets_are_equal(expected_classes, owl_classes)


    # def test_extract_owl_classes_and_sub_classes_conjunction(self):
    #     xml = '''<?xml version="1.0"?> 
    #                <sbvr-specification>
    #                  <sbvr-facts>
    #                  </sbvr-facts>

    #                  <sbvr-rules>

    #                    <sbvr-rule>
    #                       <quantification type="universal">Each</quantification>
    #                       <domain-noun-concept>LactoVegetarianismo</domain-noun-concept>
    #                       <verb>solo permite consumo de</verb>
    #                       <conjunction>
    #                         <range-noun-concept>Lacteo</range-noun-concept>
    #                 	    <range-noun-concept>AlimentoOrigenVegetal</range-noun-concept>
    #                       </conjunction>
    #                     </sbvr-rule>

    #                  </sbvr-rules>
    #              </sbvr-specification>'''

    #     sbvr_specification = self.get_sbvr_specification_from_string(xml)
    #     transformer = None
    #     transformer = SBVRToOWL(sbvr_specification, 'output.test', '')
    #     owl_classes = transformer.extract_owl_classes_and_sub_classes()

    #     self.assert_set_len(3, owl_classes)
    #     expected_classes = set()
    #     expected_classes.add(SBVRToOWL.OWL_CLASS_TEMPLATE.format(classname = 'LactoVegetarianismo',
    #                                                              prefix = ''))
    #     expected_classes.add(SBVRToOWL.OWL_CLASS_TEMPLATE.format(classname = 'Lacteo',
    #                                                              prefix = ''))
    #     expected_classes.add(SBVRToOWL.OWL_CLASS_TEMPLATE.format(classname = 'AlimentoOrigenVegetal',
    #                                                              prefix = ''))
    #     self.assert_sets_are_equal(expected_classes, owl_classes)


    # def test_extract_owl_classes_and_sub_classes_subclass_of(self):
    #     xml = '''<?xml version="1.0"?> 
    #                <sbvr-specification>
    #                  <sbvr-facts>
    #                  </sbvr-facts>

    #                  <sbvr-rules>

    #                    <sbvr-rule>
    #                       <domain-noun-concept>AlimentoCrudo</domain-noun-concept>
    #                       <verb>es un</verb>
    #                       <range-noun-concept>Alimento</range-noun-concept>
    #                     </sbvr-rule>

    #                  </sbvr-rules>
    #              </sbvr-specification>'''

    #     sbvr_specification = self.get_sbvr_specification_from_string(xml)
    #     transformer = None
    #     transformer = SBVRToOWL(sbvr_specification, 'output.test', '')
    #     owl_classes = transformer.extract_owl_classes_and_sub_classes()

    #     self.assert_set_len(1, owl_classes)
    #     expected_classes = set()
    #     owl_class = SBVRToOWL.OWL_CLASS_AND_SUBCLASS_TEMPLATE.format(parent = 'Alimento',
    #                                                                  classname = 'AlimentoCrudo',
    #                                                                  prefix = '')
    #     expected_classes.add(owl_class)
    #     self.assert_sets_are_equal(expected_classes, owl_classes)


    # def test_extract_single_object_properties(self):
    #     xml = '''<?xml version="1.0"?> 
    #                <sbvr-specification>
    #                  <sbvr-facts>
    #                  </sbvr-facts>

    #                  <sbvr-rules>

    #                    <sbvr-rule>
    #                       <quantification type="universal">Each</quantification>
    #                       <domain-noun-concept>LactoVegetarianismo</domain-noun-concept>
    #                       <verb>solo permite consumo de</verb>
    #                       <range-noun-concept>Lacteo</range-noun-concept>
    #                     </sbvr-rule>

    #                  </sbvr-rules>
    #              </sbvr-specification>'''

    #     sbvr_specification = self.get_sbvr_specification_from_string(xml)
    #     transformer = None
    #     transformer = SBVRToOWL(sbvr_specification, 'output.test', '')
    #     owl_object_properties = transformer.extract_owl_object_properties()

    #     self.assert_set_len(1, owl_object_properties)
    #     expected_object_properties = set()
    #     owl_op = SBVRToOWL.OWL_OBJECT_PROPERTY_TEMPLATE.format(op_name = 'solo permite consumo de',
    #                                                            op_domain = 'LactoVegetarianismo',
    #                                                            op_range = 'Lacteo', 
    #                                                            prefix = '')
    #     expected_object_properties.add(owl_op)
    #     self.assert_sets_are_equal(expected_object_properties, owl_object_properties)



    # def test_extract_single_object_properties(self):
    #     xml = '''<?xml version="1.0"?> 
    #                <sbvr-specification>
    #                  <sbvr-facts>
    #                  </sbvr-facts>

    #                  <sbvr-rules>

    #                    <sbvr-rule>
    #                       <quantification type="universal">Each</quantification>
    #                       <domain-noun-concept>LactoVegetarianismo</domain-noun-concept>
    #                       <verb>solo permite consumo de</verb>
    #                       <disjunction>
    #                         <range-noun-concept>Lacteo</range-noun-concept>
    #                         <range-noun-concept>AlimentoOrigenVegetal</range-noun-concept>
    #                       </disjunction>
    #                     </sbvr-rule>


    #                  </sbvr-rules>
    #              </sbvr-specification>'''

    #     sbvr_specification = self.get_sbvr_specification_from_string(xml)
    #     transformer = None
    #     transformer = SBVRToOWL(sbvr_specification, 'output.test', '')
    #     owl_object_properties = transformer.extract_owl_object_properties()

    #     self.assert_set_len(1, owl_object_properties)
    #     expected_object_properties = set()
    #     owl_op = SBVRToOWL.OWL_OBJECT_PROPERTY_TEMPLATE.format(op_name = 'solo permite consumo de',
    #                                                            op_domain = 'LactoVegetarianismo',
    #                                                            op_range = 'Lacteo', 
    #                                                            prefix = '')
    #     expected_object_properties.add(owl_op)
    #     self.assert_sets_are_equal(expected_object_properties, owl_object_properties)


    def get_sbvr_specification_from_string(self, xml_string):
        """ 
        Builds the sbvr specification object from the xml string.
        """
        root = ET.fromstring(xml_string)
        sbvr_specification = SBVRSpecification()
        sbvr_specification.from_xml(root)
        return sbvr_specification


    def assert_set_len(self, expected_len, test_set):
        """
        Assert that the set is not None and it has the given size.
        """
        self.assertNotEquals(None, test_set)
        self.assertEquals(expected_len, len(test_set))

    def assert_sets_are_equal(self, expected_set, actual_set):
        """
        Asserts that both sets have the exact same elements, making the string comparison as 
        both lower cases.
        """
        self.assertEquals(len(expected_set), len(actual_set))
        for owl_class in expected_set:
            self.assertTrue(owl_class in actual_set)

if __name__ == '__main__':
    unittest.main()
