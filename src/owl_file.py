class OWLFile:
    """
    This class is meant to hold tags that are generic in the owl file.
    """

    XML_VERSION = '''<?xml version="1.0"?>'''

    OWL_RDF_NAMESPACES = '''
        <rdf:RDF xmlns="http://desibo.frsf.utn.edu.ar/ontologies/2014/8/untitled-ontology-122#"
          xml:base="http://desibo.frsf.utn.edu.ar/ontologies/2014/8/untitled-ontology-122"
          xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
          xmlns:owl="http://www.w3.org/2002/07/owl#"
          xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
          xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
        
          {owl_file_content}
        
        </rdf:RDF>'''

    OWL_DOCTYPE = '''
        <!DOCTYPE rdf:RDF [
          <!ENTITY owl "http://www.w3.org/2002/07/owl#" >
          <!ENTITY xsd "http://www.w3.org/2001/XMLSchema#" >
          <!ENTITY rdfs "http://www.w3.org/2000/01/rdf-schema#" >
          <!ENTITY rdf "http://www.w3.org/1999/02/22-rdf-syntax-ns#" >
        ]>'''
