from flask import Flask, request, jsonify, send_file
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key="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")

with open("dokument.txt", "r", encoding="utf-8") as f:
    tekst = f.read()
print(tekst)
@app.route("/")
def home():
    return send_file("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    pitanje = request.json["question"]

    prompt = f"""
    Ti si edukativni asistent za djecu.

    Odgovaraj ISKLJUČIVO na osnovu ovog teksta:
    ----------------
    {tekst}
    ----------------

    Pravila:
    - Ako odgovor ne postoji u tekstu → reci: "Ne znam na osnovu ovog dokumenta."
    - Objasni jednostavno (kao za dijete)
    - Kratki odgovori

    Pitanje: {pitanje}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return jsonify({
        "answer": response.choices[0].message.content
    })

app.run()