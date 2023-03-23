from transformers import pipeline

ner_pipeline = pipeline("ner", model="lcampillos/roberta-es-clinical-trials-ner", tokenizer="lcampillos/roberta-es-clinical-trials-ner")

def extract_symptoms(text):
    symptoms = []
    results = ner_pipeline(text)
    
    i = 0
    while i < len(results):
        if results[i]['entity'] == 'B-DISO':
            # Buscar entidades adyacentes con el mismo prefijo IOB
            prefix = results[i]['entity']
            j = i + 1
            while j < len(results) and results[j]['entity'] == 'I-DISO':
                j += 1
            # Fusionar las entidades adyacentes en una sola
            symptom = ' '.join([result['word'].lstrip('Ġ') for result in results[i:j]]) # los síntomas se guardarán correctamente sin los símbolos "Ġ" al principio de cada palabra.
            symptoms.append(symptom)
            i = j
        else:
            i += 1
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

text1 = "El paciente se presentó con fiebre y fatiga. Se sospecha que puede tener VIH debido a sus antecedentes."
print(classify_text(text1)) # VIH negativo

text2 = "La paciente tiene VIH y presenta dolor de cabeza, fatiga y sudores nocturnos."
print(classify_text(text2)) # VIH positivo (síntomas relevantes)

text3 = "No hay indicios de VIH en el paciente, pero presenta pérdida de peso y sudores nocturnos, fiebre, dolor de cabeza y fatiga."
print(classify_text(text3)) # VIH negativo

text4 = "El paciente africano se presentó con dolor de cabeza y fiebre. Se sospecha de VIH."
print(classify_text(text4)) # VIH negativo