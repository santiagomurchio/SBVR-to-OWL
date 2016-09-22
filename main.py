from src.sbvr.sbvrspecification import SBVRSpecification
from src.mapping.sbvrtoowl import SBVRToOWL

def print_help_Message():
    """
    Prints a help message to inform the user how the program should be used
    """
    print("SBVR To OWL (change) ")
    print("-----------")
    print("1.- The program will first ask you to enter the name of the xml file where the SBVR rules are defined.")
    print("If the file does not exist, an error will be thrown.")
    print("")
    print("2.- The program will ask you to enter the name of the file where the OWL will be written.")
    print("If the file does not exist, it will be created. If it does exists, and it already has content, .")
    print("it will be overwritten.")
    print("")
    print("3.- The program will ask you to enter the prefix to be used in the ontology (url).")
    print("")

def ask_output_filename():
    """ 
    Parse the xml file indicated by the user and returns its tree object.
    """
    filename = raw_input("Enter OWL ontology filename (default: ontology.owl): ")
    if filename == "":
        filename = "ontology.owl"
    return filename


def ask_input_filename():
    """ 
    Parse the xml file indicated by the user and returns its tree object.
    """
    filename = raw_input("Enter SBVR specification filename (default: rules.xml): ")
    if filename == "":
        filename = "rules.xml"
    return filename

def ask_prefix():
    """ 
    Parse the xml file indicated by the user and returns its tree object.
    """
    return  raw_input("Enter ontology base url (default: ''): ")

# Main steps
print_help_Message()
input_filename = ask_input_filename()
output_filename = ask_output_filename()
prefix = ask_prefix()

sbvr_specification = SBVRSpecification()
sbvr_specification.from_xml_file(input_filename)


sbvr_to_owl = SBVRToOWL(sbvr_specification, output_filename, prefix) 

sbvr_to_owl.transform()





