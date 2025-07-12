from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai, os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

openai.api_key = os.getenv("sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx")

# Temporary tone memory (not persistent)
user_tones = {}

welcome_message = (
    "👋 Welcome to DailyBuddy AI!
"
    "I'm here to help with your daily life, relationships, business, health, and more.
"
    "You can even ask me to generate images by typing:
"
    "  image: a sunset over mountains

"
    "🎭 Choose a tone for our chat: romantic, sad, happy, angry, formal, friendly, witty, professional, motivational, humorous.
"
    "Send: tone: happy (or any other tone)"
)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    from_number = request.values.get("From", "")
    incoming = request.values.get("Body", "").strip()
    resp = MessagingResponse()
    msg = resp.message()

    if from_number not in user_tones:
        msg.body(welcome_message)
        user_tones[from_number] = "friendly"
        return str(resp)

    if incoming.lower().startswith("tone:"):
        selected_tone = incoming.split(":", 1)[1].strip().lower()
        user_tones[from_number] = selected_tone
        msg.body(f"✅ Tone set to: {selected_tone}")
        return str(resp)

    if incoming.lower().startswith("image:"):
        prompt = incoming.split(":", 1)[1].strip()
        url = generate_image(prompt)
        msg.media(url)
        return str(resp)

    reply = talk_to_gpt(incoming, user_tones.get(from_number, "friendly"))
    msg.body(reply)
    return str(resp)

def talk_to_gpt(text, tone):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a {tone} assistant. Reply in a {tone} tone and try to match the user's mood."
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"🤖 Error: {e}"

def generate_image(desc):
    try:
        img = openai.Image.create(prompt=desc, n=1, size="512x512")
        return img["data"][0]["url"]
    except Exception:
        return "https://via.placeholder.com/512?text=Error"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
