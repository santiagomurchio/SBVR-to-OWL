import unittest
from src.sbvrspecification import SBVRSpecification
from src.fact import *
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

        self.assert_list_len(0, sbvr_specification.rules)
        self.assert_list_len(0, sbvr_specification.facts)
        

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

        self.assert_list_len(1, sbvr_specification.rules)
        self.assert_list_len(0, sbvr_specification.facts)

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

        self.assert_list_len(1, sbvr_specification.rules)
        self.assert_list_len(0, sbvr_specification.facts)
        
        rule = sbvr_specification.rules[0]
        self.assertEquals('', rule.quantification.quantification_text)
        self.assertEquals('', rule.quantification.quantification_type)
        self.assertEquals('AlimentoCrudo', rule.domain_noun_concept)
        self.assertEquals('es un', rule.verb)

        rule_range = rule.rule_range
        self.assertTrue(rule_range.is_noun_concept())
        self.assertEquals('Alimento'.lower(), rule_range.get_range().lower())



    def test_parse_rules_range_disjunction(self):
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

        self.assert_list_len(1, sbvr_specification.rules)
        self.assert_list_len(0, sbvr_specification.facts)

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


    def test_parse_rules_range_conjunction(self):
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

        root = ET.fromstring(xml)
        sbvr_specification = SBVRSpecification()
        sbvr_specification.from_xml(root)

        self.assert_list_len(1, sbvr_specification.rules)
        self.assert_list_len(0, sbvr_specification.facts)

        rule = sbvr_specification.rules[0]
        self.assertEquals('Each'.lower(), rule.quantification.quantification_text.lower())
        self.assertEquals('Universal'.lower(), rule.quantification.quantification_type.lower())
        self.assertEquals('LactoVegetarianismo', rule.domain_noun_concept)
        self.assertEquals('solo permite consumo de', rule.verb)

        rule_range = rule.rule_range
        self.assertTrue(rule_range.is_conjunction())
        self.assertEquals(2, len(rule_range.get_range()))
        expected_nouns = ['Lacteo', 'AlimentoOrigenVegetal']
        for noun in expected_nouns:
            self.assertTrue(noun in rule_range.get_range())
        
        del sbvr_specification


    def test_parse_facts_simple_fact(self):
        xml = '''<?xml version="1.0"?> 
                   <sbvr-specification>
                     <sbvr-facts>
                       <sbvr-fact>
                         <domain-noun-concept>AlimentoCrudo</domain-noun-concept>
                         <verb>es un</verb>
                         <range-noun-concept>Alimento</range-noun-concept>
                       </sbvr-fact>
                     </sbvr-facts>

                     <sbvr-rules>
                     </sbvr-rules>
                 </sbvr-specification>'''

        root = ET.fromstring(xml)
        sbvr_specification = SBVRSpecification()
        sbvr_specification.from_xml(root)

        self.assert_list_len(0, sbvr_specification.rules)
        self.assert_list_len(1, sbvr_specification.facts)
                
        fact = sbvr_specification.facts[0]
        self.assertEquals('AlimentoCrudo'.lower(), fact.domain_noun_concept.lower())
        self.assertEquals('es un'.lower(), fact.verb.lower())

        fact_range = fact.fact_range
        self.assertTrue(fact_range.is_noun_concept())
        self.assertEquals('Alimento'.lower(), fact_range.get_range().lower())


    def test_parse_facts_disjunction(self):
        xml = '''<?xml version="1.0"?> 
                   <sbvr-specification>
                     <sbvr-facts>
                       <sbvr-fact>
                         <domain-noun-concept>LactoVegetarianismo</domain-noun-concept>
                         <verb>solo permite consumo de</verb>
                         <disjunction>
                       	   <range-noun-concept>Lacteo</range-noun-concept>
                       	   <range-noun-concept>AlimentoOrigenVegetal</range-noun-concept>
                         </disjunction>
                       </sbvr-fact>
                       </sbvr-facts>
                     <sbvr-rules>
                     </sbvr-rules>
                 </sbvr-specification>'''

        root = ET.fromstring(xml)
        sbvr_specification = SBVRSpecification()
        sbvr_specification.from_xml(root)

        self.assert_list_len(0, sbvr_specification.rules)
        self.assert_list_len(1, sbvr_specification.facts)
                
        fact = sbvr_specification.facts[0]
        self.assertEquals('LactoVegetarianismo', fact.domain_noun_concept)
        self.assertEquals('solo permite consumo de', fact.verb)

        fact_range = fact.fact_range
        self.assertTrue(fact_range.is_disjunction())
        self.assert_list_len(2, fact_range.get_range())
        expected_nouns = ['Lacteo', 'AlimentoOrigenVegetal']
        for noun in expected_nouns:
            self.assertTrue(noun in fact_range.get_range())


    def test_parse_facts_conjunction(self):
        xml = '''<?xml version="1.0"?> 
                   <sbvr-specification>
                     <sbvr-facts>
                       <sbvr-fact>
                         <domain-noun-concept>LactoVegetarianismo</domain-noun-concept>
                         <verb>solo permite consumo de</verb>
                         <conjunction>
                       	   <range-noun-concept>Lacteo</range-noun-concept>
                       	   <range-noun-concept>AlimentoOrigenVegetal</range-noun-concept>
                         </conjunction>
                       </sbvr-fact>
                       </sbvr-facts>
                     <sbvr-rules>
                     </sbvr-rules>
                 </sbvr-specification>'''

        root = ET.fromstring(xml)
        sbvr_specification = SBVRSpecification()
        sbvr_specification.from_xml(root)

        self.assert_list_len(0, sbvr_specification.rules)
        self.assert_list_len(1, sbvr_specification.facts)
                
        fact = sbvr_specification.facts[0]
        self.assertEquals('LactoVegetarianismo', fact.domain_noun_concept)
        self.assertEquals('solo permite consumo de', fact.verb)

        fact_range = fact.fact_range
        self.assertTrue(fact_range.is_conjunction())
        self.assert_list_len(2, fact_range.get_range())
        expected_nouns = ['Lacteo', 'AlimentoOrigenVegetal']
        for noun in expected_nouns:
            self.assertTrue(noun in fact_range.get_range())




    def assert_list_len(self, expected_size, list):
        """
        Asserts that the list is not None and asserts the size of the list against the expected.
        """
        self.assertNotEqual(None, list)
        self.assertEqual(expected_size, len(list))
        








if __name__ == '__main__':
    unittest.main()
