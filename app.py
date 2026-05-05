import os
from flask import Flask, request, jsonify, send_file
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# učitavanje dokumenta
with open("dokument.txt", "r", encoding="utf-8") as f:
    tekst = f.read()


@app.route("/")
def home():
    return send_file("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    pitanje = request.json["question"]

    # provjera "hvala"
    user_text = pitanje.lower().strip()

    if "hvala" in user_text or "hvala ti" in user_text or "thanks" in user_text:
        return {"answer": "Nema na čemu 😊"}

    prompt = f"""
    Ti si edukativni asistent za djecu.

    Odgovaraj ISKLJUČIVO na osnovu ovog teksta:
    ----------------
    {tekst}
    ----------------

    Pravila:
    - Ako odgovor ne postoji u tekstu → reci: "Ne znam odgovor na tvoje pitanje."
    - Objasni jednostavno (kao za dijete)
    - Kratki odgovori

    Pitanje: {pitanje}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "answer": response.choices[0].message.content
    }


# Render fix (OBAVEZNO)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
