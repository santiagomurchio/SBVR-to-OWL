class Quantification:
    """ 
    This class holds the quantification element of the SBVR rules. It has a type, which can be, 
    for example, 'Universal', and a text, which can be, in this case 'Each'.
    """

    quantification_type = None
    quantification_text = ''

    def __init__(self, quantification_type, quantification_text):
        """
        Constructor
        """
        self.quantification_type = quantification_type
        self.quantification_text = quantification_text
        
