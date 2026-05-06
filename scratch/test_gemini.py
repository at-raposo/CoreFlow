import os
import google.generativeai as genai
import json
from dotenv import load_dotenv

# Mock settings
class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

settings = Settings()

def test_parser():
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        print("API KEY NOT FOUND")
        return

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    cargo_name = "Perito Criminal Federal - Informática Forense"
    # Texto mais longo simulando o trecho do edital
    text_content = "CONTEÚDO PROGRAMÁTICO. CONHECIMENTOS BÁSICOS. LÍNGUA PORTUGUESA: Compreensão e interpretação de textos. CONHECIMENTOS ESPECÍFICOS. CARGO 4: PERITO CRIMINAL FEDERAL/ÁREA 3. 1 Sistemas operacionais. 2 Redes de computadores."

    prompt = f"""
    Você é um ENGENHEIRO DE DADOS sênior.
    Extraia o Conteúdo Programático do edital para o cargo: '{cargo_name}'.

    REGRAS:
    1. Agrupe por disciplina: "Disciplina - Tópico Principal - Subtópico".
    2. Remova toda numeração original.
    3. Retorne EXATAMENTE este formato JSON:
    {{
      "title": "{cargo_name}",
      "topics": [
        {{ "name": "Disciplina - Tópico - Subtópico", "tags": ["#tag1", "#tag2"] }}
      ]
    }}

    Texto:
    {text_content}
    """

    try:
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        print("RAW RESPONSE:", response.text)
        data = json.loads(response.text)
        print("SUCCESS:", data)
    except Exception as e:
        print("ERROR:", e)

if __name__ == "__main__":
    load_dotenv("coreflow-backend/.env")
    settings.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    test_parser()
