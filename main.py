import argparse
import os
from dotenv import load_dotenv
from youtube_leads import find_youtube_leads
from business_leads import find_business_leads
from ai_filter import filter_and_score_leads, generate_outreach_message
from outreach import send_email, send_telegram_alert

# Load environment variables from .env file
load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="AI Lead Generation and Outreach Tool")
    parser.add_argument("--niche", type=str, required=True, help="Business niche to target")
    parser.add_argument("--limit", type=int, default=5, help="Number of leads to fetch per source")
    parser.add_argument("--dry-run", action="store_true", help="Run without sending actual emails/alerts")
    args = parser.parse_args()

    niche = args.niche
    limit = args.limit
    dry_run = args.dry_run

    print(f"--- Starting Lead Generation for Niche: {niche} ---")

    # 1. Fetch Leads
    leads = []
    leads.extend(find_youtube_leads(niche, limit=limit))
    leads.extend(find_business_leads(niche, max_results=limit))

    if not leads:
        print("No leads found. Exiting.")
        return

    # 2. Score Leads with AI
    scored_leads = filter_and_score_leads(leads, niche)

    # 3. Process Leads (Outreach and Alerts)
    print("\n--- Processing Leads ---")
    for lead in scored_leads:
        print(f"\nLead: {lead['name']} ({lead['source']})")
        print(f"URL: {lead['url']}")
        print(f"AI Score: {lead['ai_score']}")
        print(f"AI Reason: {lead['ai_reason']}")

        if lead['ai_score'] > 60:
            print(">>> High quality lead identified!")

            message = generate_outreach_message(lead, niche)
            print(f"Generated Message:\n{message}")

            if dry_run:
                print("[Dry Run] Skipping actual outreach and alerts.")
            else:
                # Telegram Alert
                telegram_msg = f"<b>New Lead Found!</b>\nName: {lead['name']}\nSource: {lead['source']}\nScore: {lead['ai_score']}\nURL: {lead['url']}"
                send_telegram_alert(
                    telegram_msg,
                    os.getenv("TELEGRAM_BOT_TOKEN"),
                    os.getenv("TELEGRAM_CHAT_ID")
                )

                # Email Outreach
                if lead.get('email'):
                    smtp_config = {
                        'server': os.getenv("SMTP_SERVER", "smtp.gmail.com"),
                        'port': int(os.getenv("SMTP_PORT", 587)),
                        'user': os.getenv("SMTP_USER"),
                        'password': os.getenv("SMTP_PASS")
                    }
                    if smtp_config['user'] and smtp_config['password']:
                        send_email(lead['email'], f"Proposal for {lead['name']}", message, smtp_config)
                    else:
                        print("SMTP credentials missing, skipping email.")
                else:
                    print("No email found for this lead, skipping email outreach.")
        else:
            print("Lead score too low, skipping outreach.")

    print("\n--- Finished ---")

if __name__ == "__main__":
    main()
