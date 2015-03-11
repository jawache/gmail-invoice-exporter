# -*- coding: utf-8 -*-
from datetime import datetime
import os
import sys
from slugify import slugify
from email.utils import parseaddr
import gmail


def ensure_dir(path):
    if not os.path.exists(path): os.makedirs(path)


def is_non_zero_file(fpath):
    return True if os.path.isfile(fpath) and os.path.getsize(fpath) > 0 else False


def parse_mail(messages):
    for message in messages:
        message.fetch()
        frn, fr = parseaddr(message.fr)
        ton, to = parseaddr(message.to)
        body = message.body
        html = message.html
        sent = message.sent_at
        subject = slugify(message.subject)
        name = sent.date().isoformat() + "-" + subject
        path = os.path.join("receipts/", slugify(frn or fr), name)
        ensure_dir(path)
        print u"🍏  [%s] %s - %s" % (sent.date().isoformat(), fr, subject),
        with open(path + "/info.txt", "w") as f:
            data = [
                u"From: %s\n" % message.fr,
                u"To: %s\n" % message.to,
                u"Subject: %s\n" % message.subject.encode('ascii', 'ignore'),
                u"Sent: %s\n" % message.sent_at
            ]
            try:
                f.writelines(data)
            except:
                print data
        with open(path + "/email.txt", "w") as f:
            if body:
                f.write(body)

        html_file_path = path + "/email.html"
        with open(html_file_path, "w+r") as f:
            if html and len(html) > 0:
                f.write(html)
        if not is_non_zero_file(html_file_path):
            os.remove(html_file_path)

        for i, attachment in enumerate(message.attachments):
            name = attachment.name or "attachment-%s.txt" % i
            print '💊   ' + name,
            filepath = path + "/" + name
            attachment.save(filepath)

        print


def loop_mail(email, password):
    before = datetime(year=2015, month=3, day=1)
    after = datetime(year=2014, month=2, day=28)
    g = gmail.login(email, password)
    print u"✅  Using smart label\n"
    messages = g.inbox().mail(label="^smartlabel_receipt", before=before, after=after)
    parse_mail(messages)
    print u"✅  Using subject=receipt\n"
    messages = g.inbox().mail(subject="receipt", before=before, after=after)
    parse_mail(messages)
    print u"✅  Using subject=invoice\n"
    messages = g.inbox().mail(subject="invoice", before=before, after=after)
    parse_mail(messages)
    print u"✅  Using subject=order\n"
    messages = g.inbox().mail(subject="order", before=before, after=after)
    parse_mail(messages)



if __name__ == '__main__':
    email = sys.argv[1]
    password = sys.argv[2]
    print email
    print password
    loop_mail(email, password)