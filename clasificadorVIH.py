from transformers import pipeline
import os
import re
import spacy

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

            # Agregar síntoma a la lista si no está repetido
            if symptom not in symptoms:
                symptoms.append(symptom)
            i = j
        else:
            i += 1

    # Eliminar espacios en blanco innecesarios
    for i in range(len(symptoms)):
        symptoms[i] = symptoms[i].strip()

    return symptoms


def group1(symptoms):
    indicators = ['neumonía recurrente', 
            'bacteriemia recurrente por salmonella', ''
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
            'herpes simple', 
            'citomegalovirus', 
            'toxoplasmosis cerebral', 
            'leucoencefalopatía multifocal progresiva', 
            'sarcoma de kaposi', 
            'linfomas', 'linfoma'
            'carcinoma de cérvix uterino invasivo']
    match = []
    # Buscamos enfermedades definitorias de sida (Grupo 1)
    for symptom in symptoms:
        if symptom in indicators:
            match.append(symptom)
    return match

def group2(symptoms):
    indicators = [
    "angiomatosis bacilar",
    "candidiasis orofaringea",
    "muguet",
    "candidiasis vulvovaginal",
    "displasia cervical"
    "carcinoma cervical",
    "síndrome constitucional",
    "fiebre persistente",
    "diarrea crónica ", # de más de un mes de duración, en combinación con la fiebre
    "leucoplasia oral vellosa",
    "herpes zoster",
    "púrpura trombocitopénica idiopática",
    "listeriosis",
    "enfermedad pélvica inflamatoria", 
    "abscesos tuboováricos",
    "neuropatía periférica"
]

    match = []
    # Buscamos enfermedades indicadoras de sida (Grupo 2)
    for symptom in symptoms:
        if symptom in indicators:
            match.append(symptom)
    return match

def group3(symptoms):
    indicators = indicators = [
    "cáncer de pulmón primario",
    "meningitis linfocítica",
    "psoriasis grave o atípica",
    "síndrome de guillain-barré",
    "mononeuritis",
    "demencia subcortical",
    "esclerosis múltiple",
    "insuficiencia renal crónica idiopática",
    "hepatitis a",
    "neumonía adquirida en la comunidad",
    "dermatitis atópica"
]

    match = []
    # Buscamos otras enfermedades indicadoras de sida (Grupo 3)
    for symptom in symptoms:
        if symptom in indicators:
            match.append(symptom)
    return match

def group4(text):
    pattern = r"(\d{1,2}) años"
    age = 0
    points = 0
    
    match = re.search(pattern, text)
    if match:
        age = int(match.group(1)) # Almacena la primera aparición del patrón
        
    if age >= 20 and age <= 24:
        points += 3.2
    elif age >= 25 and age <= 29:
        points += 3.5
    elif age >= 30 and age <= 34:
        points += 3.3
    elif age >= 35 and age <= 39:
        points += 3.3
    elif age >= 40 and age <= 44:
        points += 2.8
    elif age >= 45 and age <= 49:
        points += 2.8
    elif age >= 50: 
        points += 2.8
    
    # Expresión regular para reconocer "homosexual", "homosexualidad", "hombre que tiene sexo con hombres", "HSH" y sus variantes
    pattern = r"(homosexual|homosexualidad|hombre que tiene sexo con hombres|hsh)"
    # Buscar la expresión regular en el texto
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        points += 4.8
        
    # Expresión regular para reconocer "trabajo sexual", "trabajadora sexual", "trabajador sexual" y sus variantes
    pattern = r"(trabajo sexual|trabajadora sexual|trabajador sexual|prostitución|prostitut[oa])"
    # Buscar la expresión regular en el texto
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        points += 5
    
    # Expresión regular para reconocer "violencia sexuak", "violación" y sus variantes
    pattern = r"(violencia sexual|violación|violad[oa])"
    # Buscar la expresión regular en el texto
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        points += 4.3
    
    # Expresión regular para reconocer "embarazo", "embarazada" y sus variantes
    pattern = r"(embarazad[oa]|embarazo)"
    # Buscar la expresión regular en el texto
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        points += 3.2
    
    return points

def group5(text):
    nlp = spacy.load("es_core_news_sm")
    # Aplicar el ner al texto
    doc = nlp(text)
    country = ""
    # Iterar sobre las entidades reconocidas
    for ent in doc.ents:
    # Si la entidad es de tipo LOC (localización) y su etiqueta es GPE (entidad geopolítica)
        if ent.label_ == "LOC":
            country = ent.text
            break

    group1 = ['australia', 'azerbaiyán', 'bahamas', 'benín', 'botsuana', 'burkina faso', 'burundi', 'camboya', 'camerún', 'costa de marfil', 
              'dinamarca', 'yibuti', 'eritrea', 'estonia', 'etiopía', 'alemania', 'haití', 'india', 'italia', 'japón', 'kenia', 'lesoto', 'luxemburgo', 
              'malaui', 'nepal', 'países bajos', 'nueva zelanda', 'noruega', 'portugal', 'ruanda', 'santo tomé y príncipe', 'singapur', 'eslovenia', 
              'sudáfrica', 'españa', 'suiza', 'tailandia', 'togo', 'trinidad y tobago', 'ucrania', 'estados unidos', 'venezuela', 'vietnam', 
              'zambia', 'zimbabue']

    group2 = ['argentina', 'barbados', 'bielorrusia', 'belice', 'república centroafricana', 'chad', 'chile', 'colombia', 'comoras', 'croacia', 
              'chipre', 'república democrática del congo', 'ecuador', 'el salvador', 'esuatini', 'francia', 'gabón', 'ghana', 'global', 'grecia', 
              'guatemala', 'honduras', 'islandia', 'indonesia', 'irán', 'irlanda', 'jamaica', 'liberia', 'malí', 'méxico', 'marruecos', 'mozambique',
              'myanmar', 'namibia', 'nicaragua', 'níger', 'nigeria', 'rumanía', 'senegal', 'somalia', 'sri lanka', 'uganda', 'república unida de tanzania']

    group3 = ['albania', 'argelia', 'angola', 'armenia', 'baréin', 'bangladés', 'bután', 'bolivia', 'brasil', 'bulgaria', 'cabo verde', 
              'congo', 'costa rica', 'cuba', 'república dominicana', 'guinea ecuatorial', 'gambia', 'georgia', 'guinea', 'guinea-bisáu', 
              'guyana', 'jordania', 'kazajistán', 'kirguistán', 'república democrática popular lao', 'letonia', 'líbano', 'libia', 'lituania',
              'malasia', 'mauritania', 'mauricio', 'mongolia', 'montenegro', 'omán', 'papúa nueva guinea', 'paraguay', 'perú', 'catar', 
              'república de moldova', 'arabia saudita', 'serbia', 'sierra leona', 'eslovaquia', 'sudán del sur', 'sudán', 'surinam', 
              'república árabe siria', 'tayikistán', 'timor oriental', 'túnez', 'uruguay', 'uzbekistán']

    group4 = ['afganistán', 'fiyi', 'egipto', 'madagascar', 'pakistán', 'filipinas', 'yemen']

    group5 = ['austria', 'bélgica', 'bosnia y herzegovina', 'brunéi', 'canadá', 'china', 'chequia', 'finlandia', 'hungría', 'irak', 'israel', 
              'kuwait', 'maldivas', 'malta', 'macedonia del norte', 'panamá', 'polonia', 
              'corea','federación de rusia', 'suecia', 'turquía', 'turkmenistán', 'emiratos árabes unidos', 'reino unido', 'venezuela']


    if country in group1:
        return 1.3
    elif country in group2:
        return 2.3
    elif country in group3:
        return 3.2
    elif country in group4:
        return 3.8
    elif country in group5:
        return 1.8
    else: 
        return 1.3 # Si no se encuentra el país, se asume que es España

def group6(symptoms):

    indicators = {
    'úlceras mucocutáneas': 3.7,
    'úlceras orales': 3.7,
    'úlceras labiales': 3.7,
    'úlceras yugales': 3.7,
    'úlceras bucales': 3.7,
    'úlceras faríngeas': 3.7,
    'úlceras anales': 3.7,
    'úlceras genitales': 3.7,
    'exantema': 2.8,
    'rash cutáneo': 2.8,
    'erupción cutánea': 2.8,
    'mialgias': 1.7,
    'artralgias': 1.7,
    'anorexia': 2.7,
    'pérdida de peso injustificada': 2.7,
    'fiebre': 2.8,
    'manifestaciones graves a nivel del sistema nervioso central': 3.5,
    'meningitis': 3.5,
    'encefalitis': 3.5,
    'fatiga': 2,
    'malestar': 2,
    'astenia': 2,
    'cefalea': 1.7,
    'linfadenopatía periférica': 3.5,
    'adenopatías': 3.5,
    'faringitis': 2.5,
    'alteraciones gastrointestinales': 2.8,
    'diarrea': 2.8,
    'mononucleosis': 4.8,
    'síndrome mononucleósido': 4.8
}

    points = 0
    # Buscamos enfermedades definitorias de sida (Grupo 1)
    for symptom in symptoms:
        if symptom in indicators:
            points += indicators[symptom]
    return points

def group7(symptoms, text):
    points = 0
    if 'leucopenia' in symptoms or 'leucocitos <3500 cel/ml' in text:
        points += 3.3
    if 'trombopenia' in symptoms or 'plaquetas <100000 cel/ml' in text:
        points += 2.5
    if 'linfopenia <500' in text:
        points += 0.7
    if 'hipergammaglobulinemia' in symptoms:
        points += 0.5

    return points

def group8(symptoms):
    match = []
    diseases = [
    'hepatitis b', 'hbsag +',
    'hepatitis c' , 'ac antivhc +',
    'serología lúes','sífilis',
    'exudado rectal positivo',
    'exudado uretral positivo',
    'exudado cuello uterino positivo',
    'gonococo',
    'chlamydia'
]
    for symptom in symptoms:
        if symptom in diseases:
            match.append(symptom)
    return match

def detect_vih(text): 
    text = text.lower()
    symptoms = extract_symptoms(text)
    vih = 0
    
    symptomsg1 = group1(symptoms) # enfermedades definitorias de sida
    symptomsg2 = group2(symptoms) # enfermedades indicadoras de sida
    symptomsg3 = group3(symptoms) # otras engfermedades indicadoras de sida
    sociodemographic = group4(text)
    country = group5(text)
    symptoms6 = group6(symptoms) # signos y síntomas de infección aguda por VIH
    laboratory = group7(symptoms, text) # alteraciones de laboratorio
    std = group8(symptoms) # enfermedades de transmisión sexual
    
    vih = len(symptomsg1) * (4.5 * 2) + len(symptomsg2) * 3.5 + len(symptomsg3) * 2.5 + sociodemographic + country + symptoms6 + laboratory + len(std) * 4.3
    
    
    # print('Probabilidad de padecer sida: ' + str(sida *10) + '% \nSíntomas del grupo 1: ' + str(symptomsg1) + '\nSíntomas del grupo 2: ' + str(symptomsg2) + '\nSíntomas del grupo 3: ' + str(symptomsg3))
    # print('Sintomas totales: ' + str(symptoms))
    print(str(vih))
    if vih >= 10:
        return True
    else :
        return False
    
text = get_text_from_file('datasets', 0)
detect_vih(text)