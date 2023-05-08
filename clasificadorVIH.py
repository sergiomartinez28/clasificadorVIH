from transformers import pipeline
import os
import re

ner_pipeline = pipeline("ner", model="lcampillos/roberta-es-clinical-trials-ner", tokenizer="lcampillos/roberta-es-clinical-trials-ner")

# Funcion para obtener el texto del primer fichero de una carpeta
def get_text_from_file(path, number):
    files = os.listdir(path)
    with open(os.path.join(path, files[number]), 'r', encoding='utf-8') as f:
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


def analyze_text(text):
    # Convertir el texto a minúsculas
    text = text.lower()
    

    # Expresión regular para reconocer "positivo", "VIH" y sus variantes
    pattern = r"(seropositivo|VIH estadio|VIH estadío|infectado de VIH|infectado con VIH|infección de VIH|infección con VIH|infección por VIH|infección VIH diagnosticada|VIH\+|VIH \+|HIV\+|HIV \+|VIH positivo|VIH positiva|positivo en VIH|positivo para VIH|síndrome de inmunodeficiencia adquirida)"
    # Buscar la expresión regular en el texto
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        # Si se encuentra la expresión regular, el resultado es positivo
        return True
    
    # Expresión regular para reconocer "antecedentes", "VIH" y sus variantes
    pattern = r"(antecedentes|historial|previamente diagnosticado|diagnóstico previo|diagnóstico) .{0,20} (VIH|vih|HIV|hiv|SIDA|sida)"
    # Buscar la expresión regular en el texto
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        # Si se encuentra la expresión regular, el resultado es positivo
        return True
    
    # Expresión regular para reconocer "en tratamiento", "SIDA" y sus variantes
    pattern = r"(en tratamiento|bajo tratamiento|recibe tratamiento) .* (SIDA|síndrome de inmunodeficiencia adquirida|antirretroviral)"
    # Buscar la expresión regular en el texto
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        # Si se encuentra la expresión regular, el resultado es positivo
        return True
    
    # Si no se encuentra ninguna expresión regular, el resultado es negativo
    return False



def detect_sida(text): 
    
    if analyze_text(text):
       return True
    else: 
        symptoms = extract_symptoms(text)
        sida = 0
        
        symptomsg1 = []
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
        
        symptomsg2 = []
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

        symptomsg3 = []
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
                symptomsg1.append(symptom)
        
        # Buscamos enfermedades indicadoras de sida (Grupo 2)
        for symptom in symptoms:
            if symptom in group2:
                sida += 3.5
                symptomsg2.append(symptom)
        
        # Buscamos otras enfermedades indicadoras de sida (Grupo 3)
        for symptom in symptoms:
            if symptom in group3:
                sida += 2.5
                symptomsg3.append(symptom)
        
        print('Probabilidad de padecer sida: ' + str(sida *20) + '% \nSíntomas del grupo 1: ' + str(symptomsg1) + '\nSíntomas del grupo 2: ' + str(symptomsg2) + '\nSíntomas del grupo 3: ' + str(symptomsg3) + '\nSintomas totales: ' + str(symptoms))
        if sida >= 4.5:
            return True
        else :
            return False


    
    
def testNota1():
    text = get_text_from_file('datasets', 29)
    print(detect_sida(text))

# Funcion que hace una lista con los ficheros de un directorio
def get_files_from_dir(dir):
    files = []
    for file in os.listdir(dir):
        files.append(file)
    return files


    
testNota1()
