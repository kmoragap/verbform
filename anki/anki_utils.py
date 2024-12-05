from anki.collection import Collection
from templates.card_template import *

def add_card_to_anki(data, config):
    col = Collection(config.ANKI_COLLECTION_PATH)
    
    deck_id = col.decks.id(config.DECK_NAME)
    col.decks.select(deck_id)
    
    model = col.models.by_name(config.MODEL_NAME)
    if not model:
        print(f"Error: Model '{config.MODEL_NAME}' not found.")
        col.close()
        return
    
    note = col.new_note(model)
    note.deck_id = deck_id

    if data['type'] == 'verb':
        front_template = get_verb_front_template(data, config.COLORS)
        back_template = get_verb_back_template(data, config.COLORS)
    elif data['type'] == 'noun':
        front_template = get_noun_front_template(data, config.COLORS)
        back_template = get_noun_back_template(data, config.COLORS)
    elif data['type'] == 'adverb':
        front_template = get_adverb_front_template(data, config.COLORS)
        back_template = get_adverb_back_template(data, config.COLORS)

    note.fields[0] = front_template
    note.fields[1] = back_template

    col.add_note(note, deck_id)

    if config.CREATE_REVERSE:
        note = col.new_note(model)
        note.deck_id = deck_id

        if data['type'] == 'verb':
            front_template = get_verb_front_template_reverse(data, config.COLORS)
            back_template = get_verb_back_template_reverse(data, config.COLORS)
        elif data['type'] == 'noun':
            front_template = get_noun_front_template_reverse(data, config.COLORS)
            back_template = get_noun_back_template_reverse(data, config.COLORS)

        note.fields[0] = front_template
        note.fields[1] = back_template

        col.add_note(note, deck_id)

    if config.CREATE_CLOZE:
        model = col.models.by_name("Cloze")
        if not model:
            print(f"Error: Model 'Cloze' not found.")
            col.close()
            return
        
        note = col.new_note(model)
        note.deck_id = deck_id

        if data['type'] == 'verb':
            front_template = get_verb_template_cloze(data, config.COLORS)
        elif data['type'] == 'noun':
            front_template = get_noun_template_cloze(data, config.COLORS)

        note.fields[0] = front_template

        col.add_note(note, deck_id)

    #print(f"'{data['verb']}' successfully added to deck '{config.DECK_NAME}'.")
    
    col.close()