from transformers import pipeline
import os

ner_pipeline = pipeline("ner", model="lcampillos/roberta-es-clinical-trials-ner", tokenizer="lcampillos/roberta-es-clinical-trials-ner")

# Funcion para obtener el texto del primer fichero de una carpeta
def get_text_from_file(path):
    files = os.listdir(path)
    with open(os.path.join(path, files[0]), 'r', encoding='utf-8') as f:
        text = f.read()
    return text
    
    
def extract_symptoms(text):
    # Lista donde se guardarán los síntomas extraídos
    symptoms = []
    # Ejecutar pipeline de NER
    results = ner_pipeline(text)

    # Recorrer los resultados de NER
    i = 0
    while i < len(results):
        # Si se detecta el inicio de una entidad de tipo DISO (enfermedad)
        if results[i]['entity'] == 'B-DISO':
            j = i + 1
            # Buscar el final de la entidad DISO
            while j < len(results) and results[j]['entity'] == 'I-DISO':
                j += 1

            # Extraer subcadena del síntoma y eliminar prefijo 'Ġ' si existe
            symptom = text[results[i]['start']:results[j-1]['end']].lstrip('Ġ')
            # Verificar si es necesario agregar espacios entre palabras
            for k in range(i+1, j):
                # Si hay un espacio entre las palabras de las entidades DISO, agregar espacio
                if results[k]['start'] > results[k-1]['end']:
                    symptom += ' ' + text[results[k-1]['end']:results[k]['start']].lstrip('Ġ')

            # Agregar síntoma a la lista
            symptoms.append(symptom)
            i = j
        else:
            i += 1

    # Eliminar espacios en blanco innecesarios
    for i in range(len(symptoms)):
        symptoms[i] = symptoms[i].strip()

    return symptoms


def classify_text(text):
        # Extracción de síntomas
    symptoms = extract_symptoms(text)
    
    # Ponderación de los síntomas
    symptom_weights = {'fiebre': 3, 'dolor de cabeza': 5, 'fatiga': 2, 'pérdida de peso': 4, 'sudores nocturnos': 4}
    
    # Cálculo de la puntuación de síntomas
    symptom_score = sum([symptom_weights.get(symptom, 0) for symptom in symptoms])
    
    # Clasificación del texto según las reglas
    if "VIH" in text and symptom_score >= 10:
        return "VIH positivo (síntomas relevantes)"
    else:
        return "VIH negativo"
    
def testManual():
    text1 = "El paciente se presentó con fiebre y fatiga. Se sospecha que puede tener VIH debido a sus antecedentes."
    print(extract_symptoms(text1)) # VIH negativo

    text2 = "La paciente tiene VIH y presenta dolor de cabeza, fatiga y sudores nocturnos."
    print(extract_symptoms(text2)) # VIH positivo (síntomas relevantes)

    text3 = "No hay indicios de VIH en el paciente, pero presenta pérdida de peso y sudores nocturnos, fiebre, dolor de cabeza y fatiga."
    print(extract_symptoms(text3)) # VIH negativo

    text4 = "El paciente africano se presentó con dolor de cabeza y fiebre. Se sospecha de VIH."
    extract_symptoms(text4) # VIH negativo
    
def testNota1():
    text = get_text_from_file('datasets')
    print(extract_symptoms(text))

testNota1()
