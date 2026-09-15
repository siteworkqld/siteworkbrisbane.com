import csv, os, json, time, base64, urllib.request
U=os.environ['CLICKSEND_USER']; K=os.environ['CLICKSEND_KEY']
batch=os.environ.get('BATCH','sms_leads.csv'); tmpl=os.environ.get('TEMPLATE','sms_initial')
body_t=open(f'outreach/{tmpl}.txt').read().strip()
rows=list(csv.DictReader(open(f'outreach/{batch}')))
log='outreach/sms_sent.log'; sent=set(l.strip() for l in open(log)) if os.path.exists(log) else set()
auth=base64.b64encode(f'{U}:{K}'.encode()).decode(); n=0
for r in rows:
    key=f"{tmpl}|{r['phone']}"
    if key in sent: continue
    msg=body_t.format(**r)
    payload={"messages":[{"source":"sitework","body":msg,"to":r['phone']}]}
    req=urllib.request.Request('https://rest.clicksend.com/v3/sms/send',data=json.dumps(payload).encode(),headers={'Authorization':'Basic '+auth,'Content-Type':'application/json'})
    try:
        res=json.load(urllib.request.urlopen(req)); st=res['data']['messages'][0]['status']
    except urllib.error.HTTPError as e: st='HTTP '+str(e.code)+' '+e.read().decode()[:200]
    print(r['phone'],'->',st,'|',len(msg),'chars')
    if st=='SUCCESS': open(log,'a').write(key+'\n'); n+=1
    time.sleep(3)
print(f'done: {n} sent')
