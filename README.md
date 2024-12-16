# 🇩🇪 VerbForm: Python tool for creating German verb Anki cards  📚

## 🌟 Overview

VerbForm is a powerful Python-based tool designed to help language learners quickly create Anki flashcards for German verbs. With just a few commands, you can transform verb information from [verbformen.de](https://www.verbformen.de) into beautiful, informative Anki cards.

![VerbForm Banner](verbform.gif)

## ✨ Features

- 🤖 Automatic verb data extraction
- 📇 One-click Anki card creation
- 🔊 Includes audio pronunciations
- 🌈 Customized, visually appealing card design
- 🌍 Multilingual support

## 🛠 Prerequisites

Before you begin, ensure you have:

- Python 3.8+
- Anki Desktop installed
- A passion for learning German! 🇩🇪

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kmoragap/verbform.git
   cd verbform
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🔧 Configuration

### Detailed Configuration Guide

Before using VerbForm, you **MUST** configure the `config.py` file carefully. Here's a step-by-step walkthrough:

#### 1. Anki Collection Paths

You need to specify the exact paths to your Anki collection:

- `ANKI_COLLECTION_PATH`: The path to your Anki collection file
- `ANKI_MEDIA_PATH`: The path to your Anki media folder

🔍 **How to Find Your Paths:**
- For macOS: `/Users/[YourUsername]/Library/Application Support/Anki2/[Profile Name]/`
- For Windows: `C:\Users\[YourUsername]\AppData\Roaming\Anki2\[Profile Name]\`
- For Linux: `~/.local/share/Anki2/[Profile Name]/`

🌐 **Helpful Resources:**
- [Anki Manual: Finding Collection Paths](https://docs.ankiweb.net/files.html)

#### 2. Deck Configuration

- `DECK_NAME`: The name of the Anki deck where cards will be added
  - Can be an existing deck
  - Or create a new deck by simply entering a new name

#### 3. Model Name

- `MODEL_NAME`: The type of note template
  - Default is "Basic" (English)
  - Varies by Anki's language setting, e.g.:
    - Spanish: "Básico"
    - French: "Basique"

🌍 **Tip:** Check your Anki's note type name in the card type manager.

#### 4. Language Setting

- `LANGUAGE`: Set the language code for translations
  - `'es'` for Spanish
  - `'fr'` for French
  - `'en'` for English
  - etc.

## 🚀 Usage

### Basic Usage

Create Anki cards for verbs directly from the command line:

```bash
python main.py machen lernen spielen
```

### Adding Nouns

To add a noun to your Anki deck, use the `--noun` flag:

```bash
python3.12 main.py --noun <noun>
```

Example:
```bash
python3.12 main.py --noun libro
```

Use the `--reverse` and/or `--cloze` flags to generate multiple cards from the noun. Reverse will flip front and back for better recall. Cloze will create a cloze on (1) der/die/das, (2) genitive case, and (3) plural form

Example:
```bash
python3.12 main.py --noun libro --reverse --cloze
```

### Adding Adverbs

To add an adverb to your Anki deck, use the `--adverb` flag:

```bash
python3.12 main.py --adverb <adverb>
```

Example:
```bash
python3.12 main.py --adverb gern
```

### Adding Adjectives

To add an adjective to your Anki deck, use the `--adjective` flag:

```bash
python3.12 main.py --adjective <adjective>
```

Example:
```bash
python3.12 main.py --adjective ganz
```

### Supported Commands

- Add a single verb: `python main.py lernen`
- Add multiple verbs: `python main.py machen spielen gehen`
- Use the `--reverse` and/or `--cloze` flags to generate multiple cards from the verb. Reverse will flip front and back for better recall. Cloze will create a cloze on (1) 3rd person Präsens, (2) 3rd person Präteritum, and (3) past Partzip

Example:
```bash
python3.12 main.py lernen --reverse --cloze
```

### Important Notes

⚠️ **IMPORTANT**: 
- Close Anki before running the script
- Ensure you have the correct Anki deck and model set in `config.py`

## 🎨 Customization

### Configuration

Edit `config.py` to customize:
- Anki collection path
- Deck and model names
- Language settings
- Theme colors

### Card Design

![Card Design](https://preview.redd.it/i-made-a-small-python-tool-for-creating-german-verb-anki-v0-v5br28smbi4e1.png?width=1504&format=png&auto=webp&s=976c1ad505d3b4e3114c30689d172a22ec425574)


The `card_template.py` allows you to modify the visual style of your Anki cards. Adjust colors, fonts, and layout to suit your learning style!

## 🌐 Language Support

Translations currently tested in:
- Spanish (es)
- French (fr)
- English (en)

But it should work for all languages 😁.

Set your preferred language in `config.py`

## 🤝 Contributing

Love VerbForm? Help us make it better!

- ⭐ Star the repository
- 🐛 Report issues
- 🚀 Submit pull requests

## 📍 Roadmap

- [ ] Create web interface
- [ ] New card templates

## 🔗 Quick Links

- 🐛 [Report Issues](https://github.com/kmoragap/verbform/issues)
- 🌟 [Contribute](https://github.com/kmoragap/verbform/pulls)


---

🌈 **Happy Learning!** Made with ❤️ by German Language Enthusiast
