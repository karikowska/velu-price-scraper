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
$ python main_flexible.py "Hatsune Miku Nendoroid" solaris
```

Sample output:
```
🛒 Best match for 'Hatsune Miku Nendoroid' on solaris: The price of the "Hatsune Miku - Racing 2023 Ver." is ¥6980 JPY.
```

---

## 🚀 Getting Started

### 1. Install dependencies

```
pip install -r requirements.txt
```

You'll also need an OpenAI API key. Set it in your cmd using ```export``` or place within a .env file as such:
```
OPENAI_API_KEY=...
```

-to be continued-

## TODO in order of importance:

- finish README instructions to run
- make batch json input method work
- expand functionality to more websites than just Solaris Japan
- change output format into CSV
- add web UI or a dashboard to show results
- add license to repo
