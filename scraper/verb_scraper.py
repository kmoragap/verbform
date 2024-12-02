import requests
from bs4 import BeautifulSoup
import os

def download_audio(url, filename, media_path, base_url):
    """Helper function to download audio files"""
    if not url.startswith("https://"):
        url = f"{base_url}{url}"
    
    audio_path = os.path.join(media_path, filename)
    audio_data = requests.get(url)
    
    with open(audio_path, "wb") as f:
        f.write(audio_data.content)
    
    return f"[sound:{filename}]"

def extract_verb_data(word, config):
    """Main function to extract verb data from verbformen.de"""
    url = f"{config.BASE_URL}/konjugation/steckbrief/info/{word}.htm"
    headers = {"Accept-Language": config.LANGUAGE}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error: Could not access page for word '{word}'.")
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    data = {}
    
    verb_element = soup.find("span", id="grundform")
    if verb_element:
        data["verb"] = verb_element.text.strip()
        
        if audio_link := verb_element.find("a"):
            audio_filename = f"{data['verb']}_infinitiv.mp3"
            data["audio_infinitive"] = download_audio(
                audio_link["href"],
                audio_filename,
                config.ANKI_MEDIA_PATH,
                config.BASE_URL
            )
    
    if conjugations := soup.find("p", id="stammformen"):
        data["conjugations"] = conjugations.text.strip().replace("·", ",")
        
        if audio_link := conjugations.find("a"):
            audio_filename = f"{data['verb']}_conjugations.mp3"
            data["audio_conjugations"] = download_audio(
                audio_link["href"],
                audio_filename,
                config.ANKI_MEDIA_PATH,
                config.BASE_URL
            )
    
    if translation_block := soup.find("p", class_="r1Zeile rU3px rO0px", style="font-size: 1.22em"):
        if translation_span := translation_block.find("span", lang=config.LANGUAGE):
            all_translations = translation_span.text.strip().split(',')
            selected_translations = [t.strip() for t in all_translations[:3]]
            data["translation"] = ', '.join(selected_translations)
    
    if definition_block := soup.find("p", class_="rInf r1Zeile rU3px rO0px rNt"):
        if definition_block.find("i"):
            data["definition"] = definition_block.text.strip()
    
    example_block = soup.find(lambda tag: tag.name == "p" and "»" in tag.get_text())
    if example_block:
        spans = example_block.find_all("span")
        if len(spans) >= 2:
            german_example = spans[0].get_text()
            german_example = german_example.replace("»", "").strip()
            
            translation_span = spans[2]
            if translation_span.find('img'):
                translation_span.find('img').decompose()
            example_translation = translation_span.get_text().strip()
    
            data["example"] = german_example
            data["example_translation"] = example_translation
        else:
            print("Could not extract example and translation.")
    return data

def extract_multiple_verbs(verbs, config):
    """Extract data for multiple verbs"""
    results = {}
    for verb in verbs:
        results[verb] = extract_verb_data(verb, config)
    return results

#def search_verb(word, config):
#    """Search for verb suggestions"""
#    url = f"{config.BASE_URL}/search/{word}"
#    response = requests.get(url, headers={"Accept-Language": config.LANGUAGE})
#    if response.status_code != 200:
#        return []
    
#    soup = BeautifulSoup(response.text, "html.parser")
#    suggestions = soup.find_all("a", class_="rKrm")
#    return [suggestion.text.strip() for suggestion in suggestions]

