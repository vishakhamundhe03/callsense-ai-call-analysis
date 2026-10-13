"""Demo analysis engine. Replace the heuristic model with a trained model for production."""
import re
from datetime import date

CALLS = [
    {
        "id": "CALL-001", "customer": "Aarav Sharma", "product": "Premium Wireless Headphones",
        "date": "2026-10-10", "duration": "02:14", "audio": "/static/audio/CALL-001.wav",
        "transcript": [
            {"speaker":"Agent","text":"Thank you for calling SoundNest. How can I help you today?"},
            {"speaker":"Customer","text":"I saw your premium wireless headphones online. The reviews look great and I like the noise cancellation."},
            {"speaker":"Agent","text":"They have active noise cancellation and a two-year warranty. I can also explain today's offer."},
            {"speaker":"Customer","text":"That sounds good. Is the discount available today, and can I get delivery by Friday?"},
            {"speaker":"Agent","text":"Yes, the current offer is available today, and delivery by Friday is available in your area."},
            {"speaker":"Customer","text":"Excellent. Please send me the checkout link. I am ready to order."}
        ],
        "intent":"High", "objections": [], "behavior":"The customer expresses clear product preference, asks about offer and delivery, and explicitly requests the checkout link."
    },
    {
        "id": "CALL-002", "customer": "Priya Nair", "product": "Smart Fitness Watch",
        "date": "2026-10-10", "duration": "03:02", "audio": "/static/audio/CALL-002.wav",
        "transcript": [
            {"speaker":"Agent","text":"Hello, this is the FitTrack product team. What would you like to know?"},
            {"speaker":"Customer","text":"I am comparing a few fitness watches. Does this one track sleep and heart rate?"},
            {"speaker":"Agent","text":"Yes, it tracks sleep, heart rate, workouts, and daily activity."},
            {"speaker":"Customer","text":"Okay, that is useful. I need to compare the battery life and price with another model first."},
            {"speaker":"Agent","text":"Of course. I can send you a comparison sheet and product details."},
            {"speaker":"Customer","text":"Please send the details. I will think about it and decide later."}
        ],
        "intent":"Medium", "objections":["Comparing competitors","Needs more information"], "behavior":"The customer is interested enough to ask feature questions but is still comparing alternatives and postponing the decision."
    },
    {
        "id": "CALL-003", "customer": "Rohan Mehta", "product": "Ergonomic Office Chair",
        "date": "2026-10-11", "duration": "02:48", "audio": "/static/audio/CALL-003.wav",
        "transcript": [
            {"speaker":"Agent","text":"Thank you for contacting WorkSpace Living. How may I assist?"},
            {"speaker":"Customer","text":"The chair looks nice, but it is much more expensive than I expected."},
            {"speaker":"Agent","text":"It has adjustable lumbar support and a five-year frame warranty. We may have payment options."},
            {"speaker":"Customer","text":"I have seen similar chairs for less. I am not sure the extra cost is worth it."},
            {"speaker":"Agent","text":"I understand. I can explain the differences or check whether a promotion applies."},
            {"speaker":"Customer","text":"No, I do not want to spend that much right now. Thank you."}
        ],
        "intent":"Low", "objections":["Price too high","Cheaper competitors","No immediate budget"], "behavior":"The customer repeatedly raises price concerns, questions the value difference, and declines further purchase discussion."
    },
    {
        "id": "CALL-004", "customer": "Meera Iyer", "product": "Organic Skincare Starter Kit",
        "date": "2026-10-11", "duration": "02:31", "audio": "/static/audio/CALL-004.wav",
        "transcript": [
            {"speaker":"Agent","text":"Hi, thank you for calling PureLeaf. How can I help with our skincare kit?"},
            {"speaker":"Customer","text":"I am interested, but my skin is sensitive. Are the ingredients listed clearly?"},
            {"speaker":"Agent","text":"Yes, the full ingredient list is on the product page. We recommend checking it carefully and patch testing."},
            {"speaker":"Customer","text":"That is reassuring. Is there a return policy if it does not suit me?"},
            {"speaker":"Agent","text":"Unopened products can be returned within the stated return window. I can send the policy and ingredients."},
            {"speaker":"Customer","text":"Please send both. I would like to review them before deciding."}
        ],
        "intent":"Medium", "objections":["Sensitive-skin suitability","Needs to review return policy"], "behavior":"The customer shows measured interest and asks practical risk-reduction questions, but wants to verify ingredients and policy before buying."
    }
]

POSITIVE = {"great":2, "excellent":3, "love":3, "good":1, "ready to order":4, "reassuring":2, "interested":1, "useful":1, "please send":1, "sounds good":2, "like":1, "thank":0}
NEGATIVE = {"expensive":-2, "not sure":-1, "not":-1, "no":-2, "less":-1, "concern":-2, "problem":-2, "disappointed":-3, "do not":-2, "don't":-2, "too high":-3, "not worth":-3}
BUY_WORDS = ["ready to order", "checkout link", "buy now", "place an order", "purchase today", "order today"]
INTEREST_WORDS = ["interested", "price", "delivery", "discount", "feature", "ingredients", "warranty", "send", "available"]
OBJECTION_WORDS = ["expensive", "not sure", "compare", "comparing", "later", "return policy", "sensitive", "less", "not worth", "do not want"]

def get_calls():
    return CALLS

def get_call(call_id):
    return next((c for c in CALLS if c["id"] == call_id), None)

def analyze_call(call):
    transcript_text = " ".join(x["text"] for x in call["transcript"]).lower()
    score = 0
    for word, weight in POSITIVE.items():
        if word in transcript_text: score += weight
    for word, weight in NEGATIVE.items():
        if word in transcript_text: score += weight
    sentiment = "Positive" if score >= 4 else ("Negative" if score <= -3 else "Neutral")
    buy_hits = sum(1 for term in BUY_WORDS if term in transcript_text)
    interest_hits = sum(1 for term in INTEREST_WORDS if term in transcript_text)
    objection_hits = sum(1 for term in OBJECTION_WORDS if term in transcript_text)
    # Transparent demo scoring, deliberately not presented as calibrated probability.
    raw = 20 + buy_hits * 28 + min(interest_hits, 5) * 6 - min(objection_hits, 5) * 7 + max(-10, min(10, score))
    probability = max(5, min(95, raw))
    insights = []
    if buy_hits: insights.append("Explicit buying language or a direct next-step request was detected.")
    if interest_hits >= 2: insights.append("The customer asked product, offer, availability, or follow-up questions.")
    if objection_hits: insights.append("Potential friction was detected: " + ", ".join(call["objections"]) + ".")
    if not insights: insights.append("No strong buying signal was detected; continue discovery.")
    if sentiment == "Positive":
        insights.append("The language is mostly positive or indicates progress toward a decision.")
    elif sentiment == "Negative":
        insights.append("Negative language or unresolved concerns may be blocking conversion.")
    else:
        insights.append("The customer appears to be evaluating options rather than committing.")
    return {
        **call,
        "sentiment": sentiment,
        "sentiment_score": score,
        "purchase_probability": probability,
        "purchase_intent": call["intent"],
        "key_insights": insights,
        "customer_behavior": call["behavior"],
        "recommended_action": (
            "Send checkout link and confirm delivery details." if probability >= 70 else
            "Follow up with requested information and address the main concern." if probability >= 40 else
            "Avoid pressure; offer a lower-cost option or reconnect only if the customer opts in."
        ),
        "method": "Lexicon/rule-based sentiment plus transparent heuristic purchase score",
        "transcript_text": transcript_text
    }
