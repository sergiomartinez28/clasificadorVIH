import os
from transformers import pipeline

class TextProcessor:
    def __init__(self):
        # Inicializar la pipeline de NER con el modelo y tokenizer específicos
        self.ner_pipeline = pipeline("ner", model="lcampillos/roberta-es-clinical-trials-ner", tokenizer="lcampillos/roberta-es-clinical-trials-ner")
    
    def get_text_from_file(self, path, number):
        """
        Obtiene el texto del primer fichero de una carpeta.
        
        :param path: Ruta de la carpeta que contiene los archivos.
        :param number: Número del archivo a leer (empezando desde 0).
        :return: Texto leído del archivo especificado.
        """
        files = os.listdir(path)
        # Asegúrate de que el índice no exceda el número de archivos disponibles
        if number < len(files):
            file_name = files[number]
            
            file_path = os.path.join(path, file_name)
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            return text
        else:
            print(f"No hay suficientes archivos en el directorio. Intentando leer archivo número {number} en un directorio con {len(files)} archivos.")
            return ""  # Devuelve una cadena vacía si el índice está fuera de rango
        
    def extract_symptoms(self, text):
        """
        Extrae los síntomas de un texto dado.

        :param text: Texto del cual extraer los síntomas.
        :return: Lista de síntomas extraídos.
        """
        symptoms = []
        results = self.ner_pipeline(text)
        i = 0
        while i < len(results):
            if results[i]['entity'] == 'B-DISO':
                j = i + 1
                while j < len(results) and (results[j]['entity'] == 'I-DISO' or results[j]['start'] == results[j-1]['end']):
                    j += 1
                symptom = text[results[i]['start']:results[j-1]['end']].lstrip('Ġ')
                for k in range(i+1, j):
                    if results[k]['start'] > results[k-1]['end']:
                        symptom += ' ' + text[results[k-1]['end']:results[k]['start']].lstrip('Ġ')
                if symptom not in symptoms:
                    symptoms.append(symptom)
                i = j
            else:
                i += 1
        symptoms = [symptom.strip() for symptom in symptoms]
        return symptoms