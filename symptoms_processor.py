import re
import spacy

class SymptomsProcessor:
    def __init__(self): 
        self.nlp = spacy.load("es_core_news_sm")
    
    def group1(symptoms):
        indicators = {
            'neumonía recurrente': 4.2,
            'bacteriemia recurrente por salmonella': 4.5,
            'tuberculosis pulmonar': 4.5,
            'tuberculosis extrapulmonar': 4.5, #
            'micobacterias atípicas diseminadas': 4.8,
            'candidiasis esofágica': 4.5,
            'candidiasis bronquial': 4.5, 
            'candidiasis traqueal': 4.5, 
            'candidiasis pulmonar': 4.5, 
            'neumonía por pneumocystis jirovecii': 5.0,
            'neumonía por pneumocystis carinii': 5.0, 
            'histoplasmosis extrapulmonar': 4.8,
            'coccidioidomicosis extrapulmonar': 4.7,
            'criptococosis extrapulmonar': 4.8,
            'criptosporidiosis': 4.8,
            'herpes simple': 4.3,
            'citomegalovirus': 4.7,
            'toxoplasmosis cerebral': 4.8,
            'leucoencefalopatía multifocal progresiva': 4.7,
            'sarcoma de kaposi': 5.0,
            'linfoma de burkitt': 4.8,
            'linfoma cerebral primario': 4.8,
            'linfoma inmunoblástico': 4.8,
            'carcinoma de cérvix uterino invasivo': 4.5
        }
        match = []
        # Buscamos enfermedades definitorias de sida (Grupo 1)
        for symptom in symptoms:
            if symptom in indicators:
                match.append(symptom)
        return match

    def group2(symptoms):
        indicators = {
            'angiomatosis bacilar': 3.7,
            'candidiasis orofaringea': 3.5,
            'muguet': 3.5,
            'candidiasis vulvovaginal': 3.2,
            'displasia cervical': 3.7,
            'carcinoma cervical': 3.7,
            'síndrome constitucional': 4.0,
            'fiebre persistente': 4.0,
            'diarrea crónica': 4.0,
            'leucoplasia oral vellosa': 3.8,
            'herpes zoster': 3.7,
            'púrpura trombocitopénica idiopática': 3.0,
            'listeriosis': 2.8,
            'enfermedad pélvica inflamatoria': 3.3,
            'abscesos tuboováricos': 3.3,
            'neuropatía periférica': 3.0
        }

        match = []
        # Buscamos enfermedades indicadoras de sida (Grupo 2)
        for symptom in symptoms:
            if symptom in indicators:
                match.append(symptom)
        return match

    def group3(symptoms):
        indicators = {
            'angiomatosis bacilar': 3.7,
            'candidiasis orofaringea': 3.5,
            'muguet': 3.5,
            'candidiasis vulvovaginal': 3.2,
            'displasia cervical': 3.7,
            'carcinoma cervical': 3.7,
            'síndrome constitucional': 4.0,
            'fiebre persistente': 4.0,
            'diarrea crónica': 4.0,
            'leucoplasia oral vellosa': 3.8,
            'herpes zoster': 3.7,
            'púrpura trombocitopénica idiopática': 3.0,
            'listeriosis': 2.8,
            'enfermedad pélvica inflamatoria': 3.3,
            'abscesos tuboováricos': 3.3,
            'neuropatía periférica': 3.0
        }

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
        detected_symptoms = []
        # Buscamos enfermedades definitorias de sida (Grupo 1)
        for symptom in symptoms:
            if symptom in indicators:
                detected_symptoms.append(symptom)
                points += indicators[symptom]
        return detected_symptoms, points

    def group7(symptoms, text):
        detected_symptoms = []
        points = 0

        if 'leucopenia' in symptoms or 'leucocitos <3500 cel/ml' in text:
            points += 3.3
            detected_symptoms.append('leucopenia' if 'leucopenia' in symptoms else 'leucocitos <3500 cel/ml')

        if 'trombopenia' in symptoms or 'plaquetas <100000 cel/ml' in text:
            points += 2.5
            detected_symptoms.append('trombopenia' if 'trombopenia' in symptoms else 'plaquetas <100000 cel/ml')

        if 'linfopenia <500' in text:
            points += 0.7
            detected_symptoms.append('linfopenia <500')

        if 'hipergammaglobulinemia' in symptoms:
            points += 0.5
            detected_symptoms.append('hipergammaglobulinemia')

        return detected_symptoms, points

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
            
    def detect_vih(self, text, symptoms): 
        text = text.lower()

        vih = 0
        symptomsg1 = self.group1(symptoms) # enfermedades definitorias de sida
        symptomsg2 = self.group2(symptoms) # enfermedades indicadoras de sida
        symptomsg3 = self.group3(symptoms) # otras engfermedades indicadoras de sida
        p4 = self.group4(text)
        p5 = self.group5(text)
        symptoms6, p6 = self.group6(symptoms) # signos y síntomas de infección aguda por VIH
        symptoms7, p7 = self.group7(symptoms, text) # alteraciones de laboratorio
        std = self.group8(symptoms) # enfermedades de transmisión sexual
        
        symptons_filtered = symptomsg1 + symptomsg2 + symptomsg3 + symptoms6 + symptoms7 + std
    
        vih += p4 + p5 + p6 + p7
        print(vih)
        return vih >= 8