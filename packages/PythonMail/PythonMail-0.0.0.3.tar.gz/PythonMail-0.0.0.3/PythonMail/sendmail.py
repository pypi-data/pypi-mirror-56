import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def send_email(fromaddr, toaddr, password, subject="", content="", files=None):
    """
    send email - supports html + css and more (further encodings are not tested)
    :param fromaddr: from addr
    :param toaddr: to addr
    :param content: text message
    :param files: Files with complete path
    :return: None
    """
    if files is not None:
        assert type(files) == list

    msg = MIMEMultipart()
    msg['To'] = toaddr
    msg['From'] = fromaddr
    msg['Subject'] = subject

    body = MIMEText(content, "html", "utf8")
    msg.attach(body)

    if files is not None:
        for file in files:
            attachment = MIMEApplication(open(file).read(), _subtype="txt")
            attachment.add_header("Content-Disposition", 'attachment', filename=file)
            msg.attach(attachment)

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(fromaddr, password)
    text = msg.as_string()
    smtp.sendmail(fromaddr, toaddr, text)
    smtp.quit()
