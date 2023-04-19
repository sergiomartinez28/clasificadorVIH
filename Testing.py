import nltk

# Descarga los recursos necesarios de NLTK
nltk.download('punkt')
nltk.download('stopwords')

# Define una función para clasificar el texto
def clasificar_texto(texto):
    # Tokeniza el texto en palabras
    palabras = nltk.word_tokenize(texto.lower())
    
    # Elimina las palabras comunes que no aportan significado (stopwords)
    stopwords = set(nltk.corpus.stopwords.words('spanish'))
    palabras = [palabra for palabra in palabras if palabra not in stopwords]
    
    # Busca la aparición de la palabra "VIH" en el texto
    if 'vih' in palabras:
        return 'VIH presente'
    else:
        return 'VIH no presente'

# Ejemplo de uso
texto_ejemplo = 'El cancer es una enfermedad grave que afecta a millones de personas en todo el mundo.'
# print(clasificar_texto(texto_ejemplo))  # Debería imprimir "VIH presente"


import spacy

# Descargar el modelo pre-entrenado de spaCy para el reconocimiento de entidades médicas
nlp = spacy.load('es_dep_news_trf')
import es_dep_news_trf
nlp = es_dep_news_trf.load()

# Definir una serie de reglas para la detección del VIH
def detectar_VIH(texto):
    doc = nlp(texto)
    
    # Buscar entidades nombradas relacionadas con síntomas del VIH
    sintomas = ['fiebre', 'dolor de cabeza', 'sudores nocturnos', 'pérdida de peso', 'diarrea', 'fatiga', 'dolor de garganta']
    sintomas_encontrados = [entidad.text for entidad in doc.ents if entidad.label_ == 'SINTOMA' and entidad.text.lower() in sintomas]
    
    # Buscar entidades nombradas relacionadas con pruebas del VIH
    pruebas = ['ELISA', 'Western Blot', 'carga viral', 'CD4', 'PCR']
    pruebas_encontradas = [entidad.text for entidad in doc.ents if entidad.label_ == 'PRUEBA' and entidad.text in pruebas]
    
    # Buscar entidades nombradas relacionadas con el VIH
    VIH = [entidad.text for entidad in doc.ents if entidad.label_ == 'VIH']
    
    # Buscar entidades nombradas genéricas para contextualizar la información
    paises = [entidad.text for entidad in doc.ents if entidad.label_ == 'LOC' and entidad.text.lower() in ['españa', 'méxico', 'argentina']]
    
    # Aplicar las reglas para determinar si el texto contiene indicios de VIH
    if VIH or sintomas_encontrados or (pruebas_encontradas and any(pais in paises for pais in ['España', 'México'])):
        return 'VIH presente'
    else:
        return 'VIH no presente'

# Ejemplo de uso
texto_ejemplo = 'La paciente presenta fiebre, dolor de cabeza y sudores nocturnos. Se le realizó una prueba de ELISA que dio positivo. Además, viajó a México hace dos meses.'
print(detectar_VIH)

