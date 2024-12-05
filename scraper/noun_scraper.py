import requests
from bs4 import BeautifulSoup
from verb_scraper import download_audio
import os

def extract_noun_data(word, config):
    """Main function to extract noun data from verbformen.de"""
    url = f"{config.BASE_URL}/deklination/substantive/steckbrief/info/{word}.htm"
    headers = {"Accept-Language": config.LANGUAGE}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error: Could not access page for word '{word}'.")
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    data = {}

    noun_element = soup.find("span", class_="vGrnd")
    if noun_element:
        data["noun"] = noun_element.text.strip()
        
        if audio_link := noun_element.find("a"):
            audio_filename = f"{data['noun']}_noun.mp3"
            data["audio_noun"] = download_audio(
                audio_link["href"],
                audio_filename,
                config.ANKI_MEDIA_PATH, 
                config.BASE_URL
            )
    
    if stem_element := soup.find("p", class_="vStm"):
        data["stem"] = stem_element.text.strip()
        # strip out superscripts and subscripts
        data["stem"] = ''.join([i for i in data["stem"] if ord(i) < 256])
        if audio_link := stem_element.find("a"):
            audio_filename = f"{data['noun']}_stem.mp3"
            data["audio_stem"] = download_audio(
                audio_link["href"],
                audio_filename, 
                config.ANKI_MEDIA_PATH,
                config.BASE_URL
            )
    
    if translation_block := soup.find("p", class_="r1Zeile rU3px rO0px", style="font-size: 1.22em"):
        if translation_span := translation_block.find("span", lang=config.LANGUAGE):
            all_translations = translation_span.text.strip().split(',')
            selected_translations = [t.strip() for t in all_translations[:3]]
            data["translation_noun"] = ', '.join(selected_translations)
    
    if definition_block := soup.find("p", class_="rInf r1Zeile rU3px rO0px"):
        if definition_block.find("i"):
            data["definition_noun"] = definition_block.text.strip()
    
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
    
            data["example_noun"] = german_example
            data["example_noun_translation"] = example_translation
        else:
            print("Could not extract example and translation.")
    
    return data

def extract_multiple_nouns(nouns, config):
    """Extract data for multiple nouns"""
    data = {}
    for noun in nouns:
        noun_data = extract_noun_data(noun, config)
        noun_data['type'] = 'noun'
        if noun_data:
            data[noun] = noun_data
    return data