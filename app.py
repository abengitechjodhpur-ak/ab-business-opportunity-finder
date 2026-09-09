import json, os, csv
from datetime import datetime
from urllib.parse import quote
import streamlit as st

from styles import apply_styles, intro_block, step_header, close_step, result_card_start, fact_grid, lead_intro
from translations import TEXT
from engine import BUDGETS, LAND_EN, LAND_HI, score_project

BASE = os.path.dirname(__file__)
with open(os.path.join(BASE, 'data', 'projects.json'), encoding='utf-8') as f:
    PROJECTS = json.load(f)
with open(os.path.join(BASE, 'data', 'districts.json'), encoding='utf-8') as f:
    DISTRICTS = json.load(f)

st.set_page_config(
    page_title='AB ENGITECH Business Opportunity Finder',
    page_icon='🏭',
    layout='centered',
    initial_sidebar_state='collapsed'
)
apply_styles()

if 'lang' not in st.session_state:
    st.session_state.lang = None
if 'show_results' not in st.session_state:
    st.session_state.show_results = False

# Compact top brand row
head1, head2 = st.columns([1, 4.7], vertical_alignment='center')
with head1:
    st.image('assets/logo.svg', width=58)
with head2:
    st.markdown('<div class="brand-card"><div class="brand-title">AB ENGITECH</div><div class="brand-sub">Business Opportunity Finder • Jodhpur</div><div class="brand-accent"></div></div>', unsafe_allow_html=True)

# Language gate
if not st.session_state.lang:
    intro_block('Find the right manufacturing opportunity', 'Choose your language to start. / शुरुआत के लिए अपनी भाषा चुनें।', 'en')
    c1, c2 = st.columns(2)
    if c1.button('English', type='primary', use_container_width=True):
        st.session_state.lang = 'en'
        st.rerun()
    if c2.button('हिंदी', use_container_width=True):
        st.session_state.lang = 'hi'
        st.rerun()
    st.stop()

lang = st.session_state.lang
t = TEXT[lang]

# Language switch in main flow, no sidebar
switch_label = 'हिंदी' if lang == 'en' else 'English'
_, switch_col = st.columns([4, 1.2])
with switch_col:
    if st.button(switch_label, use_container_width=True):
        st.session_state.lang = 'hi' if lang == 'en' else 'en'
        st.session_state.show_results = False
        st.rerun()

intro_title = 'Find your best-fit manufacturing project' if lang == 'en' else 'अपने लिए उपयुक्त मैन्युफैक्चरिंग परियोजना खोजें'
intro_sub = 'Answer a few quick questions. We will shortlist the best opportunities for your district and budget.' if lang == 'en' else 'कुछ आसान जानकारी भरें। हम आपके जिले और बजट के अनुसार उपयुक्त परियोजनाएं सुझाएंगे।'
intro_block(intro_title, intro_sub, lang)

# STEP 1
step_header('1', 'Location' if lang == 'en' else 'स्थान', 'Tell us where you want to start.' if lang == 'en' else 'बताएं आप व्यवसाय कहाँ शुरू करना चाहते हैं।')
display_districts = [d['name'] if lang == 'en' else d['hi'] for d in DISTRICTS]
selected_district = st.selectbox(t['district'], display_districts)
area = st.selectbox(t['area'], [t['rural'], t['urban'], t['undecided']])
close_step()

# STEP 2
step_header('2', 'Investment' if lang == 'en' else 'निवेश', 'Choose a realistic investment range.' if lang == 'en' else 'अपना वास्तविक निवेश स्तर चुनें।')
budget_en = list(BUDGETS.keys())
budget_hi = ['₹10–20 लाख','₹20–35 लाख','₹35–50 लाख','₹50 लाख–₹1 करोड़','₹1–2 करोड़','₹2–5 करोड़','₹5 करोड़ से अधिक']
budget_display = st.selectbox(t['budget'], budget_en if lang == 'en' else budget_hi)
budget_label = budget_display if lang == 'en' else budget_en[budget_hi.index(budget_display)]
capital_options = ['Below ₹5 lakh','₹5–10 lakh','₹10–25 lakh','₹25–50 lakh','₹50 lakh–₹1 crore','Above ₹1 crore'] if lang == 'en' else ['₹5 लाख से कम','₹5–10 लाख','₹10–25 लाख','₹25–50 लाख','₹50 लाख–₹1 करोड़','₹1 करोड़ से अधिक']
capital = st.selectbox(t['capital'], capital_options)
close_step()

# STEP 3
step_header('3', 'Resources & preference' if lang == 'en' else 'संसाधन और प्राथमिकता', 'A few details help us rank projects better.' if lang == 'en' else 'कुछ जानकारी से हम बेहतर परियोजना सुझा पाएंगे।')
land_status = st.selectbox(t['land'], [t['available'], t['arrange'], t['rent'], t['not_sure']])
land_options = list(LAND_EN.keys()) if lang == 'en' else list(LAND_HI.keys())
land_size = st.selectbox(t['land_size'], land_options)
priority = st.selectbox(t['priority'], [t['best'], t['low'], t['growth'], t['govt'], t['simple'], t['mineral'], t['construction']])
close_step()

# Scoring prep
district = next(d for d in DISTRICTS if (d['name'] if lang == 'en' else d['hi']) == selected_district)
bmin, bmax = BUDGETS[budget_label]
land_avail = (LAND_EN if lang == 'en' else LAND_HI)[land_size]
ranked = sorted(
    [(score_project(p, district, bmin, bmax, land_avail, priority, t), p) for p in PROJECTS],
    key=lambda x: x[0],
    reverse=True
)

if st.button(t['find'], type='primary', use_container_width=True):
    st.session_state.show_results = True

if st.session_state.show_results:
    st.markdown(f'<div class="results-title">{t["results"]}</div>', unsafe_allow_html=True)
    top = ranked[:3]

    for idx, (score, p) in enumerate(top, 1):
        name = p['name_en'] if lang == 'en' else p['name_hi']
        desc = p['desc_en'] if lang == 'en' else p['desc_hi']
        result_card_start(idx, name, score, desc)

        invest_text = f'₹{p["min_budget"]}–{p["max_budget"]} L' if lang == 'en' else f'₹{p["min_budget"]}–{p["max_budget"]} लाख'
        space_text = f'{p["land_min"]:,}–{p["land_max"]:,} sq ft' if lang == 'en' else f'{p["land_min"]:,}–{p["land_max"]:,} वर्गफुट'
        facts = [
            (t['investment'], invest_text),
            (t['space'], space_text),
            (t['power'], f'{p["power_min"]}–{p["power_max"]} kW'),
            (t['manpower'], f'{p["manpower_min"]}–{p["manpower_max"]}')
        ]
        fact_grid(facts)

        with st.expander(t['details']):
            st.write(f'**{t["capacity"]}:** {p["capacity_en"] if lang == "en" else p["capacity_hi"]}')
            complexity = p['regulatory'] if lang == 'en' else {'Low':'कम','Medium':'मध्यम','High':'उच्च'}.get(p['regulatory'], p['regulatory'])
            st.write(f'**{t["complexity"]}:** {complexity}')
            st.write(f'**{t["support"]}:**')
            st.info(t['pmegp_ok'] if p['pmegp'] and p['min_budget'] <= 50 else t['pmegp_high'])
            if p['rips']:
                st.info(t['rips'])

    lead_intro(t['lead'], t['lead_help'])
    selected = st.selectbox(t['lead'], [p['name_en'] if lang == 'en' else p['name_hi'] for _, p in top])

    with st.form('leadform'):
        lead_name = st.text_input(t['name'])
        mobile = st.text_input(t['mobile'])
        timeline = st.selectbox(t['timeline'], [t['immediate'], t['m3'], t['m6'], t['m12'], t['exploring']])
        sent = st.form_submit_button(t['submit'], type='primary', use_container_width=True)

    if sent:
        pobj = next(p for _, p in top if (p['name_en'] if lang == 'en' else p['name_hi']) == selected)
        sc = next(s for s, p in top if p['id'] == pobj['id'])
        lead_score = 'HOT' if timeline in [t['immediate'], t['m3']] and land_status == t['available'] else 'WARM' if timeline != t['exploring'] else 'COLD'

        leadfile = os.path.join(BASE, 'leads.csv')
        exists = os.path.exists(leadfile)
        with open(leadfile, 'a', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            if not exists:
                w.writerow(['timestamp','name','mobile','district','area','budget','capital','land_status','land_size','project','opportunity_score','timeline','lead_score'])
            w.writerow([datetime.now().isoformat(timespec='seconds'), lead_name, mobile, district['name'], area, budget_label, capital, land_status, land_size, pobj['name_en'], sc, timeline, lead_score])

        msg = f'''Hello AB ENGITECH. I used your Business Opportunity Finder.\n\nDistrict: {district['name']}\nRecommended project: {pobj['name_en']}\nInvestment: {budget_label}\nOwn capital: {capital}\nLand: {land_status}\nStart timeline: {timeline}\nOpportunity score: {sc}/100\n\nPlease guide me regarding feasibility.'''
        st.success(t['saved'])
        st.link_button(t['whatsapp'], f'https://wa.me/?text={quote(msg)}', use_container_width=True)

st.markdown(f'<div class="note">{t["disclaimer"]}</div>', unsafe_allow_html=True)
