import requests
import time
import os
import pygame
from bs4 import BeautifulSoup
from gtts import gTTS
from deep_translator import GoogleTranslator
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.text import Text
from rich.box import ROUNDED
from rich.columns import Columns
from rich.align import Align

console = Console()

class NewsArchitectPro:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        self.streams = {
            "1": ("India", "https://www.bbc.com/news/world/asia/india"),
            "2": ("World", "https://www.bbc.com/news/world"),
            "3": ("Technology", "https://www.bbc.com/news/technology"),
            "4": ("Science", "https://www.bbc.com/news/science_and_environment"),
            "5": ("Sports", "https://www.bbc.com/sport"),
            "6": ("Business", "https://www.bbc.com/news/business")
        }
        self.languages = {
            "1": ("English", "en"), "2": ("Hindi", "hi"), "3": ("French", "fr"),
            "4": ("Spanish", "es"), "5": ("German", "de"), "6": ("Japanese", "ja"),
            "7": ("Russian", "ru"), "8": ("Arabic", "ar"), "9": ("Portuguese", "pt"),
            "10": ("Italian", "it"), "11": ("Korean", "ko"), "12": ("Turkish", "tr"),
            "13": ("Bengali", "bn"), "14": ("Gujarati", "gu"), "15": ("Tamil", "ta")
        }
        pygame.mixer.init()

    def get_header(self, title=""):
        return Panel(
            Text.assemble((" ARCHITECT ", "bold white on cyan"), (f" {title.upper()} ", "bold cyan")),
            box=ROUNDED, border_style="grey37", expand=True
        )

    def fetch_headlines(self, url):
        """Advanced Scraper: Populates all relevant headlines for the stream."""
        with console.status("[cyan]Synchronizing with stream data...", spinner="point"):
            try:
                res = requests.get(url, headers=self.headers, timeout=10)
                soup = BeautifulSoup(res.text, 'html.parser')
                headlines = []
             
                for item in soup.find_all(['h2', 'h3', 'a']):
                    title = item.get_text().strip()
                    link = item.get('href') if item.name == 'a' else (item.find('a').get('href') if item.find('a') else None)
                    
                    if title and link and len(title) > 25:
                        full_link = link if link.startswith('http') else f"https://www.bbc.com{link}"
                        if full_link not in [h['link'] for h in headlines]:
                            headlines.append({'title': title, 'link': full_link})
                    if len(headlines) == 15: break 
                return headlines
            except:
                return []

    def fetch_full_article(self, url):
        """Recursive Scraper: Extracts all paragraphs from the target article."""
        with console.status("[cyan]Extracting full article content...", spinner="dots"):
            try:
                res = requests.get(url, headers=self.headers, timeout=10)
                soup = BeautifulSoup(res.text, 'html.parser')
                
                paras = [p.get_text().strip() for p in soup.find_all('p') if len(p.get_text()) > 50]
                return paras if paras else ["No content could be decrypted from this source."]
            except:
                return ["Connection to article node failed."]

    def voice_sync_engine(self, paragraphs, lang_code):
        """Fixed Static Frame: Highlights words without duplicated printing."""
        full_text = " ".join(paragraphs)
        
        if lang_code != 'en':
            with console.status(f"[cyan]Translating intelligence...", spinner="dots"):
                full_text = GoogleTranslator(source='auto', target=lang_code).translate(full_text)

        filename = "audio_temp.mp3"
        gTTS(text=full_text, lang=lang_code).save(filename)
        
        pygame.mixer.music.load(filename)
        words = full_text.split()
        
        # Pacing map
        delay = 0.44 if lang_code in ['hi', 'bn', 'gu', 'ta'] else 0.36
        pygame.mixer.music.play()
        
        # Static Live context ensures the UI stays fixed on screen
        with Live(auto_refresh=False) as live:
            for i in range(len(words)):
                if not pygame.mixer.music.get_busy(): break
                
                display = Text(justify="left")
                
                start = max(0, i - 25)
                end = min(len(words), i + 65)
                
                for idx in range(start, end):
                    style = "bold white on cyan" if idx == i else "grey70"
                    display.append(f"{words[idx]} ", style=style)
                
                live.update(Panel(display, title="[bold cyan] ACTIVE VOICE STREAM [/]", border_style="grey37", padding=(1, 2)))
                live.refresh()
                time.sleep(delay)

        pygame.mixer.music.unload()
        if os.path.exists(filename): os.remove(filename)

    def run(self):
        while True:
            console.clear()
            console.print(self.get_header("Clean Information Hub"))
            
            
            grid = [Panel(f"[bold cyan]{k}[/] {v[0]}", border_style="grey37") for k, v in self.streams.items()]
            console.print(Columns(grid, equal=True, expand=True))
            
            choice = console.input("\n[cyan]❯[/] Stream ID (q to quit): ").lower()
            if choice == 'q': break
            
            if choice in self.streams:
                name, url = self.streams[choice]
                news = self.fetch_headlines(url)
                
                if not news:
                    console.print("[red]No headlines found for this stream.[/]")
                    time.sleep(2)
                    continue

                console.clear()
                console.print(self.get_header(f"Feed: {name}"))
                table = Table(box=ROUNDED, border_style="grey37", expand=True)
                table.add_column("ID", style="cyan", justify="center")
                table.add_column("Latest Headlines")
                for i, n in enumerate(news, 1): table.add_row(str(i), n['title'])
                console.print(table)
                
                try:
                    ref = int(console.input("\n[cyan]❯[/] Select News ID: ")) - 1
                    selected = news[ref]
                    
                    
                    paras = self.fetch_full_article(selected['link'])

                    console.clear()
                    console.print(self.get_header("Reader Preference"))
                    modes = Table.grid(padding=1)
                    modes.add_row(
                        Panel("[1] [bold]Visual Reading[/]\n[grey70]Structured Blocks[/]", border_style="grey37", width=35),
                        Panel("[2] [bold cyan]Voice Sync[/]\n[grey70]Translated Audio[/]", border_style="cyan", width=35)
                    )
                    console.print(Align.center(modes))
                    
                    mode = console.input("\n[cyan]❯[/] Choice ID: ")
                    
                    if mode == '2':
                       
                        lang_table = Table(box=ROUNDED, border_style="grey37", show_header=False)
                        for k, v in self.languages.items(): lang_table.add_row(k, v[0])
                        console.print(Align.center(lang_table))
                        
                        l_id = console.input("[cyan]❯[/] Select Language ID: ")
                        lang_code = self.languages.get(l_id, ("English", "en"))[1]
                        
                        console.clear()
                        self.voice_sync_engine(paras, lang_code)
                    else:
                        console.clear()
                        console.print(self.get_header("Complete Content Stream"))
                        for i, p in enumerate(paras, 1):
                            console.print(Panel(p, title=f"[bold cyan] Paragraph {i} [/]", border_style="grey37"))
                        console.input("\n[cyan]❯[/] Press Enter to return...")
                except: pass

if __name__ == "__main__":
    app = NewsArchitectPro()
    app.run()
                    
