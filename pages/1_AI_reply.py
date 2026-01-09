
import json
import streamlit as st
from llm_client import generate_reply
from prompts import build_prompt

st.set_page_config(page_title="SALO • AI Reply", layout="wide")


if "result" not in st.session_state:
    st.session_state.result = None
if "review_text" not in st.session_state:
    st.session_state.review_text = ""

st.markdown("""
<style>
.block-container {max-width: 1200px; padding-top: 1.8rem;}
.panel{
  padding: 18px; border-radius: 18px;
  background: rgba(17,24,39,0.70);
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: 0 10px 30px rgba(0,0,0,0.28);
}
.hero2{
  padding: 18px; border-radius: 18px;
  background: radial-gradient(700px 240px at 15% 20%, rgba(124,58,237,0.28), transparent 55%),
              linear-gradient(180deg, rgba(17,24,39,0.85), rgba(17,24,39,0.65));
  border: 1px solid rgba(255,255,255,0.08);
}
.fade{animation: fadeIn 0.6s ease-in-out;}
@keyframes fadeIn{from{opacity:0; transform:translateY(8px);} to{opacity:1; transform:translateY(0);}}
.small{color: rgba(229,231,235,0.72); font-size: 13px;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero2 fade">
  <h2 style="margin:0;"> AI Reply Generator</h2>
  <div class="small">Paste a review → get sentiment + issue type + 3 reply options + internal fixes.</div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Settings")
    business_type = st.selectbox("Business type", ["Restaurant","Online Store","Delivery Service","SaaS App","Gym","Other"])
    tone = st.selectbox("Tone", ["Professional","Friendly","Apologetic","Firm (still respectful)"])
    language = st.selectbox("Language", ["English","Arabic","Both"])
    st.divider()
    if st.button("Load sample"):
        st.session_state.review_text = "Too bad experience, too much salt."
        st.session_state.result = None
    if st.button("Reset"):
        st.session_state.review_text = ""
        st.session_state.result = None

st.write("")
left, right = st.columns([1.1, 0.9])

with left:
    st.markdown('<div class="panel fade">', unsafe_allow_html=True)
    st.subheader("Input")
    review = st.text_area(
        "Customer review",
        height=170,
        value=st.session_state.review_text,
        placeholder="e.g., Delivery was late and food arrived cold..."
    )
    st.session_state.review_text = review

    st.caption("Tip: Keep it short. Don’t paste private customer data.")

    gen_col1, gen_col2 = st.columns([1,1])
    with gen_col1:
        generate = st.button("✨ Generate", use_container_width=True)
    with gen_col2:
        clear = st.button("Clear", use_container_width=True)

    if clear:
        st.session_state.review_text = ""
        st.session_state.result = None
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    if generate:
        if not review.strip():
            st.warning("Paste a review first.")
        else:
            with st.spinner("Generating smart output..."):
                prompt = build_prompt(review, business_type, tone, language)
                raw = generate_reply(prompt)

            try:
                st.session_state.result = json.loads(raw)
            except Exception:
                st.error("AI returned non-JSON output. Raw output below:")
                st.code(raw)
                st.stop()

with right:
    st.markdown('<div class="panel fade">', unsafe_allow_html=True)
    st.subheader("Output")

    if not st.session_state.result:
        st.info("Generate to see results here.")
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

    data = st.session_state.result

    m1, m2 = st.columns(2)
    m1.metric("Sentiment", str(data.get("sentiment","")).title())
    m2.metric("Issue", str(data.get("issue_type","")).replace("_"," ").title())

    tabs = st.tabs(["Replies", "Insights", "Export"])

    with tabs[0]:
        st.markdown("**Best reply**")
        st.text_area("best", data["replies"]["best"], height=120, label_visibility="collapsed")
        st.markdown("**Short reply**")
        st.text_area("short", data["replies"]["short"], height=90, label_visibility="collapsed")
        st.markdown("**Alternative reply**")
        st.text_area("alt", data["replies"]["alternative"], height=120, label_visibility="collapsed")
        st.caption("Click inside a reply box and Ctrl+C to copy.")

    with tabs[1]:
        st.markdown("**Key points**")
        for p in data.get("key_points", []):
            st.write(f"• {p}")
        st.markdown("**Internal fixes (not public)**")
        for s in data.get("internal_fix_suggestions", []):
            st.write(f"• {s}")

    with tabs[2]:
        st.download_button(
            "⬇️ Download JSON report",
            data=json.dumps(data, ensure_ascii=False, indent=2),
            file_name="review_reply_report.json",
            mime="application/json",
            use_container_width=True
        )

    st.markdown('</div>', unsafe_allow_html=True)
