# 🛍️ AI Price Scraper

An AI-powered price-checking tool that scrapes figure listings from websites like **Solaris Japan**, extracts prices using **LangChain + OpenAI**, and intelligently picks the best match.

---

## ✨ Features

- 🔍 Scrapes real-time product listings from supported sites
- 💬 Uses an LLM agent to extract and interpret price information from messy HTML
- 🧠 Selects the most relevant or cheapest listing
- 🗂️ Supports single-product CLI mode and batch JSON input
- ⚙️ Modular and easy to extend to other figure stores

---

## 🧪 Example Command & Output
Command:
```
$ python main.py "Hatsune Miku Nendoroid" solaris
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

Currently, the only supported service is Solaris Japan, or ```solaris```. Other websites I've tried are much more resistant to scraping, or fetch completely irrelevant results.

-to be continued-

## TODO in order of importance:

- [x] finish README instructions to run
- [ ] make batch json input method work
- [ ] expand functionality to more websites than just Solaris Japan
- [ ] change output format into CSV
- [ ] add database integration to save results
- [ ] add web UI or a dashboard to show results
- [ ] add license to repo
