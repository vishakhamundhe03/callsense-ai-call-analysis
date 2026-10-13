from flask import Flask, jsonify, render_template, send_file, abort
from analysis_engine import analyze_call, get_calls, get_call
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import datetime

app = Flask(__name__)

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/api/calls")
def calls():
    return jsonify([analyze_call(c) for c in get_calls()])

@app.get("/api/calls/<call_id>")
def call_detail(call_id):
    call = get_call(call_id)
    if not call:
        abort(404, description="Call not found")
    return jsonify(analyze_call(call))

@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "AI Call Analysis API"})

@app.get("/api/reports/<call_id>.pdf")
def report(call_id):
    call = get_call(call_id)
    if not call:
        abort(404, description="Call not found")
    a = analyze_call(call)
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=44, leftMargin=44, topMargin=42, bottomMargin=42)
    styles = getSampleStyleSheet()
    story = [Paragraph("Customer Call Analysis Report", styles["Title"]),
             Paragraph(f"{a['customer']} · {a['product']} · {a['date']}", styles["Heading2"]),
             Spacer(1, 10)]
    rows = [
        ["Call ID", a["id"]],
        ["Duration", a["duration"]],
        ["Sentiment", a["sentiment"]],
        ["Purchase probability", f"{a['purchase_probability']}%"],
        ["Intent", a["purchase_intent"]],
        ["Recommended action", a["recommended_action"]],
    ]
    table = Table(rows, colWidths=[145, 350])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#eef2ff")),
        ("TEXTCOLOR", (0,0), (-1,-1), colors.HexColor("#172033")),
        ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#d8deea")),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
        ("PADDING", (0,0), (-1,-1), 8),
    ]))
    story += [table, Spacer(1, 14), Paragraph("Call transcript", styles["Heading2"])]
    for line in a["transcript"]:
        story.append(Paragraph(f"<b>{line['speaker']}:</b> {line['text']}", styles["BodyText"]))
        story.append(Spacer(1, 5))
    story += [Spacer(1, 8), Paragraph("Key insights", styles["Heading2"])]
    for insight in a["key_insights"]:
        story.append(Paragraph("• " + insight, styles["BodyText"]))
        story.append(Spacer(1, 4))
    story += [Spacer(1, 8), Paragraph("Customer behavior", styles["Heading2"]),
              Paragraph(a["customer_behavior"], styles["BodyText"]),
              Spacer(1, 8), Paragraph("Analysis method and limitations", styles["Heading2"]),
              Paragraph("Sentiment is estimated from transcript language using a lightweight lexicon/rule-based scorer. Purchase probability is a demo heuristic based on expressed intent, price/availability questions, objections, and positive/negative language. These percentages are illustrative, not calibrated probabilities or a validated production ML model. Validate against labeled calls before business use.", styles["BodyText"]),
              Spacer(1, 10), Paragraph(f"Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["Italic"])]
    doc.build(story)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"{call_id}-analysis-report.pdf", mimetype="application/pdf")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
