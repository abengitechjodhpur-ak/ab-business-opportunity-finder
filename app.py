import json, os, csv
from datetime import datetime
from urllib.parse import quote
import streamlit as st
from translations import TEXT
from engine import BUDGETS, LAND_EN, LAND_HI, score_project

BASE = os.path.dirname(__file__)
with open(os.path.join(BASE, 'data', 'projects.json'), encoding='utf-8') as f:
    PROJECTS = json.load(f)
with open(os.path.join(BASE, 'data', 'districts.json'), encoding='utf-8') as f:
    DISTRICTS = json.load(f)

st.set_page_config(page_title='AB ENGITECH Business Opportunity Finder', page_icon='🏭', layout='centered', initial_sidebar_state='collapsed')

st.markdown('''
<style>
:root{--orange:#EF8429;--green:#087A5C;--ink:#18212F;--muted:#667085;--line:#E7E9EE;--soft:#F6F7F9}
.block-container{max-width:760px;padding-top:.7rem;padding-bottom:4rem;padding-left:1rem;padding-right:1rem}
[data-testid="stAppViewContainer"]{background:var(--soft)}
[data-testid="stHeader"]{background:rgba(246,247,249,.94)}
#MainMenu,footer{visibility:hidden}
.brand-card{background:#fff;border:1px solid var(--line);border-radius:16px;padding:12px 14px;box-shadow:0 3px 14px rgba(16,24,40,.04)}
.brand-title{font-size:1.18rem;font-weight:800;color:var(--ink)}
.brand-sub{font-size:.82rem;color:var(--muted);margin-top:2px}.brand-accent{height:3px;border-radius:99px;background:linear-gradient(90deg,var(--orange) 0 50%,var(--green) 50% 100%);margin-top:8px}
.intro{text-align:center;padding:12px 8px 4px}.intro h1{font-size:1.55rem;line-height:1.15;margin:.2rem 0 .45rem;color:var(--ink)}.intro p{font-size:.92rem;color:var(--muted);margin:0 auto;max-width:610px}.trust-row{display:flex;justify-content:center;gap:7px;flex-wrap:wrap;margin:11px 0 3px}.trust{background:#fff;border:1px solid var(--line);border-radius:999px;padding:5px 9px;font-size:.76rem;color:#475467}
.step-card{background:#fff;border:1px solid var(--line);border-radius:16px;padding:15px 15px 8px;margin:12px 0;box-shadow:0 3px 14px rgba(16,24,40,.035)}
.step-row{display:flex;align-items:center;gap:10px}.step-num{width:28px;height:28px;border-radius:9px;background:#FFF1E5;color:#C86412;font-weight:800;display:flex;align-items:center;justify-content:center;font-size:.85rem}.step-title{font-size:1rem;font-weight:750;color:var(--ink)}.step-help{font-size:.82rem;color:var(--muted);margin:3px 0 8px 38px}
div[data-baseweb="select"]>div,div[data-testid="stTextInput"] input{min-height:50px;border-radius:12px!important;background:#FBFCFD;border-color:#DDE1E7!important}label[data-testid="stWidgetLabel"] p{font-size:.87rem;font-weight:650;color:#344054}.stButton>button,.stFormSubmitButton>button,.stLinkButton>a{min-height:50px;border-radius:12px!important;font-weight:750!important;font-size:.97rem!important}.stButton>button[kind="primary"],.stFormSubmitButton>button[kind="primary"]{background:var(--green)!important;border-color:var(--green)!important}
.results-title{font-size:1.22rem;font-weight:800;color:var(--ink);margin:1.4rem 0 .5rem}.result-card{background:#fff;border:1px solid var(--line);border-radius:16px;padding:15px;margin:10px 0;box-shadow:0 4px 18px rgba(16,24,40,.045)}.result-head{display:flex;align-items:flex-start;justify-content:space-between;gap:10px}.result-name{font-size:1.05rem;font-weight:800;color:var(--ink);line-height:1.2}.result-rank{font-size:.7rem;font-weight:800;color:#C86412;text-transform:uppercase;letter-spacing:.04em;margin-bottom:4px}.score-pill{white-space:nowrap;background:#EAF7F2;color:#08654D;border-radius:999px;padding:7px 10px;font-size:.82rem;font-weight:800}.result-desc{color:#667085;font-size:.87rem;margin:8px 0 12px}.facts{display:grid;grid-template-columns:1fr 1fr;gap:8px}.fact{background:#F8F9FB;border-radius:11px;padding:10px}.fact-label{font-size:.66rem;text-transform:uppercase;letter-spacing:.04em;color:#98A2B3;font-weight:750}.fact-value{font-size:.88rem;color:#344054;font-weight:700;margin-top:2px}.lead-box{background:#18212F;border-radius:16px;padding:17px;margin:18px 0 10px;color:#fff}.lead-box h3{font-size:1.06rem;margin:0 0 5px;color:#fff}.lead-box p{font-size:.84rem;color:#D0D5DD;margin:0}.note{font-size:.74rem;color:#98A2B3;text-align:center;margin-top:14px}
@media(max-width:640px){.block-container{padding-left:.7rem;padding-right:.7rem}.intro h1{font-size:1.35rem}.brand-title{font-size:1rem}.brand-sub{font-size:.74rem}.step-card{padding:13px 12px 7px}.facts{grid-template-columns:1fr 1fr}}
</style>
''', unsafe_allow_html=True)


def intro_block(title, subtitle, lang='en'):
    chips = ['District-based','Budget matched','Subsidy-aware'] if lang == 'en' else ['जिला आधारित','बजट अनुसार','सब्सिडी जानकारी']
    chip_html = ''.join(f'<span class="trust">{x}</span>' for x in chips)
    st.markdown(f'<div class="intro"><h1>{title}</h1><p>{subtitle}</p><div class="trust-row">{chip_html}</div></div>', unsafe_allow_html=True)


def step_header(num, title, help_text):
    st.markdown(f'<div class="step-card"><div class="step-row"><div class="step-num">{num}</div><div class="step-title">{title}</div></div><div class="step-help">{help_text}</div>', unsafe_allow_html=True)


def close_step():
    st.markdown('</div>', unsafe_allow_html=True)


def result_card(rank, name, score, desc, facts):
    facts_html = ''.join(f'<div class="fact"><div class="fact-label">{label}</div><div class="fact-value">{value}</div></div>' for label, value in facts)
    st.markdown(f'<div class="result-card"><div class="result-head"><div><div class="result-rank">Recommendation #{rank}</div><div class="result-name">{name}</div></div><div class="score-pill">{score}/100</div></div><div class="result-desc">{desc}</div><div class="facts">{facts_html}</div></div>', unsafe_allow_html=True)


if 'lang' not in st.session_state:
    st.session_state.lang = None
if 'show_results' not in st.session_state:
    st.session_state.show_results = False

head1, head2 = st.columns([1, 4.7], vertical_alignment='center')
with head1:
    st.image('assets/logo.svg', width=58)
with head2:
    st.markdown('<div class="brand-card"><div class="brand-title">AB ENGITECH</div><div class="brand-sub">Business Opportunity Finder • Jodhpur</div><div class="brand-accent"></div></div>', unsafe_allow_html=True)

if not st.session_state.lang:
    intro_block('Find the right manufacturing opportunity', 'Choose your language to start. / शुरुआत के लिए अपनी भाषा चुनें।', 'en')
    c1, c2 = st.columns(2)
    if c1.button('English', type='primary', use_container_width=True):
        st.session_state.lang = 'en'; st.rerun()
    if c2.button('हिंदी', use_container_width=True):
        st.session_state.lang = 'hi'; st.rerun()
    st.stop()

lang = st.session_state.lang
t = TEXT[lang]
_, switch_col = st.columns([4, 1.2])
with switch_col:
    if st.button('हिंदी' if lang == 'en' else 'English', use_container_width=True):
        st.session_state.lang = 'hi' if lang == 'en' else 'en'
        st.session_state.show_results = False
        st.rerun()

intro_block('Find your best-fit manufacturing project' if lang == 'en' else 'अपने लिए उपयुक्त मैन्युफैक्चरिंग परियोजना खोजें', 'Answer a few quick questions. We will shortlist the best opportunities for your district and budget.' if lang == 'en' else 'कुछ आसान जानकारी भरें। हम आपके जिले और बजट के अनुसार उपयुक्त परियोजनाएं सुझाएंगे।', lang)

step_header('1', 'Location' if lang == 'en' else 'स्थान', 'Tell us where you want to start.' if lang == 'en' else 'बताएं आप व्यवसाय कहाँ शुरू करना चाहते हैं।')
display_districts = [d['name'] if lang == 'en' else d['hi'] for d in DISTRICTS]
selected_district = st.selectbox(t['district'], display_districts)
area = st.selectbox(t['area'], [t['rural'], t['urban'], t['undecided']])
close_step()

step_header('2', 'Investment' if lang == 'en' else 'निवेश', 'Choose a realistic investment range.' if lang == 'en' else 'अपना वास्तविक निवेश स्तर चुनें।')
budget_en = list(BUDGETS.keys())
budget_hi = ['₹10–20 लाख','₹20–35 लाख','₹35–50 लाख','₹50 लाख–₹1 करोड़','₹1–2 करोड़','₹2–5 करोड़','₹5 करोड़ से अधिक']
budget_display = st.selectbox(t['budget'], budget_en if lang == 'en' else budget_hi)
budget_label = budget_display if lang == 'en' else budget_en[budget_hi.index(budget_display)]
capital_options = ['Below ₹5 lakh','₹5–10 lakh','₹10–25 lakh','₹25–50 lakh','₹50 lakh–₹1 crore','Above ₹1 crore'] if lang == 'en' else ['₹5 लाख से कम','₹5–10 लाख','₹10–25 लाख','₹25–50 लाख','₹50 लाख–₹1 करोड़','₹1 करोड़ से अधिक']
capital = st.selectbox(t['capital'], capital_options)
close_step()

step_header('3', 'Resources & preference' if lang == 'en' else 'संसाधन और प्राथमिकता', 'A few details help us rank projects better.' if lang == 'en' else 'कुछ जानकारी से हम बेहतर परियोजना सुझा पाएंगे।')
land_status = st.selectbox(t['land'], [t['available'], t['arrange'], t['rent'], t['not_sure']])
land_options = list(LAND_EN.keys()) if lang == 'en' else list(LAND_HI.keys())
land_size = st.selectbox(t['land_size'], land_options)
priority = st.selectbox(t['priority'], [t['best'], t['low'], t['growth'], t['govt'], t['simple'], t['mineral'], t['construction']])
close_step()

district = next(d for d in DISTRICTS if (d['name'] if lang == 'en' else d['hi']) == selected_district)
bmin, bmax = BUDGETS[budget_label]
land_avail = (LAND_EN if lang == 'en' else LAND_HI)[land_size]
ranked = sorted([(score_project(p, district, bmin, bmax, land_avail, priority, t), p) for p in PROJECTS], key=lambda x: x[0], reverse=True)

if st.button(t['find'], type='primary', use_container_width=True):
    st.session_state.show_results = True

if st.session_state.show_results:
    st.markdown(f'<div class="results-title">{t["results"]}</div>', unsafe_allow_html=True)
    top = ranked[:3]
    for idx, (score, p) in enumerate(top, 1):
        name = p['name_en'] if lang == 'en' else p['name_hi']
        desc = p['desc_en'] if lang == 'en' else p['desc_hi']
        invest = f'₹{p["min_budget"]}–{p["max_budget"]} L' if lang == 'en' else f'₹{p["min_budget"]}–{p["max_budget"]} लाख'
        space = f'{p["land_min"]:,}–{p["land_max"]:,} sq ft' if lang == 'en' else f'{p["land_min"]:,}–{p["land_max"]:,} वर्गफुट'
        result_card(idx, name, score, desc, [(t['investment'], invest),(t['space'], space),(t['power'], f'{p["power_min"]}–{p["power_max"]} kW'),(t['manpower'], f'{p["manpower_min"]}–{p["manpower_max"]}')])
        with st.expander(t['details']):
            st.write(f'**{t["capacity"]}:** {p["capacity_en"] if lang == "en" else p["capacity_hi"]}')
            complexity = p['regulatory'] if lang == 'en' else {'Low':'कम','Medium':'मध्यम','High':'उच्च'}.get(p['regulatory'], p['regulatory'])
            st.write(f'**{t["complexity"]}:** {complexity}')
            st.write(f'**{t["support"]}:**')
            st.info(t['pmegp_ok'] if p['pmegp'] and p['min_budget'] <= 50 else t['pmegp_high'])
            if p['rips']:
                st.info(t['rips'])

    st.markdown(f'<div class="lead-box"><h3>{t["lead"]}</h3><p>{t["lead_help"]}</p></div>', unsafe_allow_html=True)
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
