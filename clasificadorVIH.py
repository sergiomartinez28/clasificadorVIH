from negEx import NegEx
from symptoms_processor import SymptomsProcessor
from text_processor import TextProcessor


class ClasificadorVIH:
    def __init__(self):
        self.text_processor = TextProcessor()
        self.symptoms_processor = SymptomsProcessor()
        self.negEx = NegEx()

    def execute(self, path, n_texto, theshold):
        texto = self.text_processor.get_text_from_file(path, n_texto)
        sintomas = self.text_processor.extract_symptoms(texto)
        sintomas_afirmados = self.negEx.execute_negex(sintomas, texto)
        infected, score = self.symptoms_processor.detect_vih(texto, sintomas_afirmados, theshold)
        return infected, score
    
    def symptoms_analysis(self, n_texto):
        texto = self.text_processor.get_text_from_file('datasets2', n_texto)
        sintomas = self.text_processor.extract_symptoms(texto)
        sintomas_afirmados = self.negEx.execute_negex(sintomas, texto)
        sintomas_g1, score_g1 = self.symptoms_processor.score_group1(sintomas_afirmados)
        sintomas_g2, score_g2 = self.symptoms_processor.score_group2(sintomas_afirmados)
        sintomas_g3, score_g3 = self.symptoms_processor.score_group3(sintomas_afirmados)
        score_g4 = self.symptoms_processor.group4(texto)
        score_g5 = self.symptoms_processor.group5(texto)
        sintomas_g6, score_g6 = self.symptoms_processor.score_group6(sintomas_afirmados)
        sintomas_g7, score_g7 = self.symptoms_processor.score_group7(sintomas_afirmados, texto)
        sintomas_g8, score_g8 = self.symptoms_processor.score_group8(sintomas_afirmados)
        analisis_g1 = (sintomas_g1, score_g1)
        analisis_g2 = (sintomas_g2, score_g2)
        analisis_g3 = (sintomas_g3, score_g3)
        analisis_g6 = (sintomas_g6, score_g6)
        analisis_g7 = (sintomas_g7, score_g7)
        analisis_g8 = (sintomas_g8, score_g8)
        infected, score = self.symptoms_processor.detect_vih(texto, sintomas_afirmados)
        
        return analisis_g1, analisis_g2, analisis_g3, score_g4, score_g5, analisis_g6, analisis_g7, analisis_g8, score
        
