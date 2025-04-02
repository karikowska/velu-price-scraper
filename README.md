# 🛍️ Velu - AI Price Scraper

An AI-powered price-checking tool that scrapes figure listings from websites like **Solaris Japan**, extracts prices using **LangChain + OpenAI**, and intelligently fills in the price and picks the best matches. 

I collect figures in my free time and love getting a good deal - but this can be time-consuming on the regular! I made this tool to speed the process up :)

---

## ✨ Features

- 🔍 Scrapes real-time product listings from supported sites (currently Nin-Nin Game, Solaris Japan)
- 💬 Uses an LLM agent to extract and interpret price information from messy HTML
- 🧠 Selects the most relevant or cheapest listing (not yet!)
- 🗂️ Supports single-product CLI mode and batch YAML input (working on this!)
- ⚙️ Modular and very easy to extend to other figure stores! (as long as you are willing to put in the extra work to scroll through their Inspect Element menus to figure out what goes where 🙃)

---

## 🧪 Example Command & Output
Command:
```
$ python main.py "Hatsune Miku Rascal Trio-Try-It" sol
```

Sample output:
```
🔎 Scraping: Araiguma Rascal - Vocaloid - Hatsune Miku - Rascal - Trio-Try-iT - Akuma (FuRyu)
https://solarisjapan.com//products/araiguma-rascal-vocaloid-hatsune-miku-rascal-trio-try-it-akuma-furyu?oid=268825&qid=9546401fd66c683846ba8262b7713d55
💷 Price: ¥17,120 | Raw: This is a figure listing.

The price of the Araiguma Rascal - Vocaloid - Hatsune Miku - Rascal - Trio-Try-iT - Akuma figure is ¥17,120 JPY. After converting from JPY to GBP, the final price is £120.
```

---

## 🚀 Getting Started

### 1. Install dependencies
To install dependencies in this project, use the following command:
```
pip install -r requirements.txt
```

You'll also need an OpenAI API key. Set it in your terminal using ```export``` or place within a .env file as such:
```
OPENAI_API_KEY=...
```

### 2. Usage
#### Single item
To run the single item price scraper, you will need the following command:
```
$ python main.py "<nameofitem>" <nameofsupportedservice>
```

#### Bulk
To run the price scraper in bulk, you will need to create a YAML file that looks like this:
```
- name: Hatsune Miku Pop Up Parade Galaxy Live
  stores:
    - anim
    - nng

- name: Hatsune Miku Virtual Popstar Ver.
  stores:
    - nng
    - sol
    - jf
```

And then run the following command to invoke it:
```
$ python main.py "path/to/config.yaml"
```

### 3. Supported Stores
Currently, the only supported services are:
- Solaris Japan == ```sol```
- Nin-Nin Game == ```nng```
- Animota == ```anim```
- Japan Figure == ```jf```

I've coded up a complete scraper for AmiAmi, but they sadly use Cloudflare and I seem to be getting obfuscated results. I need to work on it a bit more.

-to be continued-

---

## 📝 TODO in order of importance:

- [x] finish README instructions to run
- [x] make batch YAML input method work
- [x] expand functionality to more websites than just Solaris Japan
- [ ] add other stores like Animota, Japan Figure Store, Tokyo Otaku Mode, Hobby Japan... (if they are scrapable!)
- [ ] add reseller sites like Depop, Vinted or Ebay
- [ ] add JP stores like Mercari.jp and Buyee with translation
- [ ] add NLP to replace where an LLM doesn't need to be!
- [ ] add a wishlist feature (YAML) - user has a wishlist which they can run the scraper on regularly to monitor for current best prices in the file (automation through Bash script?)
- [ ] add preferred budget per figure (YAML) - results will not be shown unless they are less than the budget!
- [ ] look into why AmiAmi can't have its prices scraped and if we can go around that
- [ ] add an LLM that will delete listings that are not relevant to figure-finding OR just use NLP to verify strings against a corpus
- [ ] add unit tests
- [ ] add database integration to save results
- [ ] add Streamlit integration to talk to the LLM directly?
- [ ] add web UI or a dashboard to show results
- [ ] add license to repo

---

## Lessons learned!

This project has taught me:
- web scraping and BeautifulSoup4!
- LangChain, prompting and dealing with token limitations
- how to efficiently wade through Inspect Element
- how to build and modularize a mini-app

---

## DISCLAIMER

I do not own any of the stores mentioned above. I do not own Hatsune Miku either, she is property of Crypton Future Media. All I own here is the code for the price scraper.
