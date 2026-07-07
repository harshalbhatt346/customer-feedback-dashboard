# 📊 Customer Feedback Dashboard

An interactive web dashboard built with **Streamlit**, **TextBlob**, and **Plotly** that
performs sentiment analysis on customer feedback and visualizes the results.

## ✨ Features

- Upload your own CSV of customer feedback, or use the built-in 30-row sample dataset
- Automatic sentiment scoring (Positive / Neutral / Negative) using TextBlob NLP
- KPI cards: total feedback, % positive, % negative, average sentiment score
- Interactive Plotly charts:
  - Sentiment distribution (donut chart)
  - Star rating vs. sentiment (box plot)
  - Sentiment trend over time (line chart)
  - Sentiment by product (stacked bar chart)
- Sidebar filters: product, sentiment, date range
- Most positive / most negative feedback highlights
- Full data table with download button (export analyzed CSV)
- Live "type your own feedback" sentiment checker

---

## 📁 Project Structure

```
customer-feedback-dashboard/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── data/
    └── customer_feedback.csv   # Sample dataset (30 customer reviews)
```

---

## ✅ Prerequisites

- **Python 3.9+** installed
- **VS Code** installed
- **VS Code Python extension** (recommended, not required)

Check your Python version:
```bash
python --version
```

---

## 🚀 Step-by-Step: Run in VS Code

### 1. Unzip and open the project
Unzip the downloaded folder, then open it in VS Code:
```bash
cd customer-feedback-dashboard
code .
```

### 2. Open a terminal inside VS Code
`Terminal` → `New Terminal` (or `` Ctrl+` ``)

### 3. (Recommended) Create a virtual environment
This keeps dependencies isolated from your system Python.

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` appear at the start of your terminal prompt.

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Download TextBlob's language corpora (one-time setup)
TextBlob needs some NLTK data files to perform sentiment analysis:
```bash
python -m textblob.download_corpora
```

### 6. Run the app
```bash
streamlit run app.py
```

### 7. View it in your browser
Streamlit will automatically print a local URL in the terminal, e.g.:
```
Local URL: http://localhost:8501
```
It should also auto-open in your default browser. If not, **Ctrl+Click** the link in
the VS Code terminal, or manually paste `http://localhost:8501` into your browser.

### 8. Stop the app
Go back to the VS Code terminal and press `Ctrl+C`.

---

## 📤 Using Your Own Data

Click **"Upload your own CSV"** in the sidebar. Your CSV must contain at minimum a
`feedback` column (the review text). These optional columns unlock extra charts:

| Column          | Type   | Required? | Used For                          |
|-----------------|--------|------------|------------------------------------|
| `feedback`      | text   | ✅ Yes     | Sentiment analysis                 |
| `date`          | date   | Optional   | Trend-over-time chart, date filter |
| `product`       | text   | Optional   | Sentiment-by-product chart, filter |
| `customer_name` | text   | Optional   | Shown in the data table            |
| `rating`        | number | Optional   | Rating-vs-sentiment box plot       |

Example minimal CSV:
```csv
feedback
"The app is great but crashes sometimes."
"Excellent service, very happy!"
```

---

## 🛠️ Troubleshooting

**"streamlit: command not found"**
→ Your virtual environment isn't activated, or Streamlit didn't install. Re-run
steps 3–4.

**TextBlob sentiment errors / missing corpora**
→ Re-run: `python -m textblob.download_corpora`

**Port 8501 already in use**
→ Run on a different port: `streamlit run app.py --server.port 8502`

**Blank/white page in browser**
→ Hard refresh (`Ctrl+Shift+R`), or check the VS Code terminal for a Python traceback.

**CSV upload error: "must contain a column named 'feedback'"**
→ Rename your review-text column to exactly `feedback` (lowercase).

---

## 📦 Tech Stack

| Library    | Purpose                          |
|------------|-----------------------------------|
| Streamlit  | Web app framework / UI            |
| TextBlob   | NLP sentiment analysis (polarity & subjectivity) |
| Plotly     | Interactive charts                |
| Pandas     | Data loading & manipulation       |

---

Built and verified end-to-end — sentiment pipeline tested against the sample
dataset and the app confirmed to launch cleanly on `localhost:8501`.
