import unittest
from src.sbvr.sbvrspecification import SBVRSpecification
from src.sbvr.fact import *
from src.sbvr.rule import *
import xml.etree.ElementTree as ET


class SBVRSpecificationTest(unittest.TestCase):
    """
    Test cases for the SBVR specification parser
    """

    def test_parse_rules_empty_string(self):
        xml = '''<?xml version="1.0"?> 
                   <sbvr-specification>
                 </sbvr-specification>'''

        root = ET.fromstring(xml)
        sbvr_specification = SBVRSpecification()
        sbvr_specification.from_xml(root)

        self.assert_list_len(0, sbvr_specification.get_terms())
        

    def test_from_xml_simple_term(self):
        xml = '''<?xml version="1.0"?> 
                   <sbvr-specification>
                     <sbvr-term>
                         <sbvr-term-name>AlimentoOrigenAnimal</sbvr-term-name>
                         <sbvr-term-definition></sbvr-term-definition>
                         <sbvr-term-general-concept>Alimento</sbvr-term-general-concept>
                         <sbvr-term-concept-type>general concept</sbvr-term-concept-type>
                         <sbvr-term-synonym>AlimentoOrigenAnimalSinonimo</sbvr-term-synonym>
                         <sbvr-term-necessity></sbvr-term-necessity>
                     </sbvr-term>                     
                 </sbvr-specification>'''

        root = ET.fromstring(xml)
        sbvr_specification = SBVRSpecification()
        sbvr_specification.from_xml(root)

        self.assert_list_len(1, sbvr_specification.get_terms())

        term = sbvr_specification.get_terms()[0]
        self.assertEquals('AlimentoOrigenAnimal'.lower(), term.get_name().lower())
        self.assertEquals(None, term.get_definition())
        self.assertEquals('Alimento'.lower(), term.get_general_concept().lower())
        self.assertEquals('general concept', term.get_concept_type().lower())
        self.assertEquals('AlimentoOrigenAnimalSinonimo'.lower(), term.get_synonym().lower())
        self.assertEquals(None, term.get_necessity())

    def test_from_xml_term_with_single_concept_necessity(self):
        xml = '''<?xml version="1.0"?> 
                 <sbvr-specification>
                   <sbvr-term>
                       <sbvr-term-name>RegimenAlimentario</sbvr-term-name>
                       <sbvr-term-definition></sbvr-term-definition>
                       <sbvr-term-general-concept></sbvr-term-general-concept>
                       <sbvr-term-concept-type>general concept</sbvr-term-concept-type>
                       <sbvr-term-synonym>Dieta</sbvr-term-synonym>
                       <sbvr-term-necessity>
                         <sbvr-verb>permite consumo de</sbvr-verb>
                         <sbvr-quantification type="at-least-N">1</sbvr-quantification>
                         <sbvr-concept>Alimento</sbvr-concept>
                       </sbvr-term-necessity>
                   </sbvr-term>
                 </sbvr-specification>'''

        root = ET.fromstring(xml)
        sbvr_specification = SBVRSpecification()
        sbvr_specification.from_xml(root)

        self.assert_list_len(1, sbvr_specification.get_terms())

        term = sbvr_specification.get_terms()[0]
        self.assertEquals('RegimenAlimentario'.lower(), term.get_name().lower())
        self.assertEquals(None, term.get_definition())
        self.assertEquals(None, term.get_general_concept())
        self.assertEquals('general concept', term.get_concept_type().lower())
        self.assertEquals('Dieta'.lower(), term.get_synonym().lower())

        necessity = term.get_necessity()
        self.assertEquals('permite consumo de', necessity.get_verb().lower())
        
        quantification = necessity.get_quantification()
        self.assertEquals('at-least-N'.lower(), quantification.get_type().lower())
        self.assertEquals('1', quantification.get_value().lower())
        
        necessity_range = necessity.get_rule_range()
        self.assertTrue(necessity_range.is_noun_concept())
        self.assertEquals('Alimento'.lower(), necessity_range.get_range().lower())
        
                
    def test_from_xml_term_with_conjunction_necessity(self):
         xml = '''<?xml version="1.0"?> 
                  <sbvr-specification>
                   <sbvr-term>
                       <sbvr-term-name>RegimenAlimentario</sbvr-term-name>
                       <sbvr-term-definition></sbvr-term-definition>
                       <sbvr-term-general-concept></sbvr-term-general-concept>
                       <sbvr-term-concept-type>general concept</sbvr-term-concept-type>
                       <sbvr-term-synonym>Dieta</sbvr-term-synonym>
                       <sbvr-term-necessity>
                         <sbvr-verb>permite consumo de</sbvr-verb>
                         <sbvr-quantification type="at-least-N">1</sbvr-quantification>
                         <sbvr-conjunction>
                           <sbvr-concept>Miel</sbvr-concept>
	                   <sbvr-concept>AlimentoOrigenVegetal</sbvr-concept>
                         </sbvr-conjunction>
                       </sbvr-term-necessity>
                   </sbvr-term>
                 </sbvr-specification>'''

         root = ET.fromstring(xml)
         sbvr_specification = SBVRSpecification()
         sbvr_specification.from_xml(root)

         self.assert_list_len(1, sbvr_specification.get_terms())

         term = sbvr_specification.get_terms()[0]
         self.assertEquals('RegimenAlimentario'.lower(), term.get_name().lower())
         self.assertEquals(None, term.get_definition())
         self.assertEquals(None, term.get_general_concept())
         self.assertEquals('general concept', term.get_concept_type().lower())
         self.assertEquals('Dieta'.lower(), term.get_synonym().lower())
         
         necessity = term.get_necessity()
         self.assertEquals('permite consumo de', necessity.get_verb().lower())
         
         quantification = necessity.get_quantification()
         self.assertEquals('at-least-N'.lower(), quantification.get_type().lower())
         self.assertEquals('1', quantification.get_value().lower())
         
         necessity_range = necessity.get_rule_range()
         self.assertTrue(necessity_range.is_conjunction())
         self.assert_list_len(2, necessity_range.get_range())
         self.assertTrue('Miel' in necessity_range.get_range())
         self.assertTrue('AlimentoOrigenVegetal' in necessity_range.get_range())

    def test_from_xml_term_with_single_term_definition(self):
        xml = '''<?xml version="1.0"?> 
                 <sbvr-specification>
                   <sbvr-term>
                       <sbvr-term-name>RegimenAlimentario</sbvr-term-name>
                       <sbvr-term-definition>
                         <sbvr-verb>permite consumo de</sbvr-verb>
                         <sbvr-quantification type="existential"></sbvr-quantification>
	                 <sbvr-concept>Miel</sbvr-concept>
                       </sbvr-term-definition>
                       <sbvr-term-general-concept></sbvr-term-general-concept>
                       <sbvr-term-concept-type>general concept</sbvr-term-concept-type>
                       <sbvr-term-synonym>Dieta</sbvr-term-synonym>
                       <sbvr-term-necessity></sbvr-term-necessity>
                   </sbvr-term>
                 </sbvr-specification>'''

        root = ET.fromstring(xml)
        sbvr_specification = SBVRSpecification()
        sbvr_specification.from_xml(root)

        self.assert_list_len(1, sbvr_specification.get_terms())

        term = sbvr_specification.get_terms()[0]
        self.assertEquals('RegimenAlimentario'.lower(), term.get_name().lower())
        self.assertEquals(None, term.get_necessity())
        self.assertEquals(None, term.get_general_concept())
        self.assertEquals('general concept', term.get_concept_type().lower())
        self.assertEquals('Dieta'.lower(), term.get_synonym().lower())

        definition = term.get_definition()
        self.assertEquals('permite consumo de', definition.get_verb().lower())
        
        quantification = definition.get_quantification()
        self.assertEquals('Existential'.lower(), quantification.get_type().lower())
        self.assertEquals(None, quantification.get_value())
        
        definition_range = definition.get_rule_range()
        self.assertTrue(definition_range.is_noun_concept())
        self.assertEquals('Miel', definition_range.get_range())

        
    def test_from_xml_term_with_conjunction_term_definition(self):
        xml = '''<?xml version="1.0"?> 
                 <sbvr-specification>
                   <sbvr-term>
                       <sbvr-term-name>RegimenAlimentario</sbvr-term-name>
                       <sbvr-term-definition>
                         <sbvr-verb>permite consumo de</sbvr-verb>
                         <sbvr-quantification type="existential"></sbvr-quantification>
                         <sbvr-conjunction>
                           <sbvr-concept>Miel</sbvr-concept>
	                   <sbvr-concept>AlimentoOrigenVegetal</sbvr-concept>
                         </sbvr-conjunction>
                       </sbvr-term-definition>
                       <sbvr-term-general-concept></sbvr-term-general-concept>
                       <sbvr-term-concept-type>general concept</sbvr-term-concept-type>
                       <sbvr-term-synonym>Dieta</sbvr-term-synonym>
                       <sbvr-term-necessity></sbvr-term-necessity>
                   </sbvr-term>
                 </sbvr-specification>'''

        root = ET.fromstring(xml)
        sbvr_specification = SBVRSpecification()
        sbvr_specification.from_xml(root)

        self.assert_list_len(1, sbvr_specification.get_terms())

        term = sbvr_specification.get_terms()[0]
        self.assertEquals('RegimenAlimentario'.lower(), term.get_name().lower())
        self.assertEquals(None, term.get_necessity())
        self.assertEquals(None, term.get_general_concept())
        self.assertEquals('general concept', term.get_concept_type().lower())
        self.assertEquals('Dieta'.lower(), term.get_synonym().lower())

        definition = term.get_definition()
        self.assertEquals('permite consumo de', definition.get_verb().lower())
        
        quantification = definition.get_quantification()
        self.assertEquals('Existential'.lower(), quantification.get_type().lower())
        self.assertEquals(None, quantification.get_value())
        
        definition_range = definition.get_rule_range()
        self.assertTrue(definition_range.is_conjunction())
        self.assert_list_len(2, definition_range.get_range())
        self.assertTrue('AlimentoOrigenVegetal' in definition_range.get_range())
        self.assertTrue('Miel' in definition_range.get_range())

    def test_from_xml_term_with_disjunction_term_definition(self):
        xml = '''<?xml version="1.0"?> 
                 <sbvr-specification>
                   <sbvr-term>
                       <sbvr-term-name>RegimenAlimentario</sbvr-term-name>
                       <sbvr-term-definition>
                         <sbvr-verb>permite consumo de</sbvr-verb>
                         <sbvr-quantification type="existential"></sbvr-quantification>
                         <sbvr-disjunction>
                           <sbvr-concept>Miel</sbvr-concept>
	                   <sbvr-concept>AlimentoOrigenVegetal</sbvr-concept>
                         </sbvr-disjunction>
                       </sbvr-term-definition>
                       <sbvr-term-general-concept></sbvr-term-general-concept>
                       <sbvr-term-concept-type>general concept</sbvr-term-concept-type>
                       <sbvr-term-synonym>Dieta</sbvr-term-synonym>
                       <sbvr-term-necessity></sbvr-term-necessity>
                   </sbvr-term>
                 </sbvr-specification>'''

        root = ET.fromstring(xml)
        sbvr_specification = SBVRSpecification()
        sbvr_specification.from_xml(root)

        self.assert_list_len(1, sbvr_specification.get_terms())

        term = sbvr_specification.get_terms()[0]
        self.assertEquals('RegimenAlimentario'.lower(), term.get_name().lower())
        self.assertEquals(None, term.get_necessity())
        self.assertEquals(None, term.get_general_concept())
        self.assertEquals('general concept', term.get_concept_type().lower())
        self.assertEquals('Dieta'.lower(), term.get_synonym().lower())

        definition = term.get_definition()
        self.assertEquals('permite consumo de', definition.get_verb().lower())
        
        quantification = definition.get_quantification()
        self.assertEquals('Existential'.lower(), quantification.get_type().lower())
        self.assertEquals(None, quantification.get_value())
        
        definition_range = definition.get_rule_range()
        self.assertTrue(definition_range.is_disjunction())
        self.assert_list_len(2, definition_range.get_range())
        self.assertTrue('AlimentoOrigenVegetal' in definition_range.get_range())
        self.assertTrue('Miel' in definition_range.get_range())

        

    # def test_parse_rules_no_quantification(self):
    #     xml = '''<?xml version="1.0"?> 
    #                <sbvr-specification>
    #                  <sbvr-facts>
    #                  </sbvr-facts>

    #                  <sbvr-rules>
    #                    <sbvr-rule>
    #                      <domain-noun-concept>AlimentoCrudo</domain-noun-concept>
    #                      <verb>es un</verb>
    #                      <range-noun-concept>Alimento</range-noun-concept>
    #                    </sbvr-rule>

    #                  </sbvr-rules>
    #              </sbvr-specification>'''

    #     root = ET.fromstring(xml)
    #     sbvr_specification = SBVRSpecification()
    #     sbvr_specification.from_xml(root)

    #     self.assert_list_len(1, sbvr_specification.rules)
    #     self.assert_list_len(0, sbvr_specification.facts)
        
    #     rule = sbvr_specification.rules[0]
    #     self.assertEquals('', rule.quantification.quantification_text)
    #     self.assertEquals('', rule.quantification.quantification_type)
    #     self.assertEquals('AlimentoCrudo', rule.domain_noun_concept)
    #     self.assertEquals('es un', rule.verb)

    #     rule_range = rule.rule_range
    #     self.assertTrue(rule_range.is_noun_concept())
    #     self.assertEquals('Alimento'.lower(), rule_range.get_range().lower())



    # def test_parse_rules_range_disjunction(self):
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

    #     root = ET.fromstring(xml)
    #     sbvr_specification = SBVRSpecification()
    #     sbvr_specification.from_xml(root)

    #     self.assert_list_len(1, sbvr_specification.rules)
    #     self.assert_list_len(0, sbvr_specification.facts)

    #     rule = sbvr_specification.rules[0]
    #     self.assertEquals('Each'.lower(), rule.quantification.quantification_text.lower())
    #     self.assertEquals('Universal'.lower(), rule.quantification.quantification_type.lower())
    #     self.assertEquals('LactoVegetarianismo', rule.domain_noun_concept)
    #     self.assertEquals('solo permite consumo de', rule.verb)

    #     rule_range = rule.rule_range
    #     self.assertTrue(rule_range.is_disjunction())
    #     self.assertEquals(2, len(rule_range.get_range()))
    #     expected_nouns = ['Lacteo', 'AlimentoOrigenVegetal']
    #     for noun in expected_nouns:
    #         self.assertTrue(noun in rule_range.get_range())


    # def test_parse_rules_range_conjunction(self):
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

    #     root = ET.fromstring(xml)
    #     sbvr_specification = SBVRSpecification()
    #     sbvr_specification.from_xml(root)

    #     self.assert_list_len(1, sbvr_specification.rules)
    #     self.assert_list_len(0, sbvr_specification.facts)

    #     rule = sbvr_specification.rules[0]
    #     self.assertEquals('Each'.lower(), rule.quantification.quantification_text.lower())
    #     self.assertEquals('Universal'.lower(), rule.quantification.quantification_type.lower())
    #     self.assertEquals('LactoVegetarianismo', rule.domain_noun_concept)
    #     self.assertEquals('solo permite consumo de', rule.verb)

    #     rule_range = rule.rule_range
    #     self.assertTrue(rule_range.is_conjunction())
    #     self.assertEquals(2, len(rule_range.get_range()))
    #     expected_nouns = ['Lacteo', 'AlimentoOrigenVegetal']
    #     for noun in expected_nouns:
    #         self.assertTrue(noun in rule_range.get_range())
        
    #     del sbvr_specification


    # def test_parse_facts_simple_fact(self):
    #     xml = '''<?xml version="1.0"?> 
    #                <sbvr-specification>
    #                  <sbvr-facts>
    #                    <sbvr-fact>
    #                      <domain-noun-concept>AlimentoCrudo</domain-noun-concept>
    #                      <verb>es un</verb>
    #                      <range-noun-concept>Alimento</range-noun-concept>
    #                    </sbvr-fact>
    #                  </sbvr-facts>

    #                  <sbvr-rules>
    #                  </sbvr-rules>
    #              </sbvr-specification>'''

    #     root = ET.fromstring(xml)
    #     sbvr_specification = SBVRSpecification()
    #     sbvr_specification.from_xml(root)

    #     self.assert_list_len(0, sbvr_specification.rules)
    #     self.assert_list_len(1, sbvr_specification.facts)
                
    #     fact = sbvr_specification.facts[0]
    #     self.assertEquals('AlimentoCrudo'.lower(), fact.domain_noun_concept.lower())
    #     self.assertEquals('es un'.lower(), fact.verb.lower())

    #     fact_range = fact.fact_range
    #     self.assertTrue(fact_range.is_noun_concept())
    #     self.assertEquals('Alimento'.lower(), fact_range.get_range().lower())


    # def test_parse_facts_disjunction(self):
    #     xml = '''<?xml version="1.0"?> 
    #                <sbvr-specification>
    #                  <sbvr-facts>
    #                    <sbvr-fact>
    #                      <domain-noun-concept>LactoVegetarianismo</domain-noun-concept>
    #                      <verb>solo permite consumo de</verb>
    #                      <disjunction>
    #                    	   <range-noun-concept>Lacteo</range-noun-concept>
    #                    	   <range-noun-concept>AlimentoOrigenVegetal</range-noun-concept>
    #                      </disjunction>
    #                    </sbvr-fact>
    #                    </sbvr-facts>
    #                  <sbvr-rules>
    #                  </sbvr-rules>
    #              </sbvr-specification>'''

    #     root = ET.fromstring(xml)
    #     sbvr_specification = SBVRSpecification()
    #     sbvr_specification.from_xml(root)

    #     self.assert_list_len(0, sbvr_specification.rules)
    #     self.assert_list_len(1, sbvr_specification.facts)
                
    #     fact = sbvr_specification.facts[0]
    #     self.assertEquals('LactoVegetarianismo', fact.domain_noun_concept)
    #     self.assertEquals('solo permite consumo de', fact.verb)

    #     fact_range = fact.fact_range
    #     self.assertTrue(fact_range.is_disjunction())
    #     self.assert_list_len(2, fact_range.get_range())
    #     expected_nouns = ['Lacteo', 'AlimentoOrigenVegetal']
    #     for noun in expected_nouns:
    #         self.assertTrue(noun in fact_range.get_range())


    # def test_parse_facts_conjunction(self):
    #     xml = '''<?xml version="1.0"?> 
    #                <sbvr-specification>
    #                  <sbvr-facts>
    #                    <sbvr-fact>
    #                      <domain-noun-concept>LactoVegetarianismo</domain-noun-concept>
    #                      <verb>solo permite consumo de</verb>
    #                      <conjunction>
    #                    	   <range-noun-concept>Lacteo</range-noun-concept>
    #                    	   <range-noun-concept>AlimentoOrigenVegetal</range-noun-concept>
    #                      </conjunction>
    #                    </sbvr-fact>
    #                    </sbvr-facts>
    #                  <sbvr-rules>
    #                  </sbvr-rules>
    #              </sbvr-specification>'''

    #     root = ET.fromstring(xml)
    #     sbvr_specification = SBVRSpecification()
    #     sbvr_specification.from_xml(root)

    #     self.assert_list_len(0, sbvr_specification.rules)
    #     self.assert_list_len(1, sbvr_specification.facts)
                
    #     fact = sbvr_specification.facts[0]
    #     self.assertEquals('LactoVegetarianismo', fact.domain_noun_concept)
    #     self.assertEquals('solo permite consumo de', fact.verb)

    #     fact_range = fact.fact_range
    #     self.assertTrue(fact_range.is_conjunction())
    #     self.assert_list_len(2, fact_range.get_range())
    #     expected_nouns = ['Lacteo', 'AlimentoOrigenVegetal']
    #     for noun in expected_nouns:
    #         self.assertTrue(noun in fact_range.get_range())




    def assert_list_len(self, expected_size, list):
        """
        Asserts that the list is not None and asserts the size of the list against the expected.
        """
        self.assertNotEqual(None, list)
        self.assertEqual(expected_size, len(list))
        








if __name__ == '__main__':
    unittest.main()
