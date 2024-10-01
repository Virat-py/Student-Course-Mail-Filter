import re
import imaplib
import email
from email.header import decode_header
from groq import Groq
import os

# Email search keywords
check_keywords = {
    "col106", "hul243", "mtl106", "mtl180",
    "pyl102", "cvl100","sovikdas","dharmaraja",
    "amartyasengupta","minatide"
}

def check_text(text):
    """Checks if the given mail satisfies the filter based on keywords."""
    if not isinstance(text, str):
        return False
    clean_text = re.sub(r'[^a-z0-9]', '', text.lower())
    # Return True if any keyword is found in the cleaned text
    return any(key in clean_text for key in check_keywords)

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
def summarize(text):
    """Summarizes the given text using the Groq API."""
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "summarize in paragraph form in less than 400 words add newline for every 50 words,remove any empty lines from your response" + text,
            }
        ],
        model="llama3-70b-8192",
    )

    # Get the summary text from the response
    summary = chat_completion.choices[0].message.content

    # Split the summary into lines and remove the first line
    summary_lines = summary.splitlines()
    summary = "\n".join(summary_lines[1:])

    return summary.strip()

def get_email_body(msg):
    """Extract email body content."""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() in ["text/plain", "text/html"]:
                return part.get_payload(decode=True).decode("utf-8", errors="ignore")
    else:
        return msg.get_payload(decode=True).decode("utf-8", errors="ignore")
    return ""

def fetch_emails(limit=10):
    """Connect to IMAP server and fetch filtered emails."""
    imap_server = "imap.iitd.ac.in"
    email_user = "kerberos_id@iitd.ac.in"
    email_pass = "webmail_password"

    emails = []

    with imaplib.IMAP4_SSL(imap_server) as mail:
        # Login with email credentials
        mail.login(email_user, email_pass)
        mail.select("inbox")

        # Search for all emails
        _, data = mail.search(None, "ALL")
        email_ids = data[0].split()[::-1]  # Process the most recent emails first

        # Process up to the specified limit of emails
        for num in email_ids[:limit]:
            _, msg_data = mail.fetch(num, "(RFC822)")

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    # Decode the subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or "utf-8", errors="ignore")

                    # Get the email body
                    body = get_email_body(msg)

                    # Check if the subject or body contains specific keywords
                    if check_text(subject) or check_text(body):
                        # Append formatted email data
                        print(f"Subject: {subject}")
                        print(f"Body: {summarize(body)}")
                        print("-" * 50)

        # Logout from the server
        mail.logout()

fetch_emails(limit=40)
# checks relevant mails and summarizes the body from 40 most recent mails
