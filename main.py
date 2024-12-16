import sys
import enum
from pathlib import Path
from colorama import init, Fore, Style

init()

base_path = Path(__file__).resolve().parent
sys.path.extend([str(base_path / 'config'), str(base_path / 'scraper'), str(base_path / 'anki')])

import config
from scraper.verb_scraper import extract_multiple_verbs
from scraper.noun_scraper import extract_multiple_nouns
from scraper.adverb_scraper import extract_multiple_adverbs
from scraper.adjective_scraper import extract_multiple_adjectives
from anki.anki_utils import add_card_to_anki

Types = enum.Enum('Types', [('VERB', 1), ('NOUN', 2), ('ADVERB', 3), ('ADJECTIVE', 4)])

def main():
    print(f"\n{Fore.CYAN}================================")
    print(f"📚 Welcome to VerbForm! 🇩🇪")
    print(f"================================{Style.RESET_ALL}\n")

    print(f"{Fore.YELLOW}Please make sure that Anki is closed before proceeding.{Style.RESET_ALL}")
    input(f"{Fore.YELLOW}Press Enter to continue once Anki is closed...{Style.RESET_ALL}")
    
    if len(sys.argv) < 2:
        print(f"{Fore.RED}Error: Arguments required{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Usage for verbs: python main.py <verb1> <verb2> ... <verbN>{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Usage for nouns: python main.py --noun <noun1> <noun2> ... <nounN>{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Usage for adverbs: python main.py --adverb <adverb1> <adverb2> ... <adverbN>{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}💡 Pro tip: You can add multiple words at once!{Style.RESET_ALL}")
        return

    for arg in sys.argv:
        if arg == '--reverse':
            config.CREATE_REVERSE = True
        elif arg == '--cloze':
            config.CREATE_CLOZE = True

    if config.CREATE_REVERSE:
        sys.argv.remove('--reverse')
    if config.CREATE_CLOZE:
        sys.argv.remove('--cloze')
    if sys.argv[1] == '--noun':
        if len(sys.argv) < 3:
            print(f"{Fore.RED}Error: At least one noun is required after --noun{Style.RESET_ALL}")
            return
        type = Types.NOUN
        words = sys.argv[2:]
    elif sys.argv[1] == '--adverb':
        if len(sys.argv) < 3:
            print(f"{Fore.RED}Error: At least one adverb is required after --adverb{Style.RESET_ALL}")
            return
        type = Types.ADVERB
        words = sys.argv[2:]
    elif sys.argv[1] == '--adjective':
        if len(sys.argv) < 3:
            print(f"{Fore.RED}Error: At least one adjective is required after --adjective{Style.RESET_ALL}")
            return
        type = Types.ADJECTIVE
        words = sys.argv[2:]
    else:
        words = sys.argv[1:]
        type = Types.VERB


    if type == Types.NOUN:
        word_type = "nouns"
    elif type == Types.VERB:
        word_type = "verbs"
    elif type == Types.ADVERB:
        word_type = "adverbs"
    elif type == Types.ADJECTIVE:
        word_type = "adjectives"
    
    print(f"{Fore.CYAN}🔍 Searching for information for the {word_type}: {Fore.WHITE}{', '.join(words)}...{Style.RESET_ALL}")
    
    if type == Types.NOUN:
        data = extract_multiple_nouns(words, config)
    elif type == Types.VERB:
        data = extract_multiple_verbs(words, config)
    elif type == Types.ADVERB:
        data = extract_multiple_adverbs(words, config)
    elif type == Types.ADJECTIVE:
        data = extract_multiple_adjectives(words, config)
    
    for word, word_data in data.items():
        if word_data:
            print(f"{Fore.GREEN}✅ Adding card for the {word_type[:-1]}: {word}{Style.RESET_ALL}")
            add_card_to_anki(word_data, config)
        else:
            print(f"{Fore.RED}❌ No information found for the {word_type[:-1]}: {word}{Style.RESET_ALL}")
    
    print("\n")
    print(f"{Fore.BLUE}📚 Enjoy your language learning journey!{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}★ Enjoying VerbForm? Show your support!")
    print(f"✨ Star us on GitHub: {Fore.WHITE}{config.GITHUB_URL}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}🐛 Found a bug? Open an issue: {Fore.WHITE}{config.ISSUES_URL}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}🤝 Want to contribute? PRs welcome at: {Fore.WHITE}{config.GITHUB_URL}/pulls{Style.RESET_ALL}")
    print("\n")
    print(f"{Fore.CYAN}🌟 Spread the word! Share VerbForm with your friends!{Style.RESET_ALL}")
    print("\n")

if __name__ == "__main__":
    main()