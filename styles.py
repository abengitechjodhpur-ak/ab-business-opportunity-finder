import streamlit as st


def apply_styles():
    st.markdown('''
<style>
:root{--orange:#ef8429;--green:#087a5c;--ink:#172033;--muted:#667085}
.block-container{max-width:1160px;padding-top:1.1rem;padding-bottom:3rem}
[data-testid="stAppViewContainer"]{background:linear-gradient(180deg,#fff 0%,#fafaf8 100%)}
[data-testid="stSidebar"]>div:first-child{background:linear-gradient(180deg,#ffffff,#fff8ef)}
.hero{background:linear-gradient(135deg,#fff7ec 0%,#ffffff 50%,#edf9f5 100%);border:1px solid #ead8c7;border-radius:22px;padding:22px 26px;box-shadow:0 10px 28px rgba(23,32,51,.06);margin-bottom:14px}
.hero h1{font-size:2rem;line-height:1.08;margin:0 0 8px;color:var(--ink);max-width:900px}
.hero p{margin:0;color:#475467;font-size:1rem}.chips{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}.chip{background:#fff;border:1px solid #ead8c7;border-radius:999px;padding:5px 10px;font-size:.82rem;font-weight:650;color:#765020}
.panel{background:#fff;border:1px solid #eaecf0;border-radius:18px;padding:18px 20px 10px;box-shadow:0 8px 22px rgba(15,23,42,.035);margin-bottom:16px}.panel h3{margin:0;color:var(--ink)}.panel p{color:var(--muted);margin:.25rem 0 .75rem}
.rank{display:inline-block;background:var(--ink);color:#fff;padding:4px 10px;border-radius:999px;font-size:.8rem;font-weight:800}.score{background:linear-gradient(135deg,var(--green),#0f916e);color:#fff;border-radius:15px;padding:10px 12px;text-align:center;font-weight:700}.score b{font-size:1.45rem}
div[data-testid="stMetric"]{background:#fbfbfc;border:1px solid #eef0f3;padding:10px;border-radius:14px}.stButton>button,.stLinkButton>a{border-radius:12px!important;font-weight:750!important}.cta{background:linear-gradient(135deg,#172033,#263650);color:#fff;border-radius:20px;padding:20px 22px;margin:18px 0 12px}.cta h3{color:#fff;margin:0 0 5px}.cta p{color:#d5dbea;margin:0}.brand-line{height:4px;background:linear-gradient(90deg,var(--orange) 0 50%,var(--green) 50% 100%);border-radius:99px;margin-bottom:14px}
.sidebar-logo{max-width:120px;margin:4px auto 8px;display:block}.sidebar-brand{text-align:center;color:#667085;font-size:.85rem;margin-bottom:14px}.side-rule{height:1px;background:#ead8c7;margin:10px 0 16px}
@media(max-width:900px){.hero h1{font-size:1.75rem}.hero{padding:18px 20px}}
@media(max-width:700px){.hero h1{font-size:1.5rem}.hero{padding:16px}.chips{display:none}.block-container{padding-left:.85rem;padding-right:.85rem}.sidebar-logo{max-width:95px}}
</style>
''', unsafe_allow_html=True)


def show_brand(title, tag, lang='en'):
    badges = ['Rajasthan-first','India-ready','Subsidy-aware'] if lang == 'en' else ['राजस्थान से शुरुआत','पूरे भारत के लिए तैयार','सब्सिडी जानकारी सहित']
    badge_html=''.join(f'<span class="chip">{b}</span>' for b in badges)
    st.markdown(f'''<div class="hero"><h1>{title}</h1><p>{tag}</p><div class="chips">{badge_html}</div></div>''', unsafe_allow_html=True)
    st.markdown('<div class="brand-line"></div>', unsafe_allow_html=True)


def show_sidebar_brand():
    st.markdown('''<img src="assets/logo.svg" class="sidebar-logo"><div class="sidebar-brand">AB ENGITECH • Jodhpur</div><div class="side-rule"></div>''', unsafe_allow_html=True)
