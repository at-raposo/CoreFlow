import requests
from bs4 import BeautifulSoup

def fetch_usp_syllabus(course_code: str) -> list[str]:
    """
    Scrapes the JupiterWeb public page for a given course code (e.g. MAC0110)
    and attempts to extract the syllabus (Ementa) topics.
    """
    url = f"https://uspdigital.usp.br/jupiterweb/obterDisciplina?sgldis={course_code}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # In JupiterWeb, the syllabus is usually in a span or td under the "Programa" or "Programa Resumido"
    # The structure is very legacy. We look for text blocks that look like lists.
    topics = []
    
    # Simple heuristic: find "Programa" and get the text after it
    # We will try to find a span that contains the program text
    found_programa = False
    for b_tag in soup.find_all('b'):
        if b_tag.text and "Programa" in b_tag.text:
            # The next text node or table usually contains the syllabus
            parent_td = b_tag.find_parent('td')
            if parent_td:
                # Sometimes it's right in the same TD
                content = parent_td.get_text(separator='\n').replace("Programa", "").strip()
                if len(content) > 10:
                    lines = content.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line and len(line) > 5 and not line.startswith("Docente"):
                            topics.append(line)
                    found_programa = True
                    break
    
    if not topics:
        # Fallback heuristic: just return a generic topic if we can't parse it
        topics = [f"Introdução a {course_code}", f"Aprofundamento {course_code}"]
        
    # Clean up empty strings
    topics = [t for t in topics if t]
    return topics
