def get_verb_front_template(data, colors):
    return f"""
    <div style="font-size: 24px; text-align: center; color: {colors['purple']}; margin: 20px 0; background: {colors['bg']};">
        {data.get('translation', '')}
    </div>
    """

def get_verb_front_template_reverse(data, colors):
    return f"""
    <div style="font-size: 24px; text-align: center; color: {colors['purple']}; margin: 20px 0; background: {colors['bg']};">
        {data.get('verb', '')} {data.get('audio_infinitive', '')}
    </div>
    """

def get_verb_back_template(data, colors):
    return f"""
    <div style="font-family: Arial; line-height: 1.6; padding: 15px; background: {colors['bg']}; color: {colors['fg']};">
        <div style="font-size: 28px; color: {colors['purple']}; text-align: center; margin-bottom: 20px;">
            {data.get('verb', '')} {data.get('audio_infinitive', '')}
        </div>
        
        <div style="background: {colors['bg_highlight']}; padding: 10px; border-radius: 5px; margin: 10px 0;">
            <div style="color: {colors['gray']};">Conjugations:</div>
            {data.get('conjugations', '')} {data.get('audio_conjugations', '')}
        </div>
        
        <details style="margin: 10px 0; background: {colors['bg_highlight']}; padding: 10px; border-radius: 5px;">
            <summary style="color: {colors['blue']}; cursor: pointer;">View definition</summary>
            <div style="padding: 10px 0;">
                {data.get('definition', '')}
            </div>
        </details>
        
        <div style="background: {colors['bg_highlight']}; padding: 10px; border-radius: 5px; margin: 10px 0;">
            <div style="color: {colors['gray']};">Example:</div>
            <div style="margin: 5px 0; color: {colors['fg']};">{data.get('example', '')}</div>
            <div style="color: {colors['blue']}; margin-top: 5px;">{data.get('example_translation', '')}</div>
        </div>
    </div>
    """

def get_verb_back_template_reverse(data, colors):
    return f"""
    <div style="font-family: Arial; line-height: 1.6; padding: 15px; background: {colors['bg']}; color: {colors['fg']};">
        <div style="font-size: 28px; color: {colors['purple']}; text-align: center; margin-bottom: 20px;">
            {data.get('translation', '')}
        </div>
        
        <div style="background: {colors['bg_highlight']}; padding: 10px; border-radius: 5px; margin: 10px 0;">
            <div style="color: {colors['gray']};">Conjugations:</div>
            {data.get('conjugations', '')} {data.get('audio_conjugations', '')}
        </div>
        
        <details style="margin: 10px 0; background: {colors['bg_highlight']}; padding: 10px; border-radius: 5px;">
            <summary style="color: {colors['blue']}; cursor: pointer;">View definition</summary>
            <div style="padding: 10px 0;">
                {data.get('definition', '')}
            </div>
        </details>
        
        <div style="background: {colors['bg_highlight']}; padding: 10px; border-radius: 5px; margin: 10px 0;">
            <div style="color: {colors['gray']};">Example:</div>
            <div style="margin: 5px 0; color: {colors['fg']};">{data.get('example', '')}</div>
            <div style="color: {colors['blue']}; margin-top: 5px;">{data.get('example_translation', '')}</div>
        </div>
    </div>
    """

def get_verb_template_cloze(data, colors):
    # Create a 3-part cloze card: (1) hide 3rd person Präsens conjugation (2) hide 3rd person Präteritum conjugation (3) hide past Partzip
    conjugation = data.get('conjugations', '')
    conjugation_explode = conjugation.split()
    verb = data["verb"].replace('·', '') # Remove separator within compound verb
    if "·" not in data["verb"]:
        pras3 = conjugation_explode[0]
        prat3 = conjugation_explode[2]
        hatist = conjugation_explode[4]
        part = conjugation_explode[5]
    else: # Compound verb
        pras3 = conjugation_explode[0] + " " + conjugation_explode[1]
        prat3 = conjugation_explode[3] + " " + conjugation_explode[4]
        hatist = conjugation_explode[6]
        part = conjugation_explode[7]

    clozeStr = "{{c1::Es " + str(pras3) + "::Präsens}} | {{c2::Es " + str(prat3) + "::Präteritum}} | {{c3::Es " + str(hatist) + " " + str(part) + "::Partzip}} "

    return f"""
    <div style="font-family: Arial; line-height: 1.6; padding: 15px; background: {colors['bg']}; color: {colors['fg']};">
        <div style="font-size: 28px; color: {colors['purple']}; text-align: center; margin-bottom: 20px;">
            {verb}
        </div>
        
        <div style="font-size: 28px; color: {colors['purple']}; text-align: center; margin-bottom: 20px;">
            {data.get('translation', '')}
        </div>

        <div style="background: {colors['bg_highlight']}; padding: 10px; border-radius: 5px; margin: 10px 0;">
            <div style="color: {colors['gray']};">Conjugations:</div>
            {clozeStr}
        </div>
        
        <details style="margin: 10px 0; background: {colors['bg_highlight']}; padding: 10px; border-radius: 5px;">
            <summary style="color: {colors['blue']}; cursor: pointer;">View definition</summary>
            <div style="padding: 10px 0;">
                {data.get('definition', '')}
            </div>
        </details>
        
        <div style="background: {colors['bg_highlight']}; padding: 10px; border-radius: 5px; margin: 10px 0;">
            <div style="color: {colors['gray']};">Example:</div>
            <div style="margin: 5px 0; color: {colors['fg']};">{data.get('example', '')}</div>
            <div style="color: {colors['blue']}; margin-top: 5px;">{data.get('example_translation', '')}</div>
        </div>
    </div>
    """

def get_noun_front_template(data, colors):
    return f"""
    <div style="font-size: 24px; text-align: center; color: {colors['purple']}; margin: 20px 0; background: {colors['bg']};">
        {data.get('translation_noun', '')}
    </div>
    """

def get_noun_front_template_reverse(data, colors):
    return f"""
    <div style="font-size: 24px; text-align: center; color: {colors['purple']}; margin: 20px 0; background: {colors['bg']};">
        {data.get('noun', '')} {data.get('audio_noun', '')}
    </div>
    """

def get_noun_back_template(data, colors):
    return f"""
    <div style="font-family: Arial; line-height: 1.6; padding: 15px; background: {colors['bg']}; color: {colors['fg']};">
        <div style="font-size: 28px; color: {colors['purple']}; text-align: center; margin-bottom: 20px;">
            {data.get('noun', '')} {data.get('audio_noun', '')}
        </div>
        
        <div style="background: {colors['bg_highlight']}; padding: 10px; border-radius: 5px; margin: 10px 0;">
            <div style="color: {colors['gray']};">Genitive and Plural:</div>
            {data.get('stem', '')} {data.get('audio_stem', '')}
        </div>

        <details style="margin: 10px 0; background: {colors['bg_highlight']}; padding: 10px; border-radius: 5px;">
            <summary style="color: {colors['blue']}; cursor: pointer;">View definition</summary>
            <div style="padding: 10px 0;">
                {data.get('definition_noun', '')}
            </div>
        </details>
        
        <div style="background: {colors['bg_highlight']}; padding: 10px; border-radius: 5px; margin: 10px 0;">
            <div style="color: {colors['gray']};">Example:</div>
            <div style="margin: 5px 0; color: {colors['fg']};">{data.get('example_noun', '')}</div>
            <div style="color: {colors['blue']}; margin-top: 5px;">{data.get('example_noun_translation', '')}</div>
        </div>
    </div>
    """

def get_noun_back_template_reverse(data, colors):
    return f"""
    <div style="font-family: Arial; line-height: 1.6; padding: 15px; background: {colors['bg']}; color: {colors['fg']};">
        <div style="font-size: 28px; color: {colors['purple']}; text-align: center; margin-bottom: 20px;">
            {data.get('translation_noun', '')}
        </div>
        
        <div style="background: {colors['bg_highlight']}; padding: 10px; border-radius: 5px; margin: 10px 0;">
            <div style="color: {colors['gray']};">Genitive and Plural:</div>
            {data.get('stem', '')} {data.get('audio_stem', '')}
        </div>

        <details style="margin: 10px 0; background: {colors['bg_highlight']}; padding: 10px; border-radius: 5px;">
            <summary style="color: {colors['blue']}; cursor: pointer;">View definition</summary>
            <div style="padding: 10px 0;">
                {data.get('definition_noun', '')}
            </div>
        </details>
        
        <div style="background: {colors['bg_highlight']}; padding: 10px; border-radius: 5px; margin: 10px 0;">
            <div style="color: {colors['gray']};">Example:</div>
            <div style="margin: 5px 0; color: {colors['fg']};">{data.get('example_noun', '')}</div>
            <div style="color: {colors['blue']}; margin-top: 5px;">{data.get('example_noun_translation', '')}</div>
        </div>
    </div>
    """

def get_noun_template_cloze(data, colors):
    # Create a 3-part cloze card: (1) hide der/die/das (2) hide genitive form (3) hide plural form
    noun = data.get('noun', '')
    declension = data.get('stem', '')
    noun_explode = noun.split()
    declension_explode = declension.split()
    pronoun = noun_explode[0]
    word = noun_explode[1]
    genitive = declension_explode[0]
    plural = declension_explode[2]
    genitive_pronoun = 'des'

    if (pronoun == 'die'):
        genitive_pronoun = 'der'

    clozeStr1 = "{{c1::" + str(pronoun) + "::der/die/das}} " + str(word)
    clozeStr2 = "{{c2::" + str(genitive_pronoun) + " " + str(genitive) + "::genitive}} {{c3::die " + str(plural) + "::plural}}"


    return f"""
    <div style="font-family: Arial; line-height: 1.6; padding: 15px; background: {colors['bg']}; color: {colors['fg']};">
        <div style="font-size: 28px; color: {colors['purple']}; text-align: center; margin-bottom: 20px;">
            {clozeStr1}
        </div>

        <div style="font-size: 28px; color: {colors['purple']}; text-align: center; margin-bottom: 20px;">
            {data.get('translation_noun', '')}
        </div>
        
        <div style="background: {colors['bg_highlight']}; padding: 10px; border-radius: 5px; margin: 10px 0;">
            <div style="color: {colors['gray']};">Plural:</div>
            {clozeStr2}
        </div>

        <details style="margin: 10px 0; background: {colors['bg_highlight']}; padding: 10px; border-radius: 5px;">
            <summary style="color: {colors['blue']}; cursor: pointer;">View definition</summary>
            <div style="padding: 10px 0;">
                {data.get('definition_noun', '')}
            </div>
        </details>
        
        <div style="background: {colors['bg_highlight']}; padding: 10px; border-radius: 5px; margin: 10px 0;">
            <div style="color: {colors['gray']};">Example:</div>
            <div style="margin: 5px 0; color: {colors['fg']};">{data.get('example_noun', '')}</div>
            <div style="color: {colors['blue']}; margin-top: 5px;">{data.get('example_noun_translation', '')}</div>
        </div>
    </div>
    """

def get_adverb_front_template(data, colors):
    return f"""
    <div style="font-size: 24px; text-align: center; color: {colors['purple']}; margin: 20px 0; background: {colors['bg']};">
        {data.get('adverb', '')}
    </div>
    """

def get_adverb_back_template(data, colors):
    return f"""
    <div style="font-family: Arial; line-height: 1.6; padding: 15px; background: {colors['bg']}; color: {colors['fg']};">
        <div style="font-size: 28px; color: {colors['purple']}; text-align: center; margin-bottom: 20px;">
            {data.get('translation_adverb', '')}
        </div>

        <details style="margin: 10px 0; background: {colors['bg_highlight']}; padding: 10px; border-radius: 5px;">
            <summary style="color: {colors['blue']}; cursor: pointer;">View definition</summary>
            <div style="padding: 10px 0;">
                {data.get('definition_adverb', '')}
            </div>
        </details>
        
        <div style="background: {colors['bg_highlight']}; padding: 10px; border-radius: 5px; margin: 10px 0;">
            <div style="color: {colors['gray']};">Example:</div>
            <div style="margin: 5px 0; color: {colors['fg']};">{data.get('example_adverb', '')}</div>
            <div style="color: {colors['blue']}; margin-top: 5px;">{data.get('example_adverb_translation', '')}</div>
        </div>
    </div>
    """

def get_adjective_front_template(data, colors):
    return f"""
    <div style="font-size: 24px; text-align: center; color: {colors['purple']}; margin: 20px 0; background: {colors['bg']};">
        {data.get('adjective', '')} {data.get('audio_adjective', '')}
    </div>
    """

def get_adjective_back_template(data, colors):
    return f"""
    <div style="font-family: Arial; line-height: 1.6; padding: 15px; background: {colors['bg']}; color: {colors['fg']};">
        <div style="font-size: 28px; color: {colors['purple']}; text-align: center; margin-bottom: 20px;">
            {data.get('translation_adjective', '')}
        </div>

        <details style="margin: 10px 0; background: {colors['bg_highlight']}; padding: 10px; border-radius: 5px;">
            <summary style="color: {colors['blue']}; cursor: pointer;">View definition</summary>
            <div style="padding: 10px 0;">
                {data.get('definition_adjective', '')}
            </div>
        </details>
        
        <div style="background: {colors['bg_highlight']}; padding: 10px; border-radius: 5px; margin: 10px 0;">
            <div style="color: {colors['gray']};">Example:</div>
            <div style="margin: 5px 0; color: {colors['fg']};">{data.get('example_adjective', '')}</div>
            <div style="color: {colors['blue']}; margin-top: 5px;">{data.get('example_adjective_translation', '')}</div>
        </div>
    </div>
    """