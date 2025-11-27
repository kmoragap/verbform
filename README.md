# VerbForm: German Anki Card Generator

**VerbForm** is a Python tool that extracts data from [verbformen.de](https://www.verbformen.de) to automatically create German flashcards in Anki. It supports verbs, nouns, adverbs, and adjectives, complete with audio and customizable templates.

![VerbForm Banner](verbform.gif)

## Prerequisites

  * Python 3.8+
  * Anki Desktop

## Installation

```bash
git clone https://github.com/kmoragap/verbform.git
cd verbform
pip install -r requirements.txt
```

## Configuration

Before running the script, edit `config.py` to match your system settings.

### Required Variables

| Variable | Description |
| :--- | :--- |
| `ANKI_COLLECTION_PATH` | Path to your `.anki2` collection file. |
| `ANKI_MEDIA_PATH` | Path to your Anki media folder. |
| `DECK_NAME` | Target deck name. If it does not exist, it will be created. |
| `MODEL_NAME` | Note type (e.g., "Basic", "Básico", "Basique"). Must match your Anki localization. |
| `LANGUAGE` | Target language code for translations (e.g., `'en'`, `'es'`, `'fr'`). |

> **Note:** Consult the [Anki Manual](https://docs.ankiweb.net/files.html) to locate your file paths.

## Usage

**Important:** Close Anki before running these commands to avoid database locks.

### Verbs

You can add one or multiple verbs at once.

```bash
# Single verb
python main.py lernen

# Multiple verbs
python main.py machen spielen gehen
```

### Nouns, Adjectives, and Adverbs

Use specific flags for non-verb types.

```bash
# Noun
python main.py --noun Buch

# Adjective
python main.py --adjective ganz

# Adverb
python main.py --adverb gern
```

### Advanced Flags

You can combine flags to generate additional card types.

  * `--reverse`: Creates a card with the front and back flipped.
  * `--cloze`: Generates cloze deletion cards based on the word type:
      * **Verbs:** Clozes for 3rd person Präsens, 3rd person Präteritum, and Past Participle.
      * **Nouns:** Clozes for Article (der/die/das), Genitive case, and Plural form.

**Example:**

```bash
python main.py --noun Buch --reverse --cloze
```

## Customization
![Card Design](https://preview.redd.it/i-made-a-small-python-tool-for-creating-german-verb-anki-v0-v5br28smbi4e1.png?width=1504&format=png&auto=webp&s=976c1ad505d3b4e3114c30689d172a22ec425574)
  * **Logic:** Edit `config.py` to change theme colors and language settings.
  * **Design:** Edit `card_template.py` to modify the HTML/CSS structure of the cards.

## Contributing

Contributions are welcome. Please report issues or submit pull requests via the GitHub repository.

-----

### Quick Links

  * [Report Issues](https://github.com/kmoragap/verbform/issues)
  * [Pull Requests](https://github.com/kmoragap/verbform/pulls)
