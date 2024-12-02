import sys
from pathlib import Path
from colorama import init, Fore, Style

init()

base_path = Path(__file__).resolve().parent
sys.path.extend([str(base_path / 'config'), str(base_path / 'scraper'), str(base_path / 'anki')])

import config
from scraper.verb_scraper import extract_verb_data, extract_multiple_verbs
from anki.anki_utils import add_card_to_anki

def main():
    print(f"\n{Fore.CYAN}================================")
    print(f"📚 Welcome to VerbForm! 🇩🇪")
    print(f"================================{Style.RESET_ALL}\n")

    print(f"{Fore.YELLOW}Please make sure that Anki is closed before proceeding.{Style.RESET_ALL}")
    input(f"{Fore.YELLOW}Press Enter to continue once Anki is closed...{Style.RESET_ALL}")
    
    if len(sys.argv) < 2:
        print(f"{Fore.RED}Error: At least one verb is required as an argument{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Usage: python main.py <verb1> <verb2> ... <verbN>{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}💡 Pro tip: You can add multiple verbs at once!{Style.RESET_ALL}")
        return
    
    words = sys.argv[1:]
    print(f"{Fore.CYAN}🔍 Searching for information for the verbs: {Fore.WHITE}{', '.join(words)}...{Style.RESET_ALL}")
    
    data = extract_multiple_verbs(words, config)
    for word, verb_data in data.items():
        if verb_data:
            print(f"{Fore.GREEN}✅ Adding card for the verb: {word}{Style.RESET_ALL}")
            add_card_to_anki(verb_data, config)
        else:
            print(f"{Fore.RED}❌ No information found for the verb: {word}{Style.RESET_ALL}")
    
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
