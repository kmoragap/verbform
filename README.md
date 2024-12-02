# 🇩🇪 VerbForm: Your German Verb Learning Tool 📚

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

## 🚀 Usage

### Basic Usage

Create Anki cards for verbs directly from the command line:

```bash
python main.py machen lernen spielen
```

### Supported Commands

- Add a single verb: `python main.py lernen`
- Add multiple verbs: `python main.py machen spielen gehen`

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

## 🔗 Quick Links

- 🐛 [Report Issues](https://github.com/kmoragap/verbform/issues)
- 🌟 [Contribute](https://github.com/kmoragap/verbform/pulls)


---

🌈 **Happy Learning!** Made with ❤️ by German Language Enthusiasts
