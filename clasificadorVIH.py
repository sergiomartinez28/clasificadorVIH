import os
import torch 
from transformers import AutoTokenizer, AutoModelForTokenClassification

# Cargar el modelo y el tokenizer
tokenizer = AutoTokenizer.from_pretrained("lcampillos/roberta-es-clinical-trials-ner")
model = AutoModelForTokenClassification.from_pretrained("lcampillos/roberta-es-clinical-trials-ner")

# Ajustar la longitud maxima permitida por el modelo
tokenizer.model_max_length = 1500

# Función para obtener ficheros de texto de una carpeta
def obtain_text(folder_path):
    files = os.listdir(folder_path)
    texts = []
    for file in files:
        if file.endswith(".txt"):
            file_path = os.path.join(folder_path, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
                texts.append(text)
    return texts

# Función para obtener el primer fichero de texto de una carpeta
def obtain_first(folder_path):
    texts = obtain_text(folder_path)
    return texts[0] 
    

def extract_symptoms(text):
    symptoms = []
    # Tokenizar el texto y ajustar la longitud máxima permitida
    inputs = tokenizer.encode_plus(text, add_special_tokens=True, return_tensors="pt", max_length=1500, truncation=True)
    
    # Obtener la salida del modelo
    outputs = model(inputs['input_ids'], attention_mask=inputs['attention_mask'])
    
    # Obtener los resultados de la tarea NER
    predictions = torch.argmax(outputs.logits, dim=-1)
    tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
    
    i = 0
    while i < len(predictions):
        if predictions[i] == 1:  # B-DISO
            # Buscar entidades adyacentes con el mismo prefijo IOB
            prefix = 'B'
            j = i + 1
            while j < len(predictions) and tokens[j].startswith('I'):
                j += 1
            # Fusionar las entidades adyacentes en una sola
            symptom = ' '.join(tokens[i:j]).replace('Ġ', ' ')
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
        return "VIH positivo (síntomas relevantes) [" + str(symptoms) + "]"
    else:
        return "VIH negativo [" + str(symptoms) + "]"
    
# Este es el que hay que usar para sacar todos pero voy a testear con el otro
# texts = obtain_text('datasets')

text = obtain_first('datasets')
extract_symptoms(text)

# text1 = "El paciente se presentó con fiebre y fatiga. Se sospecha que puede tener VIH debido a sus antecedentes."
# print(classify_text(text1)) # VIH negativo

#text2 = "La paciente tiene VIH y presenta dolor de cabeza, fatiga y sudores nocturnos."
#print(classify_text(text2)) # VIH positivo (síntomas relevantes)

#text3 = "No hay indicios de VIH en el paciente, pero presenta pérdida de peso y sudores nocturnos, fiebre, dolor de cabeza y fatiga."
#print(classify_text(text3)) # VIH negativo

text4 = "El paciente africano se presentó con dolor de cabeza y fiebre. Se sospecha de VIH."
#print(classify_text(text4)) # VIH negativo
