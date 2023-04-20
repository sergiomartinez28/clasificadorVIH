from transformers import pipeline
import os

ner_pipeline = pipeline("ner", model="lcampillos/roberta-es-clinical-trials-ner", tokenizer="lcampillos/roberta-es-clinical-trials-ner")

# Funcion para obtener el texto del primer fichero de una carpeta
def get_text_from_file(path):
    files = os.listdir(path)
    with open(os.path.join(path, files[1]), 'r', encoding='utf-8') as f:
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
            while j < len(results) and (results[j]['entity'] == 'I-DISO' or results[j]['start'] == results[j-1]['end']):
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


def detect_sida(text):
    
    
    symptoms = extract_symptoms(text)
    sida = 0
    
    group1 = ['neumonía recurrente', 
              'bacteriemia recurrente por salmonella', 
              'tuberculosis pulmonar', 
              'tuberculosis extrapulmonar', 
              'micobacterias atípicas diseminadas', 
              'candidiasis esofágica', 
              'candidiasis bronquial', 
              'candidiasis traqueal', 
              'candidiasis pulmonar', 
              'neumonía por pneumocystis jirovecii', 
              'neumonía por pneumocystis carinii', 
              'histoplasmosis extrapulmonar', 
              'coccidioidomicosis extrapulmonar', 
              'criptococosis extrapulmonar', 
              'criptosporidiosis', 
              'infecciones por virus del herpes simple', 
              'infecciones por citomegalovirus', 
              'toxoplasmosis cerebral', 
              'leucoencefalopatía multifocal progresiva', 
              'sarcoma de kaposi', 
              'linfomas', 
              'carcinoma de cérvix uterino invasivo']
    
    group2 = ["Angiomatosis bacilar",
           "Candidiasis orofaringea", "muguet",
           "Candidiasis vulvovaginal; persistente, frecuente, o que no responde al tratamiento",
           "Displasia cervical (moderada o severa)/carcinoma cervical in situ",
           "Síndrome constitucional, fiebre persistente (38.5°C) y/o diarrea crónica de >1 mes de duración (COMBINACIÓN)",
           "Leucoplasia oral vellosa",
           "Herpes zoster, al menos 2 episodios distintos o más de un dermatoma",
           "Púrpura trombocitopénica idiopática",
           "Listeriosis",
           "Enfermedad pélvica inflamatoria, abscesos tuboováricos",
           "Neuropatía periférica"]

    group3 = ["Cáncer de pulmón primario",
           "Meningitis linfocítica",
           "Psoriasis grave o atípica",
           "Síndrome de Guillain-Barré",
           "Mononeuritis",
           "Demencia subcortical",
           "Esclerosis múltiple",
           "Insuficiencia renal crónica idiopática",
           "Hepatitis A",
           "Neumonía adquirida en la comunidad",
           "Dermatitis atópica"]

    
    # Buscamos enfermedades definitorias de sida (Grupo 1)
    for symptom in symptoms:
        if symptom in group1:
            sida += 4.5
    
    # Buscamos enfermedades indicadoras de sida (Grupo 2)
    for symptom in symptoms:
        if symptom in group2:
            sida += 3.5
    
    # Buscamos otras enfermedades indicadoras de sida (Grupo 3)
    for symptom in symptoms:
        if symptom in group3:
           sida += 2.5
    
    return 'Probabilidad de padecer sida: ' + str(sida *20) + '% \n Sintomas: ' + str(symptoms)

    
def testManual():
    text1 = "El paciente se presentó con fiebre y fatiga. Se sospecha que puede tener VIH debido a sus antecedentes."
    print(detect_sida(text1)) # VIH negativo

    text2 = "La paciente tiene VIH y presenta dolor de cabeza, fatiga y sudores nocturnos, Candidiasis orofaringea."
    print(detect_sida(text2)) # VIH positivo (síntomas relevantes)

    text3 = "No hay indicios de VIH en el paciente, pero presenta pérdida de peso y sudores nocturnos, fiebre, dolor de cabeza y fatiga, tuberculosis pulmonar."
    print(detect_sida(text3)) # VIH positivoo (definitorio)

    text4 = "El paciente africano se presentó con dolor de cabeza y fiebre. Se sospecha de VIH."
    print(detect_sida(text4)) # VIH negativo
    
def testNota1():
    text = get_text_from_file('datasets')
    print(detect_sida(text))

testNota1()
