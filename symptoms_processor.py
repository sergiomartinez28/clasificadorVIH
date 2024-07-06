import re
import spacy

class SymptomsProcessor:
    def __init__(self): 
        self.nlp = spacy.load("es_core_news_sm")
    
    def group1(self, symptoms):
        indicators = {
            'sindrome de inmunodeficiencia adquirida': 5.0,
            'neumonía recurrente': 4.2,
            'bacteriemia recurrente por salmonella': 4.5,
            'tuberculosis pulmonar': 4.5,
            'tuberculosis extrapulmonar': 4.5, 
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
        matches = set()
        for symptom_received in symptoms:
            for indicator_symptom, score in indicators.items():
                if indicator_symptom.lower() in symptom_received.lower():
                    matches.add((indicator_symptom, score))
                    break
        return matches

    def group2(self, symptoms):
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
        matches = set()
        for symptom_received in symptoms:
            for indicator_symptom, score in indicators.items():
                if indicator_symptom.lower() in symptom_received.lower():
                    matches.add((indicator_symptom, score))
                    break
        return matches

    def group3(self, symptoms):
        indicators = {
            'cáncer de pulmón primario': 2.5,
            'meningitis linfocítica': 3.2,
            'psoriasis grave': 2.8,
            'psoriasis atípica': 2.8,
            'síndrome de guillain-barré': 2.3,
            'mononeuritis': 2.2,
            'demencia subcortical': 2.5,
            'esclerosis múltiple': 2.5,
            'insuficiencia renal crónica idiopática': 2.0,
            'hepatitis a': 2.7,
            'neumonía adquirida en la comunidad': 2.5,
            'dermatitis atópica': 2.2
        }

        matches = set()
        for symptom_received in symptoms:
            for indicator_symptom, score in indicators.items():
                if indicator_symptom.lower() in symptom_received.lower():
                    matches.add((indicator_symptom, score))
                    break
        return matches

    def group4(self, text):
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

    def group5(self, text):
        nlp = self.nlp
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

    def group6(self, symptoms):

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
            'faringitis aguda': 2.5,
            'alteraciones gastrointestinales': 2.8,
            'diarrea': 2.8,
            'mononucleosis': 4.8,
            'síndrome mononucleósido': 4.8
        }

        matches = set()
        for symptom_received in symptoms:
            for indicator_symptom, score in indicators.items():
                if indicator_symptom.lower() in symptom_received.lower():
                    matches.add((indicator_symptom, score))
                    break
        return matches

    def group7(self, symptoms, text):
        indicators = {
            'leucopenia': 3.3,
            'trombopenia': 2.5,
            'linfopenia <500': 0.7,
            'hipergammaglobulinemia': 0.5
        }

        # Text checks for additional conditions not directly mentioned as symptoms
        text_indicators = {
            'leucocitos': 'leucopenia',  
            'plaquetas': 'trombopenia' 
        }

        matches = []

        # Check for symptoms directly
        for symptom in symptoms:
            if symptom in indicators:
                matches.append((symptom, indicators[symptom]))

        # Check for conditions described in the text
        for text_condition, equivalent_symptom in text_indicators.items():
            # Uso de regex para encontrar y comparar el número específico mencionado
            regex_pattern = fr'{text_condition}\s*<\s*(\d+)\s*cel/ml'
            match = re.search(regex_pattern, text, re.IGNORECASE)
            if match:
                count = int(match.group(1))
                if text_condition == 'leucocitos' and count < 3500:
                    if equivalent_symptom not in [symptom for symptom, _ in matches]:
                        matches.append((equivalent_symptom, indicators[equivalent_symptom]))
                elif text_condition == 'plaquetas' and count < 100000:
                    if equivalent_symptom not in [symptom for symptom, _ in matches]:
                        matches.append((equivalent_symptom, indicators[equivalent_symptom]))

        return matches

    def group8(self, symptoms):
        indicators = {
            'hepatitis b': 4,
            'hbsag +': 4,
            'hepatitis c': 4.2,
            'ac antivhc +': 4.2,
            'serología lúes': 4.3,
            'sífilis': 4.3,
            'exudado rectal': 4.3,
            'exudado uretral': 4.3,
            'exudado cuello uterino positivo': 4.2,
            'gonococo': 4.3,
            'chlamydia': 4.3, 
            'clamidia': 4.3
        }
        matches = set()
        for symptom_received in symptoms:
            for indicator_symptom, score in indicators.items():
                if indicator_symptom.lower() in symptom_received.lower():
                    matches.add((indicator_symptom, score))
                    break
        return matches
    
    def extract_vih_symptoms(self,symtomps, text):
        match = []
        # Revisar primero si hay indicadores en group3
        group3_matches = self.group3(symtomps)
        if group3_matches:
            # Si hay indicadores en group3, retornar una lista vacía
            return match
        
        #match.extend(self.group1(symtomps)) # enfermedades definitorias de sida
        match.extend((indicator, score * 2) for indicator, score in self.group1(symtomps))
        match.extend(self.group2(symtomps)) # enfermedades indicadoras de sida
        #match.extend(self.group3(symtomps)) # otras engfermedades indicadoras de sida
        
        match.extend(self.group6(symtomps)) # signos y síntomas de infección aguda por VIH
        match.extend(self.group7(symtomps, text)) # signos y síntomas de infección aguda por VIH
        match.extend(self.group8(symtomps)) # enfermedades de transmisión sexual
        return match

    def score_group1(self, symptoms):
        match = []
        match.extend(self.group1(symptoms))
        score = self.calculate_total_score(match)
        return match, score
    
    def score_group2(self, symptoms):
        match = []
        match.extend(self.group2(symptoms))
        score = self.calculate_total_score(match)
        return match, score
    
    def score_group3(self, symptoms):
        match = []
        match.extend(self.group3(symptoms))
        score = self.calculate_total_score(match)
        return match, score
    
    def score_group6(self, symptoms):
        match = []
        match.extend(self.group6(symptoms))
        score = self.calculate_total_score(match)
        return match, score
    
    def score_group7(self, symptoms, text):
        match = []
        match.extend(self.group7(symptoms, text))
        score = self.calculate_total_score(match)
        return match, score 
    
    def score_group8(self, symptoms):
        match = []
        match.extend(self.group8(symptoms))
        score = self.calculate_total_score(match)
        return match, score
    
    def calculate_total_score(self, tuples_list):
        """
        Calculates the total score by summing the scores of each symptom.

        :param tuples_list: List of tuples, where each tuple contains a symptom and its corresponding score.
        :return: Total score as a float.
        """
        total_score = sum(score for symptom, score in tuples_list)
        return total_score
            
    def detect_vih(self, text, symptoms, threshold): 
        text = text.lower()
        vih = 0
        vih_indicators = self.extract_vih_symptoms(symptoms, text)
        indicators_score = self.calculate_total_score(vih_indicators) # score estimated from symptoms (groups 1, 2, 3, 6, 7, 8)
        p4 = self.group4(text) # score estimated from sociodemographic indicators
        p5 = self.group5(text) # score estimated from country of origin

        vih += indicators_score + p4 * 0.5 + p5 
        return vih >= threshold, vih