import requests
from bs4 import BeautifulSoup
import os

def extract_adverb_data(word, config):
    """Main function to extract adverb data from verben.de"""
    url = f"{config.ALT_BASE_URL}/adverbien/steckbrief-info/{word}.htm"
    headers = {"Accept-Language": config.LANGUAGE}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error: Could not access page for word '{word}'.")
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    data = {}

    adverb_element = soup.find("div", class_="rCntr rClear")
    if adverb_element:
        data["adverb"] = adverb_element.text.strip()
    
    if translation_block := soup.find("p", class_="r1Zeile rU6px rO0px", style="font-size: 1.22em;"):
        if translation_span := translation_block.find("span", lang=config.LANGUAGE):
            all_translations = translation_span.text.strip().split(',')
            selected_translations = [t.strip() for t in all_translations[:3]]
            data["translation_adverb"] = ', '.join(selected_translations)
    
    if definition_block := soup.find("p", class_="rInf r1Zeile rU3px rO0px"):
        if definition_block.find("i"):
            data["definition_adverb"] = definition_block.text.strip()
    
    if example_block := soup.find("span", class_="rNt"):
        german_example = example_block.text.strip()
        german_example = german_example.replace("»", "").strip()
        german_example = german_example.replace("\n", "").strip()
        data["example_adverb"] = german_example

    if example_block := example_block.find_next_sibling("span", class_="rInf"):
        if example_block.find('img'):
            example_block.find('img').decompose()
        example_translation = example_block.get_text().strip()
        data["example_adverb_translation"] = example_translation

    '''
    example_block = soup.find(lambda tag: tag.name == "p" and "»" in tag.get_text())
    if example_block:
        spans = example_block.find_all("span")
        #if len(spans) >= 2:
        german_example = spans[0].get_text()
        german_example = german_example.replace("»", "").strip()
            
        translation_span = spans[2]
        if translation_span.find('img'):
            translation_span.find('img').decompose()
        example_translation = translation_span.get_text().strip()
    
            data["example_adverb"] = german_example
            data["example_adverb_translation"] = example_translation
        else:
            print("Could not extract example and translation.")
    '''
    return data

def extract_multiple_adverbs(adverbs, config):
    """Extract data for multiple adverbs"""
    data = {}
    for adverb in adverbs:
        adverb_data = extract_adverb_data(adverb, config)
        adverb_data['type'] = 'adverb'
        if adverb_data:
            data[adverb] = adverb_data
    return data