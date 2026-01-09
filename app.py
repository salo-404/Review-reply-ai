import streamlit as st

st.set_page_config(page_title="SALO • Home", layout="wide")

st.markdown("""
<style>
.block-container {max-width: 1200px; padding-top: 2.2rem;}
.hero{
  padding: 30px;
  border-radius: 22px;
  background:
    radial-gradient(900px 380px at 10% 10%, rgba(124,58,237,0.40), transparent 60%),
    radial-gradient(900px 380px at 90% 30%, rgba(34,211,238,0.25), transparent 55%),
    linear-gradient(180deg, rgba(17,24,39,0.92), rgba(17,24,39,0.68));
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: 0 14px 50px rgba(0,0,0,0.35);
}
.badge{
  display:inline-block; padding:6px 12px; border-radius:999px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.12);
  font-size: 12px; letter-spacing: 0.5px;
}
.h1{font-size: 44px; font-weight: 900; letter-spacing:-0.8px; margin: 14px 0 6px;}
.sub{color: rgba(229,231,235,0.78); font-size: 16px; max-width: 850px; line-height: 1.5;}
.card{
  padding: 18px; border-radius: 18px;
  background: rgba(17,24,39,0.70);
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: 0 10px 30px rgba(0,0,0,0.28);
  height: 100%;
}
.kpi{color: rgba(229,231,235,0.72); font-size: 13px; margin-top: 8px;}
.fade{animation: fadeIn 0.65s ease-in-out;}
@keyframes fadeIn{from{opacity:0; transform:translateY(8px);} to{opacity:1; transform:translateY(0);}}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero fade">
  <div class="badge">SALO • AI Customer Ops</div>
  <div class="h1">Welcome to SALO Reply Generator</div>
  <div class="sub">
    Instantly turn customer reviews into professional replies and actionable insights.
    Built with <b>Python</b>, <b>Streamlit</b>, and <b>Gemini</b>.
  </div>
</div>
""", unsafe_allow_html=True)

st.write("")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
    <div class="card fade">
      <h3> AI Reply</h3>
      Generate <b>3 reply options</b> + sentiment + issue type + internal fix suggestions.
      <div class="kpi">Best for: daily review handling</div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown("""
    <div class="card fade">
      <h3> Batch Mode</h3>
      Upload a CSV of reviews, process in bulk, and download a results CSV.
      <div class="kpi">Best for: businesses & agencies</div>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown("""
    <div class="card fade">
      <h3> Structured Output</h3>
      JSON-based results for stable UI, export, and scalable workflows.
      <div class="kpi">Best for: consistent brand voice</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.info("Open **AI Reply** or **Batch Mode** from the sidebar 👈")
st.write("")  # space

nav1, nav2 = st.columns(2)

with nav1:
    st.page_link("pages/1_AI_Reply.py", label="🚀 Go to AI Reply", use_container_width=True)

with nav2:
    st.page_link("pages/2_Batch_Mode.py", label="📦 Go to Batch Mode", use_container_width=True)