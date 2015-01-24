import unittest
from src.sbvrspecification import SBVRSpecification
import xml.etree.ElementTree as ET


class SBVRSpecificationTest(unittest.TestCase):
    """
    Test cases for the SBVR specification parser
    """

    def test_parse_rules_empty_string(self):
        xml = '''<?xml version="1.0"?> 
                   <sbvr-specification>
                     <sbvr-facts>
                     </sbvr-facts>

                     <sbvr-rules>
                     </sbvr-rules>
                 </sbvr-specification>'''

        root = ET.fromstring(xml)
        sbvr_specification = SBVRSpecification()
        sbvr_specification.from_xml(root)

        self.assertNotEqual(None, sbvr_specification.rules)
        self.assertNotEqual(None, sbvr_specification.facts)
        self.assertEqual(0, len(sbvr_specification.rules))
        self.assertEqual(0, len(sbvr_specification.facts))
        

    def test_parse_rules_simple_rule(self):
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

        root = ET.fromstring(xml)
        sbvr_specification = SBVRSpecification()
        sbvr_specification.from_xml(root)

        self.assertNotEqual(None, sbvr_specification.facts)
        self.assertEqual(0, len(sbvr_specification.facts))
        
        self.assertNotEqual(None, sbvr_specification.rules)
        self.assertEqual(1, len(sbvr_specification.rules))
        
        rule = sbvr_specification.rules[0]
        self.assertEquals('Each'.lower(), rule.quantification.quantification_text.lower())
        self.assertEquals('Universal'.lower(), rule.quantification.quantification_type.lower())
        self.assertEquals('AlimentoCrudo', rule.domain_noun_concept)
        self.assertEquals('es un', rule.verb)

        rule_range = rule.rule_range
        self.assertTrue(rule_range.is_noun_concept())
        self.assertEquals('Alimento'.lower(), rule_range.get_range().lower())


    def test_parse_rules_no_quantification(self):
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

        root = ET.fromstring(xml)
        sbvr_specification = SBVRSpecification()
        sbvr_specification.from_xml(root)

        self.assertNotEqual(None, sbvr_specification.facts)
        self.assertEqual(0, len(sbvr_specification.facts))
        
        self.assertNotEqual(None, sbvr_specification.rules)
        self.assertEqual(1, len(sbvr_specification.rules))
        
        rule = sbvr_specification.rules[0]
        self.assertEquals('', rule.quantification.quantification_text)
        self.assertEquals('', rule.quantification.quantification_type)
        self.assertEquals('AlimentoCrudo', rule.domain_noun_concept)
        self.assertEquals('es un', rule.verb)

        rule_range = rule.rule_range
        self.assertTrue(rule_range.is_noun_concept())
        self.assertEquals('Alimento'.lower(), rule_range.get_range().lower())



    def test_parse_rules_rule_range_disjunction(self):
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

        root = ET.fromstring(xml)
        sbvr_specification = SBVRSpecification()
        sbvr_specification.from_xml(root)

        self.assertNotEqual(None, sbvr_specification.facts)
        self.assertEqual(0, len(sbvr_specification.facts))
        
        self.assertNotEqual(None, sbvr_specification.rules)
        self.assertEqual(1, len(sbvr_specification.rules))
        
        rule = sbvr_specification.rules[0]
        self.assertEquals('Each'.lower(), rule.quantification.quantification_text.lower())
        self.assertEquals('Universal'.lower(), rule.quantification.quantification_type.lower())
        self.assertEquals('LactoVegetarianismo', rule.domain_noun_concept)
        self.assertEquals('solo permite consumo de', rule.verb)

        rule_range = rule.rule_range
        self.assertTrue(rule_range.is_disjunction())
        self.assertEquals(2, len(rule_range.get_range()))
        expected_nouns = ['Lacteo', 'AlimentoOrigenVegetal']
        for noun in expected_nouns:
            self.assertTrue(noun in rule_range.get_range())
















if __name__ == '__main__':
    unittest.main()
