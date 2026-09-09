BUDGETS={'₹10–20 lakh':(10,20),'₹20–35 lakh':(20,35),'₹35–50 lakh':(35,50),'₹50 lakh–₹1 crore':(50,100),'₹1–2 crore':(100,200),'₹2–5 crore':(200,500),'Above ₹5 crore':(500,800)}

LAND_EN={'<2,000 sq ft':1500,'2,000–5,000 sq ft':3500,'5,000–10,000 sq ft':7500,'10,000–25,000 sq ft':17500,'>25,000 sq ft':50000,'Not sure':None}
LAND_HI={'<2,000 वर्गफुट':1500,'2,000–5,000 वर्गफुट':3500,'5,000–10,000 वर्गफुट':7500,'10,000–25,000 वर्गफुट':17500,'>25,000 वर्गफुट':50000,'पता नहीं':None}


def score_project(p,d,bmin,bmax,land_avail,priority,t):
    overlap=max(0,min(bmax,p['max_budget'])-max(bmin,p['min_budget']))
    budget_fit=min(1,overlap/max(1,bmax-bmin))
    if p['min_budget']<=bmax and p['max_budget']>=bmin: budget_fit=max(budget_fit,.65)
    raw=max([d['tags'].get(tag,4) for tag in p['raw_tags']] or [5])/10
    market_context=max(d['tags'].get('construction_market',5),d['tags'].get('mineral_market',5))/10
    market=(p['market']/10)*.55+market_context*.45
    govt=1 if p['pmegp'] and p['min_budget']<=50 else .6 if p['rips'] else .3
    landfit=.65 if land_avail is None else 1 if land_avail>=p['land_min'] else max(.15,land_avail/p['land_min'])
    total=25*budget_fit+20*raw+15*market+15*govt+10*landfit+5*(p['simplicity']/10)+5*.65+5*(p['ab_fit']/10)
    if priority==t['low']: total+=max(0,5-p['ideal_budget']/50)
    if priority==t['growth']: total+=p['market']*.45
    if priority==t['govt']: total+=4 if p['pmegp'] else 1
    if priority==t['simple']: total+=p['simplicity']*.5
    if priority==t['mineral'] and p['family'] in ['mineral','gypsum','lime','value_add']: total+=5
    if priority==t['construction'] and p['family'] in ['construction','aggregate']: total+=5
    if bmax<p['min_budget']*.75: total-=30
    if p['complexity']>=5 and bmax<75: total-=25
    return max(0,min(100,round(total)))
