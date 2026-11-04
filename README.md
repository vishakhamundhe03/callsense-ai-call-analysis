# 🎙️ CallSense – AI-Powered Customer Call Analysis & Admin Portal

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-Backend-black)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue)
![AI](https://img.shields.io/badge/AI-Call%20Analysis-purple)

## 🚀 Overview

**CallSense** is an AI-powered customer call analysis and admin portal designed to transform customer conversations into meaningful business insights.

The application allows users to manage customer calls, analyze conversation transcripts, identify customer sentiment, estimate purchase intent, and generate detailed reports through an interactive dashboard.

The project demonstrates how **AI capabilities, backend APIs, databases, audio processing, and a web dashboard** can be integrated into a complete application.

---

## ✨ Key Features

### 🎙️ Call Management
- Upload and manage customer call records
- Store call information in a database
- View previously analyzed calls
- Delete unwanted or incorrect call records

### 📝 Transcript Analysis
- Analyze customer conversation transcripts
- Edit or fix incorrect conversation text
- Re-analyze calls after updating the transcript

### 😊 Sentiment Analysis
The system analyzes customer conversations and identifies the overall sentiment, such as:

- Positive
- Neutral
- Negative

### 📊 Purchase Intent Scoring
CallSense estimates the customer's purchase interest based on conversation signals and keywords.

The score helps identify whether the customer shows:

- Low purchase interest
- Medium purchase interest
- High purchase interest

> ⚠️ The current purchase intent score is a transparent heuristic-based estimate and should not be considered a trained or calibrated machine learning probability.

### 💡 AI-Powered Insights
The system generates useful insights from customer conversations to help understand:

- Customer sentiment
- Purchase interest
- Important conversation signals
- Customer concerns and intent

### 🔍 Search and Filter
The admin dashboard allows users to:

- Search calls
- Filter call records
- Explore previous analyses
- View detailed call information

### 🔄 Re-analysis
Users can update a conversation transcript and analyze it again to generate updated results.

### 📄 Report Generation
Generate downloadable reports containing important call analysis information and insights.

---

# 🏗️ System Architecture

```text
                ┌─────────────────────┐
                │   Customer Call     │
                │ Audio / Transcript  │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │   Flask Backend     │
                │    REST APIs        │
                └──────────┬──────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
 ┌────────────────┐ ┌──────────────┐ ┌─────────────────┐
 │ Transcript     │ │ Sentiment    │ │ Purchase Intent │
 │ Processing     │ │ Analysis     │ │ Scoring         │
 └────────────────┘ └──────────────┘ └─────────────────┘
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                ┌─────────────────────┐
                │     SQLite DB       │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │   Admin Dashboard   │
                │ HTML / CSS / JS     │
                └─────────────────────┘
```

---

# 🛠️ Technologies Used

## Backend

- **Python**
- **Flask**
- **REST APIs**

## Database

- **SQLite**

## AI / NLP

- **Transformers**
- **PyTorch**
- Sentiment Analysis
- Heuristic-Based Purchase Intent Scoring

## Audio Processing

- **Faster-Whisper**
- Speech-to-Text Transcription

## Frontend

- **HTML**
- **CSS**
- **JavaScript**

## Development Tools

- **Git**
- **GitHub**
- **Pytest**

---

# 📁 Project Structure

```text
CallSense/
│
├── app.py
├── database.py
├── ai_engine.py
├── check_db.py
│
├── requirements.txt
├── requirements-audio.txt
├── requirements-dev.txt
│
├── templates/
│   ├── index.html
│   └── easy.html
│
├── tests/
│   └── test_api.py
│
├── samples/
│
├── uploads/
│
└── README.md
```

---

# ⚙️ Installation

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/vishakhamundhe03/CallSense.git
```

Move into the project directory:

```bash
cd CallSense
```

---

## 2️⃣ Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate the environment:

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

Install the main dependencies:

```bash
pip install -r requirements.txt
```

For development and testing dependencies:

```bash
pip install -r requirements-dev.txt
```

For optional audio transcription support:

```bash
pip install -r requirements-audio.txt
```

---

# ▶️ Running the Application

Start the Flask application:

```bash
python app.py
```

After the server starts, open your browser and visit:

```text
http://127.0.0.1:5000/
```

For the simplified admin dashboard:

```text
http://127.0.0.1:5000/easy
```

---

# 🎯 Application Workflow

```text
Customer Call
      ↓
Upload Audio / Add Transcript
      ↓
Transcript Processing
      ↓
Sentiment Analysis
      ↓
Purchase Intent Analysis
      ↓
Generate Customer Insights
      ↓
Store Results in SQLite
      ↓
Display Results on Dashboard
      ↓
Generate Report
```

---

# 🤖 AI Analysis

## Sentiment Analysis

The application analyzes customer conversations to understand the overall emotional tone.

Possible results include:

| Sentiment | Meaning |
|---|---|
| 😊 Positive | Customer shows positive interest |
| 😐 Neutral | Customer is undecided or informational |
| 😟 Negative | Customer expresses dissatisfaction or concern |

---

## Purchase Intent Analysis

The system analyzes conversation signals to estimate customer purchase interest.

For example:

### High Intent

```text
"I am interested. Please tell me the price and how I can purchase it."
```

### Medium Intent

```text
"The product sounds interesting. I will think about it."
```

### Low Intent

```text
"I am not interested right now."
```

The current implementation uses a **rule-based and heuristic scoring approach**.

A production-grade machine learning model would require:

- Historical customer data
- Labeled outcomes
- Feature engineering
- Model training
- Validation
- Probability calibration
- Continuous monitoring

---

# 🎙️ Audio Transcription

CallSense supports optional audio transcription using **Faster-Whisper**.

Workflow:

```text
Audio File
    ↓
Faster-Whisper
    ↓
Generated Transcript
    ↓
AI Analysis
    ↓
Sentiment + Purchase Intent + Insights
```

Audio processing is optional and can require additional dependencies depending on the environment.

---

# 📊 Admin Dashboard

The dashboard allows users to:

- View customer calls
- Search call records
- Filter analysis results
- View sentiment information
- Check purchase intent
- Open detailed call analysis
- Fix incorrect conversation text
- Re-analyze conversations
- Delete unwanted calls
- Generate reports

---

# 🗄️ Database

The application uses **SQLite** for storing call information and analysis results.

Typical stored information includes:

- Call details
- Customer information
- Conversation transcript
- Sentiment result
- Purchase intent score
- Analysis insights

The database is stored locally and should not be committed to the public GitHub repository if it contains real or sensitive customer data.

---

# 🧪 Testing

Run the automated tests using:

```bash
pytest
```

Or:

```bash
python -m pytest
```

The project includes API testing to verify that important application functionality is working correctly.

---

# 🔒 Privacy and Security

The following types of files should not be uploaded to a public GitHub repository:

- Private customer recordings
- Sensitive customer data
- Local databases
- API keys
- Environment variables
- Personal credentials

Use a `.gitignore` file to exclude sensitive files and folders.

Example:

```text
instance/
uploads/
.env
__pycache__/
venv/
```

---

# 📈 Future Improvements

Some future improvements planned for CallSense include:

- 🎯 Train a real machine learning model using historical labeled call data
- 📞 Real-time call analysis
- 🧠 Advanced LLM-based conversation analysis
- 📊 Improved analytics dashboard
- ☁️ Cloud database integration
- 🔐 User authentication and role-based access
- 🐳 Docker containerization
- ☁️ Cloud deployment
- 📡 Real-time API integration
- 📈 Advanced data visualization
- 🔔 Customer follow-up recommendations

---

# 💡 What I Learned

Building CallSense helped me gain practical experience with:

- Building REST APIs using Flask
- Database integration using SQLite
- AI and NLP integration
- Sentiment analysis
- Audio transcription workflows
- Purchase intent scoring
- Backend and frontend integration
- Report generation
- Automated testing
- Git and GitHub workflows

---

# ⚠️ Important Note

CallSense is a **learning and portfolio project** created to demonstrate the integration of AI capabilities into a complete web application.

The current purchase intent scoring system is **heuristic-based** and is intended for demonstration purposes.

It should not be represented as a fully trained, validated, or calibrated machine learning probability model.

---

# 👩‍💻 Author

**Vishakha Mundhe**

Aspiring Data Engineer | Python | SQL | Data Engineering | AI Projects

🔗 GitHub: https://github.com/vishakhamundhe03

🔗 Project Repository: https://github.com/vishakhamundhe03/CallSense

---

# ⭐ Support

If you found this project interesting, please consider giving the repository a **⭐ star**!

Your feedback and suggestions are always welcome. 😊
