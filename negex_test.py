import re
import subprocess
import os

from negEx import NegEx
from symptoms_processor import SymptomsProcessor
from text_processor import TextProcessor




text_processor = TextProcessor()
symptoms_processor = SymptomsProcessor()
negEx = NegEx()

for i in range (0,10):
    texto = text_processor.get_text_from_file('datasets', i)
    sintomas = text_processor.extract_symptoms(texto)
    sintomas_filtrados = symptoms_processor.extract_vih_symptoms(sintomas, texto)
    lista_sintomas = [tupla[0] for tupla in sintomas_filtrados]
    puntos_sintomas = [tupla[1] for tupla in sintomas_filtrados]
    #print(f"Texto: {texto}\n\nSintomas: {sintomas}\n\nSíntomas filtrados: {lista_sintomas}")
    
    sintomas_afirmados = negEx.execute_negex(lista_sintomas, texto)
    print(f"Sintomas: {lista_sintomas}")
    print(f"Síntomas afirmados: {sintomas_afirmados}")
    vih = symptoms_processor.detect_vih(texto, sintomas_afirmados)
    print(f"VIH: {vih}")
