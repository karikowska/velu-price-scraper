# 🛍️ Velu - AI Price Scraper

An AI-powered price-checking tool that scrapes figure listings from websites like **Solaris Japan**, extracts prices using **LangChain + OpenAI**, and intelligently picks the best match.

---

## ✨ Features

- 🔍 Scrapes real-time product listings from supported sites (currently Nin-Nin Game, Solaris Japan)
- 💬 Uses an LLM agent to extract and interpret price information from messy HTML
- 🧠 Selects the most relevant or cheapest listing (not yet!)
- 🗂️ Supports single-product CLI mode and batch YAML input (working on this!)
- ⚙️ Modular and very easy to extend to other figure stores! (as long as you are willing to put in the extra work to scroll through their Inspect Element menus to figre out what goes where 🙃)

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
To run the price scraper, you will need the following command:
```
$ python main.py "<nameofitem>" <nameofsupportedservice>
```

Currently, the only supported services are Solaris Japan, or ```sol```, and Nin-Nin Game, or ```nng```. I've coded up a complete scraper for AmiAmi, but they sadly use Cloudflare to completely block my traffic and serve me zero results.

-to be continued-

## 📝 TODO in order of importance:

- [x] finish README instructions to run
- [ ] make batch YAML input method work
- [x] expand functionality to more websites than just Solaris Japan
- [ ] add other stores like animota, Japan Figure Store, Tokyo Otaku Mode, Hobby Japan... (if they are scrapable!)
- [ ] add unit tests
- [ ] add database integration to save results
- [ ] add web UI or a dashboard to show results
- [ ] add license to repo
