import cloudscraper
from bs4 import BeautifulSoup
import os
from scraper_utils import fetch_with_retry

def download_audio(url, filename, media_path, base_url):
    """Helper function to download audio files"""
    if not url.startswith("https://"):
        url = f"{base_url}{url}"

    audio_path = os.path.join(media_path, filename)

    # Use cloudscraper for audio downloads too
    scraper = cloudscraper.create_scraper(browser='chrome')
    audio_data = scraper.get(url)

    with open(audio_path, "wb") as f:
        f.write(audio_data.content)

    return f"[sound:{filename}]"

def normalize_verb_input(word):
    """
    Normalize verb input to base infinitive form.
    Handles cases where user inputs 'umzusetzen' instead of 'umsetzen'.
    For separable verbs, removes the 'zu' insertion (e.g., umzusetzen -> umsetzen).
    """
    # Common separable verb prefixes in German
    separable_prefixes = [
        'ab', 'an', 'auf', 'aus', 'bei', 'ein', 'empor', 'entgegen', 'fort',
        'vor', 'weg', 'zu', 'zurück', 'zusammen', 'durch', 'über', 'unter',
        'wieder', 'gegen', 'hinter', 'mit', 'nach', 'nieder', 'statt', 'um'
    ]

    # Check if verb has 'zu' inserted after a separable prefix
    # Pattern: prefix + zu + verbstem + en (e.g., umzusetzen -> umsetzen)
    for prefix in separable_prefixes:
        if word.startswith(prefix + 'zu'):
            # Remove the 'zu' to get base form
            base_form = prefix + word[len(prefix) + 2:]
            return base_form

    return word

def extract_verb_data(word, config):
    """Main function to extract verb data from verbformen.de"""
    # Normalize input to handle 'zu' forms (e.g., umzusetzen -> umsetzen)
    normalized_word = normalize_verb_input(word)

    url = f"{config.BASE_URL}/konjugation/steckbrief/info/{normalized_word}.htm"
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
    
    verb_element = soup.find("span", id="grundform")
    if verb_element:
        raw = verb_element.text.strip()
        explode = raw.split('/')
        data["verb"] = explode[0]
        
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
        if len(spans) > 2:
            german_example = spans[0].get_text()
            german_example = german_example.replace("»", "").strip()
            
            translation_span = spans[2]

            # Compound verbs handling
            if "·" in data["verb"] and len(spans) > 3:
                translation_span = spans[3]

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
    data = {}
    for verb in verbs:
        verb_data = extract_verb_data(verb, config)
        if verb_data:
            verb_data['type'] = 'verb'
            data[verb] = verb_data
        else:
            data[verb] = None
    return data

