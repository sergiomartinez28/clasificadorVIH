import re
import subprocess
import os

from text_processor import TextProcessor

def find_sentences(text, symptom):
    # Expresión regular para reconocer frases que contienen el síntoma
    pattern = r"([^.|\n]*" + re.escape(symptom) + "[^.|\n]*(?:\.|\n))"
    
    # Buscar la expresión regular en el texto
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    else:
        return ""

def preparar_archivo_negex(sintomas, texto):
    """
    Prepara el archivo de entrada para NegEx-MES con los síntomas y las frases extraídas.
    
    :param sintomas: Lista de síntomas para buscar en el texto.
    :param texto: Texto completo donde buscar los síntomas.
    :param input_path: Ruta al archivo de entrada que NegEx-MES leerá.
    """
    input_path = "../in/in.txt"
    with open(input_path, "w", encoding="utf-8") as file:
        for i, sintoma in enumerate(sintomas):
            frase = find_sentences(texto, sintoma)
            if frase:  # Asegurarse de que la frase no esté vacía
                # Escribe el síntoma y la frase en el formato esperado por NegEx
                file.write(f"{i}\t{sintoma}\t\"{frase}\"\n")

def ejecutar_negex(config_path="../config_files/", input_path="../in/in.txt", output_path="../out/callKit.result"):
    """
    Ejecuta NegEx-MES con un texto de entrada dado.


    :param config_path: Ruta a los archivos de configuración.
    :param input_path: Ruta al archivo de entrada que NegEx-MES leerá.
    :param output_path: Ruta al archivo de salida que NegEx-MES generará.
    """


    # Construir el comando para ejecutar NegEx-MES
    command = [
        "java", "-jar", "smn.jar",
        "-displayon", "true",
        "-language", "SPANISH",
        "-answerOptionYes", "true",
        "-isOuputFileGenerated", "true",
        "-lemmaConfigFiles", "false",
        "-routeConfigFiles", config_path,
        "-routeInTextFile", input_path,
        "-routeOutTextFile", output_path
    ]

    # Ejecutar NegEx-MES
    subprocess.run(command, check=True)

    # Leer y mostrar el resultado de la ejecución
    
    if os.path.exists(output_path):
        with open(output_path, "r") as file:
            result = file.read()
            print("Resultado de NegEx-MES:")
            print(result)
    else:
        print("No se pudo encontrar el archivo de salida.")


text_processor = TextProcessor()
texto = text_processor.get_text_from_file('datasets', 0)
sintomas = text_processor.extract_symptoms(texto)
for sintoma in sintomas:
    frase = find_sentences(texto, sintoma)
    #print(f"Sintoma: {sintoma} \n{frase}")

os.chdir("NegEx-MES-master/smn/main")
preparar_archivo_negex(sintomas, texto)
ejecutar_negex()
