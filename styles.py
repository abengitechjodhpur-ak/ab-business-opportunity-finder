import streamlit as st


def apply_styles():
    st.markdown('''
<style>
:root{--orange:#ef8429;--green:#087a5c;--ink:#172033;--muted:#667085}
.block-container{max-width:1160px;padding-top:1.4rem;padding-bottom:3rem}
[data-testid="stAppViewContainer"]{background:linear-gradient(180deg,#fff 0%,#fafaf8 100%)}
[data-testid="stSidebar"]>div:first-child{background:linear-gradient(180deg,#ffffff,#fff8ef)}
.hero{background:linear-gradient(135deg,#fff7ec 0%,#ffffff 50%,#edf9f5 100%);border:1px solid #ead8c7;border-radius:24px;padding:24px 28px;box-shadow:0 12px 32px rgba(23,32,51,.07);margin-bottom:18px}
.hero h1{font-size:2.3rem;line-height:1.05;margin:0 0 8px;color:var(--ink)}
.hero p{margin:0;color:#475467;font-size:1.05rem}.chips{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}.chip{background:#fff;border:1px solid #ead8c7;border-radius:999px;padding:5px 10px;font-size:.82rem;font-weight:650;color:#765020}
.panel{background:#fff;border:1px solid #eaecf0;border-radius:20px;padding:20px 22px 12px;box-shadow:0 8px 22px rgba(15,23,42,.04);margin-bottom:18px}.panel h3{margin:0;color:var(--ink)}.panel p{color:var(--muted);margin:.25rem 0 .8rem}
.rank{display:inline-block;background:var(--ink);color:#fff;padding:4px 10px;border-radius:999px;font-size:.8rem;font-weight:800}.score{background:linear-gradient(135deg,var(--green),#0f916e);color:#fff;border-radius:15px;padding:10px 12px;text-align:center;font-weight:700}.score b{font-size:1.45rem}
div[data-testid="stMetric"]{background:#fbfbfc;border:1px solid #eef0f3;padding:10px;border-radius:14px}.stButton>button,.stLinkButton>a{border-radius:12px!important;font-weight:750!important}.cta{background:linear-gradient(135deg,#172033,#263650);color:#fff;border-radius:20px;padding:20px 22px;margin:18px 0 12px}.cta h3{color:#fff;margin:0 0 5px}.cta p{color:#d5dbea;margin:0}.brand-line{height:5px;background:linear-gradient(90deg,var(--orange) 0 50%,var(--green) 50% 100%);border-radius:99px;margin-bottom:16px}
@media(max-width:700px){.hero h1{font-size:1.65rem}.hero{padding:18px}.chips{display:none}}
</style>
''', unsafe_allow_html=True)


def show_brand(title, tag):
    a,b=st.columns([1.05,4.95], vertical_alignment='center')
    with a:
        st.image('assets/logo.svg', use_container_width=True)
    with b:
        st.markdown(f'''<div class="hero"><h1>{title}</h1><p>{tag}</p><div class="chips"><span class="chip">Rajasthan-first</span><span class="chip">India-ready</span><span class="chip">Subsidy-aware</span></div></div>''', unsafe_allow_html=True)
    st.markdown('<div class="brand-line"></div>', unsafe_allow_html=True)
