# 🌆 Scranton Visitor Guide

![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-60%25+-blue)
![Streamlit](https://img.shields.io/badge/streamlit-app-orange)

## 🔗 Live App
👉 https://scranton-visitor-guide.streamlit.app/

---

## 📌 Project Overview

The **Scranton Visitor Guide** is an interactive web application built with Streamlit that helps users discover activities in Scranton, Pennsylvania.

The system combines:
- Web scraping of real activity data
- SQLite database storage for persistence
- Interactive Streamlit UI
- Data visualization of activity ratings
- AI-powered recommendations using Azure OpenAI

Users can browse activities, leave ratings and comments, and receive personalized recommendations based on their input and stored data.

---

## ⚙️ Features

- 🔎 Scraped local activities database
- 🗄️ SQLite persistent storage
- ⭐ Rate and review activities
- 💬 Comment system per activity
- 📊 Activity rating visualization
- 🤖 AI-powered activity recommendations
- 🌦️ Weather-based suggestion logic (indoor/outdoor)

---

## 🧠 AI (ChatGPT / Azure OpenAI) Integration

This project uses **Azure OpenAI (GPT model)** to power an intelligent recommendation assistant inside the Streamlit app.

### How it works:
- The app retrieves all activities from the SQLite database
- Each activity includes:
  - Name
  - Category
  - Rating
  - Comments
- This structured data is passed to the AI as context
- The AI generates:
  - 3–5 personalized recommendations
  - Explanations for each suggestion

### AI Rules:
- Rainy weather → indoor activities
- Sunny weather → outdoor activities
- Cold weather → mixed indoor/short outdoor activities
- Only uses real database activities (no hallucinations)

---

## 🧰 Tech Stack

- Python 🐍
- Streamlit
- SQLite3
- BeautifulSoup / Requests (web scraping)
- Azure OpenAI API
- Pytest (testing)

---

## 📦 Installation & Setup

### 📥 Clone repository
```bash
git clone https://github.com/YOUR_USERNAME/scranton-visitor-guide.git
cd scranton-visitor-guide
```
## 🧪 Create virtual environment
```bash
python -m venv venv
```
## ▶️ Activate virtual environment
```bash
venv\Scripts\activate
```
# Mac/Linux:
```bash
source venv/bin/activate
```
## 📦 Install dependencies
```Bash
pip install -r requirements.txt
```
## ▶️ Running the Streamlit App Locally

After installing dependencies, run the app with:

```bash
streamlit run app.py

```

## ➕ Add this section: “Running Tests”

```markdown
## 🧪 Running Tests

To run the full test suite:

```bash
pytest

pytest --cov

```

## ➕ Add this section: “Project Structure”

```markdown
## 📁 Project Structure

scranton-visitor-guide/
│
├── app.py                     # Streamlit UI
├── scraper.py                 # Web scraper
├── stored_scraped_data.py     # SQLite database logic
├── tests/                     # Pytest test suite
├── requirements.txt
└── README.md

## 🗄️ Database Schema

The SQLite database contains two tables:

### `activities`
- id (INTEGER, PK)
- name (TEXT)
- category (TEXT)
- link (TEXT)
- rating_sum (INTEGER)
- rating_count (INTEGER)

### `comments`
- id (INTEGER, PK)
- activity_id (INTEGER, FK → activities.id)
- comment (TEXT)

## 🕸️ Web Scraper Overview

The scraper collects:
- Activity name
- Category
- Wikipedia link

It stores the scraped data into the SQLite database using
