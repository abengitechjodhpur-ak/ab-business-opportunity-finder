import json,os,csv
from datetime import datetime
from urllib.parse import quote
import streamlit as st
from styles import apply_styles,show_brand
from translations import TEXT
from engine import BUDGETS,LAND_EN,LAND_HI,score_project

BASE=os.path.dirname(__file__)
with open(os.path.join(BASE,'data','projects.json'),encoding='utf-8') as f: PROJECTS=json.load(f)
with open(os.path.join(BASE,'data','districts.json'),encoding='utf-8') as f: DISTRICTS=json.load(f)

st.set_page_config(page_title='AB ENGITECH Business Opportunity Finder',page_icon='🏭',layout='wide')
apply_styles()

if 'lang' not in st.session_state: st.session_state.lang=None
if 'show_results' not in st.session_state: st.session_state.show_results=False

if not st.session_state.lang:
    show_brand('AB ENGITECH Business Opportunity Finder','Choose your preferred language / अपनी भाषा चुनें')
    c1,c2=st.columns(2)
    if c1.button('English',type='primary',use_container_width=True): st.session_state.lang='en'; st.rerun()
    if c2.button('हिंदी',use_container_width=True): st.session_state.lang='hi'; st.rerun()
    st.stop()

lang=st.session_state.lang
t=TEXT[lang]
with st.sidebar:
    st.image('assets/logo.svg',use_container_width=True)
    st.caption('AB ENGITECH • Jodhpur')
    st.markdown('### Language / भाषा')
    if st.button('हिंदी' if lang=='en' else 'English',use_container_width=True):
        st.session_state.lang='hi' if lang=='en' else 'en'; st.session_state.show_results=False; st.rerun()

show_brand(t['title'],t['tag'])
st.markdown(f'<div class="panel"><h3>{t["filters"]}</h3><p>{t["intro"]}</p>',unsafe_allow_html=True)

c1,c2,c3=st.columns(3)
display_districts=[d['name'] if lang=='en' else d['hi'] for d in DISTRICTS]
selected_district=c1.selectbox(t['district'],display_districts)
area=c2.selectbox(t['area'],[t['rural'],t['urban'],t['undecided']])
budget_label=c3.selectbox(t['budget'],list(BUDGETS.keys()))
capital_options=['Below ₹5 lakh','₹5–10 lakh','₹10–25 lakh','₹25–50 lakh','₹50 lakh–₹1 crore','Above ₹1 crore'] if lang=='en' else ['₹5 लाख से कम','₹5–10 लाख','₹10–25 लाख','₹25–50 लाख','₹50 लाख–₹1 करोड़','₹1 करोड़ से अधिक']
capital=st.selectbox(t['capital'],capital_options)
land_status=st.selectbox(t['land'],[t['available'],t['arrange'],t['rent'],t['not_sure']])
land_options=list(LAND_EN.keys()) if lang=='en' else list(LAND_HI.keys())
land_size=st.selectbox(t['land_size'],land_options)
priority=st.selectbox(t['priority'],[t['best'],t['low'],t['growth'],t['govt'],t['simple'],t['mineral'],t['construction']])
st.markdown('</div>',unsafe_allow_html=True)

district=next(d for d in DISTRICTS if (d['name'] if lang=='en' else d['hi'])==selected_district)
bmin,bmax=BUDGETS[budget_label]
land_avail=(LAND_EN if lang=='en' else LAND_HI)[land_size]
ranked=sorted([(score_project(p,district,bmin,bmax,land_avail,priority,t),p) for p in PROJECTS],key=lambda x:x[0],reverse=True)

if st.button(t['find'],type='primary',use_container_width=True): st.session_state.show_results=True

if st.session_state.show_results:
    st.subheader(t['results'])
    top=ranked[:3]
    for idx,(score,p) in enumerate(top,1):
        name=p['name_en'] if lang=='en' else p['name_hi']
        desc=p['desc_en'] if lang=='en' else p['desc_hi']
        with st.container(border=True):
            a,b=st.columns([5,1.3])
            a.markdown(f'<span class="rank">#{idx}</span>',unsafe_allow_html=True)
            a.markdown(f'### {name}')
            a.write(desc)
            b.markdown(f'<div class="score">{t["score"]}<br><b>{score}/100</b></div>',unsafe_allow_html=True)
            m1,m2,m3,m4=st.columns(4)
            m1.metric(t['investment'],f'₹{p["min_budget"]}–{p["max_budget"]} L')
            m2.metric(t['space'],f'{p["land_min"]:,}–{p["land_max"]:,} sq ft')
            m3.metric(t['power'],f'{p["power_min"]}–{p["power_max"]} kW')
            m4.metric(t['manpower'],f'{p["manpower_min"]}–{p["manpower_max"]}')
            with st.expander(t['details']):
                st.write(f'**{t["capacity"]}:** {p["capacity_en"] if lang=="en" else p["capacity_hi"]}')
                st.write(f'**{t["complexity"]}:** {p["regulatory"]}')
                st.write(f'**{t["support"]}:**')
                st.info(t['pmegp_ok'] if p['pmegp'] and p['min_budget']<=50 else t['pmegp_high'])
                if p['rips']: st.info(t['rips'])
                st.caption(t['disclaimer'])

    st.markdown(f'<div class="cta"><h3>{t["lead"]}</h3><p>{t["lead_help"]}</p></div>',unsafe_allow_html=True)
    selected=st.selectbox(t['lead'],[p['name_en'] if lang=='en' else p['name_hi'] for _,p in top])
    with st.form('leadform'):
        c1,c2=st.columns(2)
        lead_name=c1.text_input(t['name'])
        mobile=c2.text_input(t['mobile'])
        timeline=st.selectbox(t['timeline'],[t['immediate'],t['m3'],t['m6'],t['m12'],t['exploring']])
        sent=st.form_submit_button(t['submit'],type='primary',use_container_width=True)
    if sent:
        pobj=next(p for _,p in top if (p['name_en'] if lang=='en' else p['name_hi'])==selected)
        sc=next(s for s,p in top if p['id']==pobj['id'])
        lead_score='HOT' if timeline in [t['immediate'],t['m3']] and land_status==t['available'] else 'WARM' if timeline!=t['exploring'] else 'COLD'
        leadfile=os.path.join(BASE,'leads.csv'); exists=os.path.exists(leadfile)
        with open(leadfile,'a',newline='',encoding='utf-8') as f:
            w=csv.writer(f)
            if not exists: w.writerow(['timestamp','name','mobile','district','area','budget','capital','land_status','land_size','project','opportunity_score','timeline','lead_score'])
            w.writerow([datetime.now().isoformat(timespec='seconds'),lead_name,mobile,district['name'],area,budget_label,capital,land_status,land_size,pobj['name_en'],sc,timeline,lead_score])
        msg=f'''Hello AB ENGITECH. I used your Business Opportunity Finder.\n\nDistrict: {district['name']}\nRecommended project: {pobj['name_en']}\nInvestment: {budget_label}\nOwn capital: {capital}\nLand: {land_status}\nStart timeline: {timeline}\nOpportunity score: {sc}/100\n\nPlease guide me regarding feasibility.'''
        st.success(t['saved'])
        st.code(msg)
        st.link_button(t['whatsapp'],f'https://wa.me/?text={quote(msg)}',use_container_width=True)

st.divider()
st.caption(t['disclaimer'])
