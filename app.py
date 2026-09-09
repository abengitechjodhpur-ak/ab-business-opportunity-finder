import json, os, csv
from datetime import datetime
from urllib.parse import quote
import streamlit as st

BASE = os.path.dirname(__file__)
with open(os.path.join(BASE, 'data', 'projects.json'), encoding='utf-8') as f: PROJECTS = json.load(f)
with open(os.path.join(BASE, 'data', 'districts.json'), encoding='utf-8') as f: DISTRICTS = json.load(f)
with open(os.path.join(BASE, 'data', 'schemes.json'), encoding='utf-8') as f: SCHEMES = json.load(f)

st.set_page_config(page_title='AB ENGITECH Business Opportunity Finder', page_icon='🏭', layout='wide')

T = {
'en': {
 'title':'AB ENGITECH Business Opportunity Finder','tag':'Find a manufacturing business suited to your district, budget and resources.','language':'Language','district':'District','area':'Area type','urban':'Urban','rural':'Rural','undecided':'Not decided','budget':'Total investment you are considering','capital':'Your own available capital','land':'Land status','available':'Already available','arrange':'Can arrange','rent':'Need to buy/rent','not_sure':'Not sure','land_size':'Approx. land available','priority':'Your priority','best':'Show me the best opportunities','low_invest':'Lowest investment','growth':'Highest growth potential','govt':'Government-support potential','simple':'Simple operation','mineral':'Mineral-based industry','construction':'Construction-material industry','find':'Find Opportunities','results':'Top recommended projects','why':'Why this ranks well','investment':'Indicative total project investment','space':'Approx. land / shed','power':'Approx. connected power','manpower':'Typical manpower','capacity':'Indicative capacity','complexity':'Regulatory complexity','support':'Government support','details':'Project details','lead':'Get a personalised feasibility snapshot','name':'Name','mobile':'Mobile / WhatsApp','timeline':'When do you want to start?','immediate':'Immediately','3m':'Within 3 months','6m':'3–6 months','12m':'6–12 months','exploring':'Just exploring','submit':'Prepare my enquiry','disclaimer':'Indicative planning tool only. Costs and eligibility are not quotations or subsidy guarantees. Final feasibility requires site, raw material, product and regulatory validation.','pmegp_ok':'PMEGP may be relevant because the project is within the current manufacturing project ceiling.','pmegp_high':'Project investment exceeds the current PMEGP manufacturing ceiling; other financing/incentive routes may still apply.','rips':'RIPS 2024 may provide eligible Rajasthan investment incentives; exact benefit must be checked from the official policy/LaabhCalc.','whatsapp':'Open WhatsApp enquiry','saved':'Enquiry prepared. You can copy the text below or open WhatsApp.','score':'Opportunity score'
},
'hi': {
 'title':'AB ENGITECH व्यवसाय अवसर खोजक','tag':'अपने जिले, बजट और संसाधनों के अनुसार उपयुक्त मैन्युफैक्चरिंग व्यवसाय खोजें।','language':'भाषा','district':'जिला','area':'क्षेत्र','urban':'शहरी','rural':'ग्रामीण','undecided':'तय नहीं','budget':'कुल कितना निवेश करना चाहते हैं','capital':'आपकी स्वयं की उपलब्ध पूंजी','land':'जमीन की स्थिति','available':'जमीन उपलब्ध है','arrange':'व्यवस्था कर सकते हैं','rent':'खरीद/किराये पर लेनी है','not_sure':'पता नहीं','land_size':'लगभग उपलब्ध जमीन','priority':'आपकी प्राथमिकता','best':'सबसे अच्छे अवसर दिखाएं','low_invest':'कम निवेश','growth':'अधिक वृद्धि की संभावना','govt':'सरकारी सहायता की संभावना','simple':'सरल संचालन','mineral':'मिनरल आधारित उद्योग','construction':'निर्माण सामग्री उद्योग','find':'अवसर खोजें','results':'आपके लिए प्रमुख परियोजनाएं','why':'यह परियोजना क्यों उपयुक्त है','investment':'अनुमानित कुल परियोजना निवेश','space':'लगभग जमीन / शेड','power':'लगभग बिजली आवश्यकता','manpower':'सामान्य मैनपावर','capacity':'अनुमानित क्षमता','complexity':'नियामक जटिलता','support':'सरकारी सहायता','details':'परियोजना विवरण','lead':'व्यक्तिगत प्रारंभिक व्यवहार्यता जानकारी प्राप्त करें','name':'नाम','mobile':'मोबाइल / WhatsApp','timeline':'कब शुरू करना चाहते हैं?','immediate':'तुरंत','3m':'3 महीने के भीतर','6m':'3–6 महीने','12m':'6–12 महीने','exploring':'अभी जानकारी ले रहे हैं','submit':'मेरी पूछताछ तैयार करें','disclaimer':'यह केवल प्रारंभिक योजना उपकरण है। लागत, पात्रता या सब्सिडी की गारंटी नहीं है। अंतिम व्यवहार्यता के लिए साइट, कच्चा माल, उत्पाद और नियामक जांच आवश्यक है।','pmegp_ok':'यह परियोजना वर्तमान विनिर्माण परियोजना सीमा के भीतर है, इसलिए PMEGP प्रासंगिक हो सकता है।','pmegp_high':'परियोजना निवेश वर्तमान PMEGP विनिर्माण सीमा से अधिक है; अन्य वित्त/प्रोत्साहन विकल्प लागू हो सकते हैं।','rips':'RIPS 2024 के तहत पात्र राजस्थान निवेश प्रोत्साहन मिल सकते हैं; वास्तविक लाभ आधिकारिक नीति/LaabhCalc से जांचना होगा।','whatsapp':'WhatsApp पूछताछ खोलें','saved':'पूछताछ तैयार है। नीचे का टेक्स्ट कॉपी करें या WhatsApp खोलें।','score':'अवसर स्कोर'
}}

if 'lang' not in st.session_state: st.session_state.lang = None
if not st.session_state.lang:
    st.title('Choose your language / अपनी भाषा चुनें')
    c1,c2=st.columns(2)
    if c1.button('English', use_container_width=True): st.session_state.lang='en'; st.rerun()
    if c2.button('हिंदी', use_container_width=True): st.session_state.lang='hi'; st.rerun()
    st.stop()

lang=st.session_state.lang; t=T[lang]
with st.sidebar:
    st.markdown('### '+t['language'])
    if st.button('हिंदी' if lang=='en' else 'English', use_container_width=True):
        st.session_state.lang='hi' if lang=='en' else 'en'; st.rerun()
    st.caption('Rajasthan MVP • India-ready architecture')

st.title(t['title']); st.write(t['tag'])

c1,c2,c3=st.columns(3)
district_options=[d['name'] for d in DISTRICTS]
district_name=c1.selectbox(t['district'], district_options)
area=c2.selectbox(t['area'], [t['rural'],t['urban'],t['undecided']])
budget_label=c3.selectbox(t['budget'], ['₹10–20 lakh','₹20–35 lakh','₹35–50 lakh','₹50 lakh–₹1 crore','₹1–2 crore','₹2–5 crore','Above ₹5 crore'])
capital=st.selectbox(t['capital'], ['Below ₹5 lakh','₹5–10 lakh','₹10–25 lakh','₹25–50 lakh','₹50 lakh–₹1 crore','Above ₹1 crore'])
land_status=st.selectbox(t['land'], [t['available'],t['arrange'],t['rent'],t['not_sure']])
land_size=st.selectbox(t['land_size'], ['<2,000 sq ft','2,000–5,000 sq ft','5,000–10,000 sq ft','10,000–25,000 sq ft','>25,000 sq ft',t['not_sure']])
priority=st.selectbox(t['priority'], [t['best'],t['low_invest'],t['growth'],t['govt'],t['simple'],t['mineral'],t['construction']])

BUDGETS={'₹10–20 lakh':(10,20),'₹20–35 lakh':(20,35),'₹35–50 lakh':(35,50),'₹50 lakh–₹1 crore':(50,100),'₹1–2 crore':(100,200),'₹2–5 crore':(200,500),'Above ₹5 crore':(500,800)}
LAND={'<2,000 sq ft':1500,'2,000–5,000 sq ft':3500,'5,000–10,000 sq ft':7500,'10,000–25,000 sq ft':17500,'>25,000 sq ft':50000,t['not_sure']:None}

def score_project(p, district, bmin,bmax, land_avail, priority):
    overlap=max(0,min(bmax,p['max_budget'])-max(bmin,p['min_budget']))
    width=max(1,bmax-bmin)
    budget_fit=min(1, overlap/width)
    if p['min_budget']<=bmax and p['max_budget']>=bmin: budget_fit=max(budget_fit,.65)
    dvals=[district['tags'].get(tag,4) for tag in p['raw_tags']]
    raw=max(dvals)/10 if dvals else .5
    market_context=max(district['tags'].get('construction_market',5),district['tags'].get('mineral_market',5))/10
    market=((p['market']/10)*.55 + market_context*.45)
    govt=(1 if p['pmegp'] and p['min_budget']<=50 else .6 if p['rips'] else .3)
    if land_avail is None: landfit=.65
    elif land_avail>=p['land_min']: landfit=1
    else: landfit=max(.15, land_avail/p['land_min'])
    simplicity=p['simplicity']/10
    competition=.65
    ab=p['ab_fit']/10
    total=25*budget_fit+20*raw+15*market+15*govt+10*landfit+5*simplicity+5*competition+5*ab
    if priority==t['low_invest']: total += max(0, 5-(p['ideal_budget']/50))
    if priority==t['growth']: total += p['market']*.45
    if priority==t['govt']: total += 4 if p['pmegp'] else 1
    if priority==t['simple']: total += p['simplicity']*.5
    if priority==t['mineral'] and p['family'] in ['mineral','gypsum','lime','value_add']: total += 5
    if priority==t['construction'] and p['family'] in ['construction','aggregate']: total += 5
    if bmax < p['min_budget']*.75: total -= 30
    if p['complexity']>=5 and bmax<75: total -= 25
    return max(0,min(100,round(total)))

district=next(d for d in DISTRICTS if d['name']==district_name)
bmin,bmax=BUDGETS[budget_label]
land_avail=LAND[land_size]
ranked=sorted([(score_project(p,district,bmin,bmax,land_avail,priority),p) for p in PROJECTS], key=lambda x:x[0], reverse=True)

if st.button(t['find'], type='primary', use_container_width=True): st.session_state.show_results=True
if st.session_state.get('show_results'):
    st.divider(); st.subheader(t['results'])
    top=ranked[:3]
    for idx,(score,p) in enumerate(top,1):
        name=p['name_en'] if lang=='en' else p['name_hi']
        with st.container(border=True):
            a,b=st.columns([4,1]); a.markdown(f"### {idx}. {name}"); b.metric(t['score'], f"{score}/100")
            st.write(p['desc_en'] if lang=='en' else p['desc_hi'])
            m1,m2,m3,m4=st.columns(4)
            m1.metric(t['investment'], f"₹{p['min_budget']}–{p['max_budget']} L")
            m2.metric(t['space'], f"{p['land_min']:,}–{p['land_max']:,} sq ft")
            m3.metric(t['power'], f"{p['power_min']}–{p['power_max']} kW")
            m4.metric(t['manpower'], f"{p['manpower_min']}–{p['manpower_max']}")
            with st.expander(t['details']):
                st.write(f"**{t['capacity']}:** {p['capacity_en'] if lang=='en' else p['capacity_hi']}")
                st.write(f"**{t['complexity']}:** {p['regulatory']}")
                st.write(f"**{t['support']}:**")
                st.info(t['pmegp_ok'] if p['pmegp'] and p['min_budget']<=50 else t['pmegp_high'])
                if p['rips']: st.info(t['rips'])
                st.caption(t['disclaimer'])
    selected=st.selectbox(t['lead'], [p['name_en'] if lang=='en' else p['name_hi'] for _,p in top])
    with st.form('leadform'):
        name=st.text_input(t['name']); mobile=st.text_input(t['mobile']); timeline=st.selectbox(t['timeline'],[t['immediate'],t['3m'],t['6m'],t['12m'],t['exploring']])
        sent=st.form_submit_button(t['submit'], type='primary', use_container_width=True)
    if sent:
        project_obj=next(p for _,p in top if (p['name_en'] if lang=='en' else p['name_hi'])==selected)
        score=next(s for s,p in top if p['id']==project_obj['id'])
        lead_score='HOT' if ('₹25' in capital or '₹50' in capital or 'Above ₹1' in capital) and timeline in [t['immediate'],t['3m']] and land_status==t['available'] else 'WARM' if timeline!=t['exploring'] else 'COLD'
        leadfile=os.path.join(BASE,'leads.csv'); exists=os.path.exists(leadfile)
        with open(leadfile,'a',newline='',encoding='utf-8') as f:
            w=csv.writer(f)
            if not exists:w.writerow(['timestamp','name','mobile','district','area','budget','capital','land_status','land_size','project','opportunity_score','timeline','lead_score'])
            w.writerow([datetime.now().isoformat(timespec='seconds'),name,mobile,district_name,area,budget_label,capital,land_status,land_size,project_obj['name_en'],score,timeline,lead_score])
        msg=(f"Hello AB ENGITECH. I used your Business Opportunity Finder.\n\nDistrict: {district_name}\nRecommended project: {project_obj['name_en']}\nInvestment: {budget_label}\nOwn capital: {capital}\nLand: {land_status}\nStart timeline: {timeline}\nOpportunity score: {score}/100\n\nPlease guide me regarding feasibility.")
        st.success(t['saved']); st.code(msg)
        st.link_button(t['whatsapp'], f"https://wa.me/?text={quote(msg)}", use_container_width=True)

st.divider(); st.caption(t['disclaimer'])
