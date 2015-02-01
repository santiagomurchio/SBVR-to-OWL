import unittest
from src.sbvrspecification import *
from src.sbvrtoowl import *
from src.fact import *
import xml.etree.ElementTree as ET


class SBVRToOWLTest(unittest.TestCase):
    """
    Test cases for the SBVR To OWL core mappings.
    """

    def test_extract_owl_classes_and_sub_classes_no_classes(self):
        xml = '''<?xml version="1.0"?> 
                   <sbvr-specification>
                     <sbvr-facts>
                     </sbvr-facts>

                     <sbvr-rules>
                     </sbvr-rules>
                 </sbvr-specification>'''

        sbvr_specification = self.get_sbvr_specification_from_string(xml)
        transformer = SBVRToOWL(sbvr_specification, 'output.test')
        owl_classes = transformer.extract_owl_classes_and_sub_classes()
        
        self.assert_set_len(0, owl_classes)
        

    def test_extract_owl_classes_and_sub_classes_with_classes(self):
        xml = '''<?xml version="1.0"?> 
                   <sbvr-specification>
                     <sbvr-facts>
                     </sbvr-facts>

                     <sbvr-rules>
                       <sbvr-rule>
                         <quantification type="universal">Each</quantification>
                         <domain-noun-concept>AlimentoCrudo</domain-noun-concept>
                         <verb>es un</verb>
                         <range-noun-concept>Alimento</range-noun-concept>
                       </sbvr-rule>

                     </sbvr-rules>
                 </sbvr-specification>'''

        sbvr_specification = self.get_sbvr_specification_from_string(xml)
        transformer = None
        transformer = SBVRToOWL(sbvr_specification, 'output.test')
        owl_classes = transformer.extract_owl_classes_and_sub_classes()

        self.assert_set_len(2, owl_classes)
        expected_classes = set()
        expected_classes.add(SBVRToOWL.OWL_CLASS_TEMPLATE.format(classname = 'AlimentoCrudo'))
        expected_classes.add(SBVRToOWL.OWL_CLASS_TEMPLATE.format(classname = 'Alimento'))
        self.assert_sets_are_equal(expected_classes, owl_classes)


    def test_extract_owl_classes_and_sub_classes_disjunction(self):
        xml = '''<?xml version="1.0"?> 
                   <sbvr-specification>
                     <sbvr-facts>
                     </sbvr-facts>

                     <sbvr-rules>

                       <sbvr-rule>
                          <quantification type="universal">Each</quantification>
                          <domain-noun-concept>LactoVegetarianismo</domain-noun-concept>
                          <verb>solo permite consumo de</verb>
                          <disjunction>
                            <range-noun-concept>Lacteo</range-noun-concept>
                    	    <range-noun-concept>AlimentoOrigenVegetal</range-noun-concept>
                          </disjunction>
                        </sbvr-rule>

                     </sbvr-rules>
                 </sbvr-specification>'''

        sbvr_specification = self.get_sbvr_specification_from_string(xml)
        transformer = None
        transformer = SBVRToOWL(sbvr_specification, 'output.test')
        owl_classes = transformer.extract_owl_classes_and_sub_classes()

        self.assert_set_len(3, owl_classes)
        expected_classes = set()
        expected_classes.add(SBVRToOWL.OWL_CLASS_TEMPLATE.format(classname = 'LactoVegetarianismo'))
        expected_classes.add(SBVRToOWL.OWL_CLASS_TEMPLATE.format(classname = 'Lacteo'))
        expected_classes.add(SBVRToOWL.OWL_CLASS_TEMPLATE.format(classname = 'AlimentoOrigenVegetal'))
        self.assert_sets_are_equal(expected_classes, owl_classes)


    def test_extract_owl_classes_and_sub_classes_conjunction(self):
        xml = '''<?xml version="1.0"?> 
                   <sbvr-specification>
                     <sbvr-facts>
                     </sbvr-facts>

                     <sbvr-rules>

                       <sbvr-rule>
                          <quantification type="universal">Each</quantification>
                          <domain-noun-concept>LactoVegetarianismo</domain-noun-concept>
                          <verb>solo permite consumo de</verb>
                          <conjunction>
                            <range-noun-concept>Lacteo</range-noun-concept>
                    	    <range-noun-concept>AlimentoOrigenVegetal</range-noun-concept>
                          </conjunction>
                        </sbvr-rule>

                     </sbvr-rules>
                 </sbvr-specification>'''

        sbvr_specification = self.get_sbvr_specification_from_string(xml)
        transformer = None
        transformer = SBVRToOWL(sbvr_specification, 'output.test')
        owl_classes = transformer.extract_owl_classes_and_sub_classes()

        self.assert_set_len(3, owl_classes)
        expected_classes = set()
        expected_classes.add(SBVRToOWL.OWL_CLASS_TEMPLATE.format(classname = 'LactoVegetarianismo'))
        expected_classes.add(SBVRToOWL.OWL_CLASS_TEMPLATE.format(classname = 'Lacteo'))
        expected_classes.add(SBVRToOWL.OWL_CLASS_TEMPLATE.format(classname = 'AlimentoOrigenVegetal'))
        self.assert_sets_are_equal(expected_classes, owl_classes)


    def test_extract_owl_classes_and_sub_classes_subclass_of(self):
        xml = '''<?xml version="1.0"?> 
                   <sbvr-specification>
                     <sbvr-facts>
                     </sbvr-facts>

                     <sbvr-rules>

                       <sbvr-rule>
                          <domain-noun-concept>AlimentoCrudo</domain-noun-concept>
                          <verb>es un</verb>
                          <range-noun-concept>Alimento</range-noun-concept>
                        </sbvr-rule>

                     </sbvr-rules>
                 </sbvr-specification>'''

        sbvr_specification = self.get_sbvr_specification_from_string(xml)
        transformer = None
        transformer = SBVRToOWL(sbvr_specification, 'output.test')
        owl_classes = transformer.extract_owl_classes_and_sub_classes()

        self.assert_set_len(3, owl_classes)
        expected_classes = set()
        owl_class = SBVRToOWL.OWL_CLASS_AND_SUBCLASS_TEMPLATE.format(parent = 'Alimento',
                                                                     classname = 'LactoVegetarianismo')
        expected_classes.add(owl_class)
        self.assert_sets_are_equal(expected_classes, owl_classes)


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
