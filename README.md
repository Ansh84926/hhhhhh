# AI Lead Generation & Outreach Tool

This tool automates the process of finding business leads, scoring them using AI, and initiating outreach—all without requiring expensive API keys.

## Features

- **Lead Finding**: Automatically finds leads from YouTube and Google (DuckDuckGo).
- **AI Filtering**: Uses GPT4Free (`g4f`) to score leads based on relevance to your niche.
- **Auto Outreach**: Generates personalized messages and can send them via Email.
- **Notifications**: Sends instant alerts to a Telegram Bot when a high-quality lead is found.
- **100% Free**: Built using free libraries and tools (no Google Maps API, no YouTube Data API, no OpenAI API keys required).

## Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment variables (create a `.env` file):
   ```env
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASS=your-app-password
   TELEGRAM_BOT_TOKEN=your-bot-token
   TELEGRAM_CHAT_ID=your-chat-id
   ```

## Usage

Run the main script with your target niche:

```bash
python main.py --niche "Video Editing Services" --limit 10
```

To test without sending emails:

```bash
python main.py --niche "Web Design" --limit 5 --dry-run
```

## How it works (Flowchart)

1. **Step 1 - Lead dhandho**: Searches YouTube (via scrapetube) and Web (via ddgs).
2. **Step 2 - AI Filter**: Scores leads and generates personalized messages using free AI models.
3. **Step 3 - Auto Outreach**: Sends emails via SMTP if an email address was found.
4. **Step 4 - Telegram Alert**: Notifies you immediately via Telegram for high-score leads.
5. **Step 5 - Close Deal**: You take over once the lead replies!
