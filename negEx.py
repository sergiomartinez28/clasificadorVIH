import os
import re
import subprocess

class NegEx:
    def __init__(self, config_path="../config_files/", input_path="../in/in.txt", output_path="../out/callKit.result"):
        self.config_path = config_path
        self.input_path = input_path
        self.output_path = output_path

    def find_sentences(self, text, symptom):
        """
        Recognizes sentences containing the symptom within the text.
        """
        pattern = r"([^.|\n]*" + re.escape(symptom) + r"[^.|\n]*)(?:\.|\n)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            sentence = match.group(1).strip()
            # Comprueba si existe una negación después de la lista de síntomas
            if "negativo" in sentence:
                return ""
            return sentence
        return ""

    def prepare_input_file(self, symptoms, text):
        """
        Prepares the input file for NegEx-MES with extracted symptoms and phrases.
        """
        with open(self.input_path, "w", encoding="utf-8") as file:
            for i, symptom in enumerate(symptoms):
                sentence = self.find_sentences(text, symptom)
                if sentence:  # Ensure the sentence is not empty
                    file.write(f"{i}\t{symptom}\t\"{sentence}\"\n")

    def execute_negex(self, symptoms, text):
        """
        Executes NegEx-MES with the given input text.
        """
        og_dir = os.getcwd()
        os.chdir("NegEx-MES-master/smn/main")
        self.prepare_input_file(symptoms, text)
        command = [
            "java", "-jar", "smn.jar",
            "-displayon", "true",
            "-language", "SPANISH",
            "-answerOptionYes", "true",
            "-isOuputFileGenerated", "true",
            "-lemmaConfigFiles", "false",
            "-routeConfigFiles", self.config_path,
            "-routeInTextFile", self.input_path,
            "-routeOutTextFile", self.output_path
        ]
        subprocess.run(command, check=True)

        affirmed_symptoms = []  # Lista para almacenar síntomas afirmados
        
        # Leer y procesar el archivo de salida para filtrar síntomas afirmados
        if os.path.exists(self.output_path):
            with open(self.output_path, "r", encoding="latin-1") as file:
                for line in file:
                    # Dividir cada línea por el tabulador y verificar si el síntoma es afirmado
                    parts = line.strip().split("\t")
                    if len(parts) >= 5 and parts[3] == "Affirmed":
                        affirmed_symptoms.append(parts[1])  # Añadir el síntoma afirmado a la lista
        os.chdir(og_dir)
                    
        return affirmed_symptoms
