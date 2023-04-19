# Programa que procesa textos de un directorio y los clasifica en positivo o negativo en función de la presencia de síntomas
import os
from transformers import AutoTokenizer, AutoModelForTokenClassification

tokenizer = AutoTokenizer.from_pretrained("lcampillos/roberta-es-clinical-trials-ner")
model = AutoModelForTokenClassification.from_pretrained("lcampillos/roberta-es-clinical-trials-ner")

# Función para leer los textos de un directorio
def read_texts(directory):
    texts = []
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r') as f:
            texts.append(f.read())
    return texts

# Usar modelo de HugginFace para extraer entidades
def extract_entities(text):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    predictions = outputs.logits.argmax(dim=-1)
    entities = tokenizer.convert_ids_to_tokens(predictions[0].tolist())
    return entities