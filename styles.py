import streamlit as st


def apply_styles():
    st.markdown('''
<style>
:root{
  --orange:#EF8429;
  --orange-dark:#C86412;
  --green:#087A5C;
  --ink:#18212F;
  --muted:#667085;
  --line:#E7E9EE;
  --soft:#F7F8FA;
}
html, body, [class*="css"] {font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;}
.block-container{max-width:760px;padding-top:.75rem;padding-bottom:4rem;padding-left:1rem;padding-right:1rem}
[data-testid="stAppViewContainer"]{background:#F6F7F9}
[data-testid="stHeader"]{background:rgba(246,247,249,.92)}
#MainMenu, footer{visibility:hidden}

/* Top brand */
.brand-card{background:#fff;border:1px solid var(--line);border-radius:18px;padding:14px 16px;margin-bottom:14px;box-shadow:0 3px 14px rgba(16,24,40,.04)}
.brand-title{font-size:1.32rem;font-weight:800;line-height:1.15;color:var(--ink);margin:0}
.brand-sub{font-size:.9rem;color:var(--muted);margin-top:4px}
.brand-accent{height:3px;border-radius:99px;background:linear-gradient(90deg,var(--orange) 0 50%,var(--green) 50% 100%);margin-top:10px}

/* Step cards */
.step-card{background:#fff;border:1px solid var(--line);border-radius:18px;padding:16px 16px 8px;margin:12px 0;box-shadow:0 3px 14px rgba(16,24,40,.035)}
.step-row{display:flex;align-items:center;gap:10px;margin-bottom:2px}
.step-num{width:28px;height:28px;border-radius:9px;background:#FFF1E5;color:var(--orange-dark);font-weight:800;display:flex;align-items:center;justify-content:center;font-size:.85rem}
.step-title{font-size:1.02rem;font-weight:750;color:var(--ink)}
.step-help{font-size:.84rem;color:var(--muted);margin:2px 0 8px 38px}

/* Inputs */
div[data-baseweb="select"]>div, div[data-testid="stTextInput"] input{min-height:48px;border-radius:12px!important;background:#FBFCFD;border-color:#DDE1E7!important}
label[data-testid="stWidgetLabel"] p{font-size:.88rem;font-weight:650;color:#344054}
.stButton>button, .stFormSubmitButton>button, .stLinkButton>a{min-height:50px;border-radius:12px!important;font-weight:750!important;font-size:.98rem!important}
.stButton>button[kind="primary"], .stFormSubmitButton>button[kind="primary"]{background:var(--green)!important;border-color:var(--green)!important}

/* Intro */
.intro{text-align:center;padding:8px 8px 2px}
.intro h1{font-size:1.65rem;line-height:1.15;color:var(--ink);margin:.2rem 0 .45rem}
.intro p{font-size:.94rem;color:var(--muted);margin:0 auto;max-width:610px}
.trust-row{display:flex;justify-content:center;gap:8px;flex-wrap:wrap;margin:12px 0 2px}
.trust{background:#fff;border:1px solid var(--line);border-radius:999px;padding:6px 10px;font-size:.78rem;color:#475467}

/* Results */
.results-title{font-size:1.25rem;font-weight:800;color:var(--ink);margin:1.5rem 0 .5rem}
.result-card{background:#fff;border:1px solid var(--line);border-radius:18px;padding:16px;margin:10px 0;box-shadow:0 4px 18px rgba(16,24,40,.045)}
.result-head{display:flex;align-items:flex-start;justify-content:space-between;gap:12px}
.result-name{font-size:1.08rem;font-weight:800;color:var(--ink);line-height:1.2}
.result-rank{font-size:.72rem;font-weight:800;color:var(--orange-dark);text-transform:uppercase;letter-spacing:.04em;margin-bottom:4px}
.score-pill{white-space:nowrap;background:#EAF7F2;color:#08654D;border-radius:999px;padding:7px 10px;font-size:.83rem;font-weight:800}
.result-desc{color:#667085;font-size:.88rem;margin:8px 0 12px}
.facts{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.fact{background:#F8F9FB;border-radius:12px;padding:10px}
.fact-label{font-size:.68rem;text-transform:uppercase;letter-spacing:.04em;color:#98A2B3;font-weight:750}
.fact-value{font-size:.9rem;color:#344054;font-weight:700;margin-top:2px}

/* Lead */
.lead-box{background:#18212F;border-radius:18px;padding:18px;margin:18px 0 10px;color:#fff}
.lead-box h3{font-size:1.1rem;margin:0 0 5px;color:#fff}
.lead-box p{font-size:.86rem;color:#D0D5DD;margin:0}
.note{font-size:.76rem;color:#98A2B3;text-align:center;margin-top:14px}

/* Streamlit container borders */
div[data-testid="stVerticalBlockBorderWrapper"]{border:0!important;background:transparent!important;padding:0!important}

@media(max-width:640px){
  .block-container{padding-top:.55rem;padding-left:.75rem;padding-right:.75rem}
  .intro h1{font-size:1.42rem}
  .brand-title{font-size:1.08rem}
  .brand-sub{font-size:.78rem}
  .step-card{padding:14px 13px 7px;border-radius:16px}
  .step-help{margin-left:38px}
  .facts{grid-template-columns:1fr 1fr}
  div[data-baseweb="select"]>div{min-height:52px}
}
</style>
''', unsafe_allow_html=True)


def intro_block(title, subtitle, lang='en'):
    chips = ['District-based', 'Budget matched', 'Subsidy-aware'] if lang == 'en' else ['जिला आधारित', 'बजट अनुसार', 'सब्सिडी जानकारी']
    chip_html = ''.join(f'<span class="trust">{x}</span>' for x in chips)
    st.markdown(f'''<div class="intro"><h1>{title}</h1><p>{subtitle}</p><div class="trust-row">{chip_html}</div></div>''', unsafe_allow_html=True)


def step_header(num, title, help_text):
    st.markdown(f'''<div class="step-card"><div class="step-row"><div class="step-num">{num}</div><div class="step-title">{title}</div></div><div class="step-help">{help_text}</div>''', unsafe_allow_html=True)


def close_step():
    st.markdown('</div>', unsafe_allow_html=True)


def result_card_start(rank, name, score, desc):
    st.markdown(f'''<div class="result-card"><div class="result-head"><div><div class="result-rank">Recommendation #{rank}</div><div class="result-name">{name}</div></div><div class="score-pill">{score}/100</div></div><div class="result-desc">{desc}</div>''', unsafe_allow_html=True)


def fact_grid(items):
    html = '<div class="facts">'
    for label, value in items:
        html += f'<div class="fact"><div class="fact-label">{label}</div><div class="fact-value">{value}</div></div>'
    html += '</div></div>'
    st.markdown(html, unsafe_allow_html=True)


def lead_intro(title, body):
    st.markdown(f'<div class="lead-box"><h3>{title}</h3><p>{body}</p></div>', unsafe_allow_html=True)
