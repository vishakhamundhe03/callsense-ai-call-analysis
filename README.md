# CallSense — AI-Powered Call Analysis & Admin Portal

CallSense is a full-stack web application built with Flask that provides a dashboard for analyzing customer conversations. It includes a JSON API, sentiment analysis, purchase-interest scoring, sample audio playback, and downloadable PDF reports.

## Features

- Responsive admin dashboard
- Four scripted sample customer interactions
- Sentiment classification: Positive, Neutral, or Negative
- Rule-based purchase-interest scoring
- Sample audio playback
- Downloadable PDF reports
- REST API endpoints for call data and analysis

## Requirements

- Python 3.10 or newer
- pip

## Run Locally

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate the virtual environment

**Windows PowerShell**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
python app.py
```


## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Check application health |
| GET | `/api/calls` | Retrieve all calls with their analysis |
| GET | `/api/calls/CALL-001` | Retrieve a specific call and its analysis |
| GET | `/api/reports/CALL-001.pdf` | Generate and download a PDF report for a call |

## Project Structure

```text
callsense-ai-call-analysis/
├── app.py
├── analysis_engine.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── styles.css
    ├── js/
    │   └── app.js
    └── audio/
        ├── CALL-001.wav
        ├── CALL-002.wav
        ├── CALL-003.wav
        └── CALL-004.wav
```

## How the Analysis Works

### 1. Sentiment Analysis

The application uses a rule-based approach that combines a small positive and negative phrase lexicon with scoring rules. Based on the resulting score, each conversation is classified as:

- **Positive** — The conversation contains positive language or customer feedback.
- **Neutral** — The conversation contains mixed or relatively neutral language.
- **Negative** — The conversation contains negative language or customer concerns.

This approach is transparent and easy to understand. However, it may misinterpret sarcasm, negation, context-dependent phrases, and multilingual conversations.

### 2. Purchase-Interest Score

The purchase-interest score estimates how strongly a customer's conversation indicates an interest in buying a product.

**Important:** This is a rule-based scoring heuristic, not a trained machine-learning prediction model. The score is intended for demonstration purposes and is not a calibrated probability of an actual purchase.

#### Types of Signals

**Buying Signals**

These indicate a strong intention to purchase.

Examples:
- "Please send me the checkout link."
- "I am ready to order."

Buying signals increase the score.

**Interest Signals**

These indicate that the customer is exploring the product or considering a purchase.

Examples:
- Asking about price
- Asking about product features
- Enquiring about delivery or warranty

Interest signals can increase the score.

**Objections**

These indicate concerns or reasons the customer might delay or avoid a purchase.

Examples:
- "It is too expensive."
- "I will decide later."

Objections decrease the score.

#### Scoring Formula

The application calculates the score approximately using the following formula:

\[
P = 20 + 28B + 6I - 7O + S
\]

Where:

- \(P\) = Purchase-interest score
- \(B\) = Number of detected buying signals
- \(I\) = Number of detected interest signals, capped at 5
- \(O\) = Number of detected objections, capped at 5
- \(S\) = Limited contribution from the sentiment score

The final score is constrained to a range of 5% to 95%.

This formula is a heuristic designed for a simple demonstration. The resulting percentage should not be interpreted as a statistically validated probability that the customer will make a purchase.

#### What Is a Heuristic?

A **heuristic** is a practical rule of thumb used to solve a problem or make a decision quickly. It relies on simple guiding principles rather than a complete analysis of every possible factor.

In this project, the heuristic uses buying signals, interest signals, objections, and sentiment to produce an easy-to-understand purchase-interest score.

## Audio Note

The sample audio assets are intended for demonstration of the scripted customer interactions. Their availability and playback depend on the included audio files. For a realistic production application, replace sample audio with appropriately consented customer recordings.

## Limitations

- The application uses scripted sample conversations rather than automatically transcribing real customer calls.
- Sentiment analysis relies on predefined phrases and rules.
- Purchase-interest scores are heuristic estimates, not validated machine-learning predictions.
- Real-world performance may vary depending on language, context, and customer behavior.

## Future Improvements

1. Add authentication and role-based access control.
2. Store call data and analysis in PostgreSQL.
3. Store recordings securely using private object storage.
4. Integrate speech-to-text transcription, such as Whisper or an approved transcription API.
5. Introduce validated NLP or machine-learning models and report their limitations.
6. Implement consent management, data retention and deletion policies, encryption, audit logs, and personally identifiable information (PII) redaction.
7. Evaluate model performance using appropriately consented and representative data.

## Disclaimer

CallSense is a learning and demonstration project. Its sentiment labels and purchase-interest scores should not be treated
