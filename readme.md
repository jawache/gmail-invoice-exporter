# Intro
Last Minute Tax Helper

Tries to extract all your receipts & invoices from your gmail account for the last tax year and stores them in a folder.

`
<sender name or email>
 |- <date>-<subject>
    |- email.html - if available the html version of the email
    |- email.txt - if available the plain text version of the email
    |- info.txt - info about the email, sender, to, subject, date
    |- * - If there are any attachments it will download and store those also.
`   
# How it works

It does 4 separate queries
- Using smart label
- Using subject=receipt
- Using subject=invoice
- Using subject=order

# Usage

`pip install -r requirements.txt`

`python exportgmail.py <email> <password>`
