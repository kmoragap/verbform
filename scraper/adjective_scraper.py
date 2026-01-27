import requests
from bs4 import BeautifulSoup
from verb_scraper import download_audio
import os
from scraper_utils import fetch_with_retry

def extract_adjective_data(word, config):
    """Main function to extract adjective data from verben.de"""
    url = f"{config.BASE_URL}/deklination/adjektive/steckbrief/info/{word}.htm"
    headers = {
        "Accept-Language": config.LANGUAGE,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    response, error = fetch_with_retry(url, headers, config)
    if error:
        print(f"Error for '{word}': {error}")
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    data = {}

    adjective_element = soup.find("div", class_="rCntr rClear")
    if adjective_element:
        data["adjective"] = adjective_element.text.strip()

        if audio_link := adjective_element.find("a"):
            audio_filename = f"{data['adjective']}_adjective.mp3"
            data["audio_adjective"] = download_audio(
                audio_link["href"],
                audio_filename,
                config.ANKI_MEDIA_PATH, 
                config.BASE_URL
            )
    
    if translation_block := soup.find("p", style="font-size: 1.22em"):
        if translation_span := translation_block.find("span", lang=config.LANGUAGE):
            all_translations = translation_span.text.strip().split(',')
            selected_translations = [t.strip() for t in all_translations[:3]]
            data["translation_adjective"] = ', '.join(selected_translations)
    
    if definition_block := soup.find("p", class_="rInf r1Zeile rU3px rO0px"):
        if definition_block.find("i"):
            data["definition_adjective"] = definition_block.text.strip()

    example_block = soup.find(lambda tag: tag.name == "p" and "»" in tag.get_text())
    if example_block:
        spans = example_block.find_all("span")
        if len(spans) > 2:
            german_example = spans[0].get_text()
            german_example = german_example.replace("»", "").strip()
            
            translation_span = spans[2]
            if translation_span.find('img'):
                translation_span.find('img').decompose()
            example_translation = translation_span.get_text().strip()
    
            data["example_adjective"] = german_example
            data["example_adjective_translation"] = example_translation
        else:
            print("Could not extract example and translation.")

    return data

def extract_multiple_adjectives(adjectives, config):
    """Extract data for multiple adjectives"""
    data = {}
    for adjective in adjectives:
        adjective_data = extract_adjective_data(adjective, config)
        if adjective_data:
            adjective_data['type'] = 'adjective'
            data[adjective] = adjective_data
        else:
            data[adjective] = None
    return data