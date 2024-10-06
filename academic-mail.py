import streamlit as st
import imaplib
import email
from email.header import decode_header
import re

# Email search keywords
check_keywords = {
    "col106", "hul243", "mtl106", "mtl180",
    "pyl102", "cvl100", "sovikdas", "dharmaraja",
    "amartyasengupta", "minatide"
}
filter="0123456789abcdefghijklmnopqrstuvwxyz"
def check_text(text):
    """Checks if the given mail satisfies the filter based on keywords."""
    if not isinstance(text, str):
        return False
    temp=""
    text=text.lower()
    for i in text:
        if i in filter:
            temp+=i
    for check in check_keywords:
        if check in temp:
            return True
    return False


def get_email_body(msg):
    """Extract email body content and clean it by removing separators."""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() in ["text/plain", "text/html"]:
                body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                return clean_email_body(body, part.get_content_type())
    else:
        body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
        return clean_email_body(body, msg.get_content_type())
    return ""

def clean_email_body(body, content_type):
    """Clean the email body by removing unwanted separators and preserve links if HTML."""
    # Remove lines that only contain hyphens or similar patterns
    cleaned_body = re.sub(r'[-=]+', '', body)  # Remove lines of hyphens

    # Normalize line breaks
    cleaned_body = re.sub(r'\n+', '\n', cleaned_body).strip()

    # If the body is HTML, return it as is to preserve links
    if "html" in content_type.lower():
        return cleaned_body

    return cleaned_body

def fetch_emails(email_user, email_pass, limit=10):
    """Connect to IMAP server and fetch filtered emails."""
    imap_server = "imap.iitd.ac.in"
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
                        emails.append({"subject": subject, "body": body})

        # Logout from the server
        mail.logout()
    return emails

def main():
    st.title("IITD Mail Filter :envelope_with_arrow:", anchor=None)
    st.markdown("<h2 style='font-size: 36px;'>Login to Your IITD mail</h2>", unsafe_allow_html=True)

    # Login form
    email_user = st.text_input("Email Address", "")
    email_pass = st.text_input("Password", type="password")

    if st.button("Fetch Emails"):
        if email_user and email_pass:
            with st.spinner("Fetching emails..."):
                emails = fetch_emails(email_user, email_pass, limit=40)
                if emails:
                    for email in emails:
                        st.subheader(f"Subject: {email['subject']}", anchor=None)
                        st.markdown(f"<p style='font-size: 18px;'>{email['body']}</p>", unsafe_allow_html=True)
                        st.markdown("---")
                else:
                    st.warning("No relevant emails found.")
        else:
            st.error("Please enter both email and password.")

if __name__ == "__main__":
    main()
