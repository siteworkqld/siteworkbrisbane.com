import csv, os, smtplib, sys, time, json
from email.message import EmailMessage
U=os.environ['GMAIL_USER']; P=os.environ['GMAIL_APP_PASSWORD']
batch=os.environ.get('BATCH','leads.csv'); tmpl=os.environ.get('TEMPLATE','initial')
subj_t=open(f'outreach/{tmpl}.subject.txt').read().strip(); body_t=open(f'outreach/{tmpl}.body.txt').read()
rows=list(csv.DictReader(open(f'outreach/{batch}')))
sent_log=f'outreach/sent.log'; sent=set(l.strip() for l in open(sent_log)) if os.path.exists(sent_log) else set()
s=smtplib.SMTP_SSL('smtp.gmail.com',465); s.login(U,P); n=0
for r in rows:
    key=f"{tmpl}|{r['email']}"
    if not r.get('email') or key in sent: continue
    m=EmailMessage(); m['From']=f"Jacob at Sitework <{U}>"; m['To']=r['email']; m['Reply-To']=U
    m['Subject']=subj_t.format(**r); m.set_content(body_t.format(**r))
    s.send_message(m); open(sent_log,'a').write(key+'\n'); n+=1; print('sent ->',r['email']); time.sleep(20)
s.quit(); print(f'done: {n} sent')
