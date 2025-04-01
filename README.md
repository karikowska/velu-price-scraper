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
$ python main.py "Hatsune Miku Nendoroid" sol
```

Sample output:
```
🛒 Best match for 'Hatsune Miku Nendoroid' on solaris: The price of the "Hatsune Miku - Racing 2023 Ver." is ¥6980 JPY.
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
    - amiami
    - nng
    - solaris

- name: Hatsune Miku Virtual Popstar Ver.
  stores:
    - amiami
    - solaris
```

And then run the following command to invoke it:
```
$ python main.py "path/to/config.yaml"
```

### 3. Supported Stores
Currently, the only supported services are Solaris Japan, or ```sol```, and Nin-Nin Game, or ```nng```. I've coded up a complete scraper for AmiAmi, but they sadly use Cloudflare to completely block my traffic and serve me zero results.

-to be continued-

---

## 📝 TODO in order of importance:

- [x] finish README instructions to run
- [ ] make batch YAML input method work
- [x] expand functionality to more websites than just Solaris Japan
- [ ] add other stores like Animota, Japan Figure Store, Tokyo Otaku Mode, Hobby Japan... (if they are scrapable!)
- [ ] add reseller sites like Depop, Vinted or Ebay
- [ ] add JP stores like Mercari.jp and Buyee with translation
- [ ] add a wishlist feature (YAML) - user has a wishlist which they can run the scraper on regularly to monitor for current best prices in the file (automation through Bash script?)
- [ ] add preferred budget per figure (YAML) - results will not be shown unless they are less than the budget!
- [ ] add unit tests
- [ ] add database integration to save results
- [ ] add Streamlit integration to talk to the LLM directly?
- [ ] add web UI or a dashboard to show results
- [ ] add license to repo
