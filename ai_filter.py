import g4f
from g4f.client import Client
import re

def filter_and_score_leads(leads, niche):
    """
    Uses AI to score leads and filter them based on relevance to the niche.
    """
    client = Client()
    scored_leads = []

    print(f"AI is scoring {len(leads)} leads...")

    for lead in leads:
        try:
            # We provide the lead name and description/url to the AI
            prompt = f"""
            Analyze this lead for a business offering services in the '{niche}' niche.
            Lead Name: {lead.get('name')}
            Lead URL: {lead.get('url')}
            Description: {lead.get('description', 'N/A')}

            Provide a score from 0 to 100 on how likely they are to be interested in professional services related to {niche}.
            Also provide a very short reason for the score.

            Return ONLY in this format:
            Score: [number]
            Reason: [reason]
            """

            # Using specific providers that are usually free and more stable
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.choices[0].message.content

            # Simple parsing
            score = 0
            reason = "Could not parse AI response."

            for line in content.split('\n'):
                if line.startswith('Score:'):
                    try:
                        score = int(re.search(r'\d+', line).group())
                    except:
                        pass
                if line.startswith('Reason:'):
                    reason = line.replace('Reason:', '').strip()

            lead['ai_score'] = score
            lead['ai_reason'] = reason
            scored_leads.append(lead)

        except Exception as e:
            # print(f"  Error scoring lead {lead.get('name')}: {e}")
            lead['ai_score'] = 50 # Default middle score if AI fails
            lead['ai_reason'] = "AI scoring unavailable, using default."
            scored_leads.append(lead)

    # Sort by score descending
    scored_leads.sort(key=lambda x: x.get('ai_score', 0), reverse=True)
    return scored_leads

def generate_outreach_message(lead, niche):
    """
    Generates a personalized outreach message for a lead.
    """
    client = Client()
    try:
        prompt = f"""
        Write a professional and friendly outreach message to {lead.get('name')}.
        We are offering services in: {niche}.
        The message should be short, personalized based on their name/business, and have a clear call to action.
        Mention that we saw their work at {lead.get('url')}.
        Keep it under 100 words.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"Hi {lead.get('name')},\n\nI saw your work at {lead.get('url')} and was very impressed. I specialize in {niche} and would love to help you scale your business. Are you available for a quick chat next week?\n\nBest regards,\nYour Name"

if __name__ == "__main__":
    # Test
    mock_leads = [
        {'name': 'Cool Cooking Channel', 'url': 'https://youtube.com/c/coolcooking', 'description': 'I make videos about fast food and healthy recipes.'},
        {'name': 'Tech Reviews', 'url': 'https://youtube.com/c/techreviews', 'description': 'Unboxing the latest smartphones.'}
    ]
    results = filter_and_score_leads(mock_leads, "Video Editing Services")
    for lead in results:
        print(f"Name: {lead['name']}, Score: {lead['ai_score']}, Reason: {lead['ai_reason']}")
        print(f"Message:\n{generate_outreach_message(lead, 'Video Editing Services')}\n")
