import os
import pdfplumber
import google.generativeai as genai
import json
from app.core.config import settings

def extract_text_from_pdf(file_path: str) -> str:
    text_content = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                text_content += text + "\n"
    return text_content

import re

def clean_text_for_ai(text: str) -> str:
    # Remove caracteres que podem quebrar o JSON ou confundir a IA
    return re.sub(r'[^\x00-\x7F]+', ' ', text)

def extract_cargos_from_text(text_content: str) -> list[str]:
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        return ["Cargo Simulado 1", "Cargo Simulado 2"]

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    clean_text = clean_text_for_ai(text_content[:80000])

    prompt = f"""
    Liste todos os cargos ou áreas de atuação mencionados no edital abaixo.
    Retorne apenas os nomes dos cargos separados por ponto e vírgula (;).
    Não escreva mais nada, apenas os nomes.
    Exemplo: Perito Criminal - Área 3; Agente de Polícia; Delegado.

    Texto:
    {clean_text}
    """

    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip()
        
        # Split por ponto e vírgula e limpa espaços
        cargos = [c.strip() for c in raw_text.split(";") if len(c.strip()) > 3]
        
        if not cargos:
            # Tenta split por nova linha como fallback
            cargos = [c.strip() for c in raw_text.split("\n") if len(c.strip()) > 3]
            
        return cargos if cargos else ["Cargo não identificado"]
    except Exception as e:
        print(f"Error extracting cargos: {e}")
        return ["Erro na conexão com a IA"]

def extract_syllabus_for_cargo(text_content: str, cargo_name: str) -> dict:
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        return {"title": cargo_name, "topics": []}

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    # SMART CHUNKING FLEXÍVEL
    # Primeiro passo: Procurar onde começa a seção geral de conteúdo programático
    syllabus_start = 0
    upper_text = text_content.upper()
    
    # Marcadores comuns do início do conteúdo programático nos editais
    syllabus_markers = ["CONTEÚDO PROGRAMÁTICO", "PROGRAMA DAS PROVAS", "DOS OBJETOS DE AVALIAÇÃO", "ANEXO I -", "ANEXO II -"]
    for marker in syllabus_markers:
        idx = upper_text.find(marker)
        if idx != -1:
            syllabus_start = idx
            break
            
    # Segundo passo: A partir da seção de conteúdo, buscar o cargo específico
    search_keywords = cargo_name.replace(":", " ").replace("-", " ").replace("/", " ").split()
    key_terms = sorted([w for w in search_keywords if len(w) > 3], key=len, reverse=True)[:3]
    
    start_index = -1
    for term in key_terms:
        # Busca o termo do cargo apenas DEPOIS que o conteúdo programático começou
        pos = upper_text.find(term.upper(), syllabus_start)
        if pos != -1:
            start_index = max(syllabus_start, pos - 2000)
            break
            
    # Fallback caso não encontre o cargo dentro da seção
    if start_index == -1:
        start_index = syllabus_start
        
    # Pega um trecho BEM generoso para cobrir tudo (120k caracteres)
    relevant_text = text_content[start_index:start_index + 120000]

    prompt = f"""
    Aja como um engenheiro de dados. Sua tarefa é extrair, limpar e estruturar o conteúdo programático do edital fornecido para o cargo: '{cargo_name}'.
    
    Siga exatamente estes passos na ordem:
    
    Passo 1: Localização de Dados
    - Busque no texto as disciplinas e tópicos da seção "CONHECIMENTOS BÁSICOS" (ou comum a todos os cargos), que se aplica a todas as áreas.
    - Busque no texto as disciplinas e tópicos da seção de conhecimentos específicos listada EXATAMENTE sob o cabeçalho do cargo '{cargo_name}'.
    
    Passo 2: Limpeza e Normalização (ETL)
    - Remova completamente qualquer numeração do edital (ex: "1.", "1.1", "10.2.3"). 
    - Consolide tudo sob o título da disciplina principal.
    
    Passo 3: Formatação de Saída
    NÃO DIGA MAIS NADA. Não explique seus passos. Comece e termine sua resposta EXATAMENTE com o JSON abaixo.
    Retorne o resultado estritamente neste formato JSON:
    {{
      "title": "{cargo_name}",
      "topics": [
        {{ "name": "Disciplina - Tópico - Subtópico", "tags": ["#tag1"] }}
      ]
    }}

    TEXTO PARA ANÁLISE:
    {relevant_text}
    """

    try:
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        print(f"DEBUG: Resposta da IA:\n{result_text[:500]}...") # Log para debug
        
        # Limpeza para garantir que o json.loads não quebre com blocos markdown
        clean_json_str = result_text.replace("```json", "").replace("```", "").strip()
        
        data = json.loads(clean_json_str)
        
        if "topics" not in data or not data["topics"]:
            raise ValueError("JSON retornado não contém tópicos válidos.")
            
        # Garante que as tags geradas estão formatadas
        for t in data["topics"]:
            if "tags" in t:
                t["tags"] = [tag.replace(" ", "").lower() for tag in t["tags"]]
                
        return data
    except Exception as e:
        print(f"CRITICAL ERROR no parser: {e}")
        return {"title": cargo_name, "topics": []}
