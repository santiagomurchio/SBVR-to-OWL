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


    def test_from_xml_binary_verb_concept(self):
        xml = '''<?xml version="1.0"?> 
                   <sbvr-specification>
                     <sbvr-term>
                       <sbvr-term-name>permite_comer</sbvr-term-name>
                       <sbvr-term-definition></sbvr-term-definition>
                       <sbvr-term-general-concept></sbvr-term-general-concept>
                       <sbvr-term-concept-type>binary verb concept</sbvr-term-concept-type>
                       <sbvr-term-synonym>permite_consumo_de</sbvr-term-synonym>
                       <sbvr-term-necessity></sbvr-term-necessity>
                     </sbvr-term>
                 </sbvr-specification>'''

        root = ET.fromstring(xml)
        sbvr_specification = SBVRSpecification()
        sbvr_specification.from_xml(root)

        self.assert_list_len(1, sbvr_specification.get_terms())

        term = sbvr_specification.get_terms()[0]
        self.assertEquals('permite_comer', term.get_name().lower())
        self.assertEquals(None, term.get_definition())
        self.assertEquals(None, term.get_general_concept())
        self.assertEquals('binary verb concept', term.get_concept_type().lower())
        self.assertEquals('permite_consumo_de'.lower(), term.get_synonym().lower())
        self.assertEquals(None, term.get_necessity())

        
    def test_from_xml_binary_verb_concept(self):
        xml = '''<?xml version="1.0"?> 
                   <sbvr-specification>
                     <sbvr-term>
                       <sbvr-term-name>permite_consumo_de</sbvr-term-name>
                       <sbvr-term-definition></sbvr-term-definition>
                       <sbvr-term-general-concept></sbvr-term-general-concept>
                       <sbvr-term-concept-type>binary verb concept</sbvr-term-concept-type>
                       <sbvr-term-synonym>permite_comer</sbvr-term-synonym>
                       <sbvr-term-necessity>
                         <sbvr-role position="1">RegimenAlimentario</sbvr-role>
                         <sbvr-role position="2">Alimento</sbvr-role>
                       </sbvr-term-necessity>
                   </sbvr-term>
                 </sbvr-specification>'''

        root = ET.fromstring(xml)
        sbvr_specification = SBVRSpecification()
        sbvr_specification.from_xml(root)

        self.assert_list_len(1, sbvr_specification.get_terms())

        term = sbvr_specification.get_terms()[0]
        self.assertEquals('permite_consumo_de', term.get_name().lower())
        self.assertEquals(None, term.get_definition())
        self.assertEquals(None, term.get_general_concept())
        self.assertEquals('binary verb concept', term.get_concept_type().lower())
        self.assertEquals('permite_comer'.lower(), term.get_synonym().lower())
        
        necessity = term.get_necessity()
        self.assert_list_len(2, necessity.get_roles())
        self.assertEquals('RegimenAlimentario', necessity.get_roles()[0])
        self.assertEquals('Alimento', necessity.get_roles()[1])

    def test_from_xml_term_with_term_definition_necessity_and_verb(self):
        xml = '''<?xml version="1.0"?> 
                 <sbvr-specification>
                   <sbvr-term>
                       <sbvr-term-name>RegimenAlimentario</sbvr-term-name>
                       <sbvr-term-definition>
                         <sbvr-verb>permite_consumo_de</sbvr-verb>
                         <sbvr-quantification type="existential"></sbvr-quantification>
                         <sbvr-disjunction>
                           <sbvr-concept>Miel</sbvr-concept>
	                   <sbvr-concept>AlimentoOrigenVegetal</sbvr-concept>
                         </sbvr-disjunction>
                       </sbvr-term-definition>
                       <sbvr-term-general-concept></sbvr-term-general-concept>
                       <sbvr-term-concept-type>general concept</sbvr-term-concept-type>
                       <sbvr-term-synonym>Dieta</sbvr-term-synonym>
                       <sbvr-term-necessity>
                         <sbvr-verb>debe_consumir</sbvr-verb>
                         <sbvr-quantification type="at-least-N">1</sbvr-quantification>
	                   <sbvr-concept>AlimentoOrigenVegetal</sbvr-concept>
                       </sbvr-term-necessity>
                   </sbvr-term>
                     <sbvr-term>
                       <sbvr-term-name>permite_consumo_de</sbvr-term-name>
                       <sbvr-term-definition></sbvr-term-definition>
                       <sbvr-term-general-concept></sbvr-term-general-concept>
                       <sbvr-term-concept-type>binary verb concept</sbvr-term-concept-type>
                       <sbvr-term-synonym>permite_comer</sbvr-term-synonym>
                       <sbvr-term-necessity>
                         <sbvr-role position="1">RegimenAlimentario</sbvr-role>
                         <sbvr-role position="2">Alimento</sbvr-role>
                       </sbvr-term-necessity>
                   </sbvr-term>
                 </sbvr-specification>'''

        root = ET.fromstring(xml)
        sbvr_specification = SBVRSpecification()
        sbvr_specification.from_xml(root)

        self.assert_list_len(2, sbvr_specification.get_terms())

        verb_term = None
        concept_term = None

        if sbvr_specification.get_terms()[0].is_concept_type():
            concept_term = sbvr_specification.get_terms()[0]
            verb_term = sbvr_specification.get_terms()[1]
        else:
            concept_term = sbvr_specification.get_terms()[1]
            verb_term = sbvr_specification.get_terms()[0]

        # concept_term verification
        self.assertEquals('RegimenAlimentario'.lower(), concept_term.get_name().lower())
        self.assertEquals(None, concept_term.get_general_concept())
        self.assertEquals('general concept', concept_term.get_concept_type().lower())
        self.assertEquals('Dieta'.lower(), concept_term.get_synonym().lower())

        definition = concept_term.get_definition()
        self.assertEquals('permite_consumo_de', definition.get_verb().lower())
        
        quantification = definition.get_quantification()
        self.assertEquals('Existential'.lower(), quantification.get_type().lower())
        self.assertEquals(None, quantification.get_value())
        
        definition_range = definition.get_rule_range()
        self.assertTrue(definition_range.is_disjunction())
        self.assert_list_len(2, definition_range.get_range())
        self.assertTrue('AlimentoOrigenVegetal' in definition_range.get_range())
        self.assertTrue('Miel' in definition_range.get_range())

        necessity = concept_term.get_necessity()
        self.assertEquals('debe_consumir', necessity.get_verb().lower())
        
        necessity_quantification = necessity.get_quantification()
        self.assertEquals('at-least-N'.lower(), necessity_quantification.get_type().lower())
        self.assertEquals('1', necessity_quantification.get_value().lower())

        necessity_range = necessity.get_rule_range()
        self.assertTrue(necessity_range.is_noun_concept())
        self.assertEquals('AlimentoOrigenVegetal', necessity_range.get_range())

        # verb_term verification
        self.assertEquals('permite_consumo_de', verb_term.get_name().lower())
        self.assertEquals(None, verb_term.get_definition())
        self.assertEquals(None, verb_term.get_general_concept())
        self.assertEquals('binary verb concept', verb_term.get_concept_type().lower())
        self.assertEquals('permite_comer'.lower(), verb_term.get_synonym().lower())
        
        verb_term_necessity = verb_term.get_necessity()
        self.assert_list_len(2, verb_term_necessity.get_roles())
        self.assertEquals('RegimenAlimentario', verb_term_necessity.get_roles()[0])
        self.assertEquals('Alimento', verb_term_necessity.get_roles()[1])

    def assert_list_len(self, expected_size, list):
        """
        Asserts that the list is not None and asserts the size of the list against the expected.
        """
        self.assertNotEqual(None, list)
        self.assertEqual(expected_size, len(list))
        

if __name__ == '__main__':
    unittest.main()
