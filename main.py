import time
import schedule
import os
from dotenv import load_dotenv
from search_tool import SearchTool
from agent_core import AgentCore
from email_service import EmailService

load_dotenv()

class ResearchAutomation:
    def __init__(self):
        self.search_tool = SearchTool(num_results=5)
        self.agent = AgentCore(preferred_provider=os.getenv("PREFERRED_PROVIDER", "openai"))
        self.mailer = EmailService()
        self.recipient = os.getenv("RECIPIENT_EMAIL")

    def run_research_task(self, topic):
        print(f"Starting research sequence for: {topic}")
        
        # 1. Search and Scrape
        search_data = self.search_tool.search_and_scrape(topic)
        if not search_data:
            print("No search data found.")
            return

        # 2. Analyze
        context = "\n\n".join([f"Source: {d['url']}\nContent: {d['content']}" for d in search_data])
        report = self.agent.analyze(topic, context)

        # 3. Email Report
        subject = f"Research Report: {topic}"
        success = self.mailer.send_email(self.recipient, subject, report)
        
        if success:
            print("Research task completed and emailed.")
        else:
            print("Research task failed at email stage.")

    def run_reminder_task(self, message):
        print(f"Sending reminder: {message}")
        subject = "Automated Reminder"
        self.mailer.send_email(self.recipient, subject, message)

def daily_research():
    automation = ResearchAutomation()
    topic = os.getenv("DAILY_RESEARCH_TOPIC", "Latest AI News")
    automation.run_research_task(topic)

if __name__ == "__main__":
    load_dotenv()
    print("Research Automation Agent Started...")
    
    # Example: Run immediately for testing
    # daily_research()

    # Schedule: Every day at 9:00 AM
    schedule.every().day.at("09:00").do(daily_research)

    while True:
        schedule.run_pending()
        time.sleep(60)
