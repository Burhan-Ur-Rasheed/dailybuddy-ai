# DailyBuddy AI

DailyBuddy AI is a WhatsApp-based chatbot that helps with daily life, business advice, health tips, image generation, and emotional support.

## Features
- Daily problem-solving
- Friendly chatbot conversation
- Business idea generation
- Life and health advice
- AI-generated images via DALL·E
- 🎭 Custom tone support (romantic, sad, happy, angry, formal, friendly, witty, etc.)

## Setup
1. Clone this repo or upload files to your GitHub.
2. Copy `.env.example` to `.env` and fill in your credentials.
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run locally:
   ```
   python app.py
   ```

## Deploy on Render
1. Push code to GitHub
2. Go to https://render.com and create a new Web Service
3. Set:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Environment Variables: copy from `.env`

4. Set your Twilio sandbox webhook to:
```
https://your-render-url.onrender.com/whatsapp
```

## Usage
- First time users will see a welcome message.
- Set tone by sending: `tone: happy` or `tone: romantic`
- Request images like: `image: a dragon flying over mountains`