import imaplib
import email
import os
from config import EMAIL_ACCOUNT, EMAIL_PASSWORD

def fetch_unread_invoice_pdfs():
    """
    Connects to the IMAP server, finds unread emails, extracts PDF attachments,
    saves them to a local /pdfs directory, and returns a list of file paths.
    """
    if not EMAIL_ACCOUNT or not EMAIL_PASSWORD:
        print("Missing Email Credentials in .env")
        return []

    try:
        print("  -> Connecting to Gmail IMAP...")
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        
        print("  -> Logging in...")
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        
        print("  -> Selecting inbox...")
        mail.select("inbox")

        print("  -> Searching for UNSEEN emails...")
        # Search for unread emails
        status, messages = mail.search(None, "UNSEEN")
        message_ids = messages[0].split()
        
        if status != "OK" or not message_ids:
            print("  -> No new unread emails found.")
            return []

        print(f"  -> Found {len(message_ids)} unread emails. Processing the 5 most recent...")

        pdf_paths = []
        os.makedirs("pdfs", exist_ok=True)

        # Only process the 5 most recent unread emails to prevent hanging!
        for num in message_ids[-5:]:
            status, data = mail.fetch(num, "(RFC822)")
            if status != "OK":
                continue
                
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            # Walk through the email parts to find attachments
            for part in msg.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue
                
                filename = part.get_filename()
                if filename and filename.lower().endswith('.pdf'):
                    # Save the PDF
                    filepath = os.path.join("pdfs", filename)
                    with open(filepath, "wb") as f:
                        f.write(part.get_payload(decode=True))
                    
                    pdf_paths.append(filepath)
                    print(f"Downloaded attachment: {filename}")
        
        mail.logout()
        return pdf_paths

    except Exception as e:
        print(f"IMAP Error: {e}")
        return []
