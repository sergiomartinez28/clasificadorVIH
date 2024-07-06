from negEx import NegEx
from symptoms_processor import SymptomsProcessor
from text_processor import TextProcessor


class ClasificadorReglas:
    def __init__(self):
        self.text_processor = TextProcessor()
        self.symptoms_processor = SymptomsProcessor()
        self.negEx = NegEx()
        
    def execute(self, path, n_texto):
        """
        Ejecuta el clasificador de VIH en un texto dado.
        """
        texto = self.text_processor.get_text_from_file(path, n_texto)
        sintomas = self.text_processor.extract_symptoms(texto)
        sintomas_afirmados = self.negEx.execute_negex(sintomas, texto)
        sintomas_g1, score_g1 = self.symptoms_processor.score_group1(sintomas_afirmados)
        sintomas_g2, score_g2 = self.symptoms_processor.score_group2(sintomas_afirmados)
        sintomas_g3, score_g3 = self.symptoms_processor.score_group3(sintomas_afirmados)
        sintomas_g6, score_g6 = self.symptoms_processor.score_group6(sintomas_afirmados)
        sintomas_g7, score_g7 = self.symptoms_processor.score_group7(sintomas_afirmados, texto)
        sintomas_g8, score_g8 = self.symptoms_processor.score_group8(sintomas_afirmados)
        
        if len(sintomas_g1) > 0:
            return True
        elif len(sintomas_g2) > 0:
            return True
        elif len(sintomas_g3) > 0:
            return False
        elif len(sintomas_g6) > 1:
            return True
        elif len(sintomas_g7) > 1:
            return True
        elif len(sintomas_g8) > 1:
            return True
        else:
            return False