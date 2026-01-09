import json
import time
import pandas as pd
import streamlit as st
from llm_client import generate_reply
from prompts import build_prompt

st.set_page_config(page_title="SALO • Batch Mode", layout="wide")


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
  background: radial-gradient(700px 240px at 15% 20%, rgba(34,211,238,0.25), transparent 55%),
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
  <h2 style="margin:0;">📦 Batch Mode</h2>
  <div class="small">Upload a CSV with a <b>review</b> column → generate results → download CSV.</div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Batch settings")
    business_type = st.selectbox("Business type", ["Restaurant","Online Store","Delivery Service","SaaS App","Gym","Other"])
    tone = st.selectbox("Tone", ["Professional","Friendly","Apologetic","Firm (still respectful)"])
    language = st.selectbox("Language", ["English","Arabic","Both"])
    max_rows = st.slider("Max rows (free-tier friendly)", 1, 200, 10)
    delay_sec = st.slider("Delay per row (avoid 429)", 0.0, 3.0, 1.0, 0.5)

st.write("")
left, right = st.columns([1.05, 0.95])

with left:
    st.markdown('<div class="panel fade">', unsafe_allow_html=True)
    st.subheader("Upload")
    uploaded = st.file_uploader("CSV file", type=["csv"])
    st.caption("CSV must include a column named: review")
    st.markdown('</div>', unsafe_allow_html=True)

    df = None
    if uploaded is not None:
        try:
            df = pd.read_csv(uploaded)
        except Exception as e:
            st.error(f"CSV read error: {e}")
            st.stop()

        if "review" not in df.columns:
            st.error("Missing required column: review")
            st.stop()

        st.markdown('<div class="panel fade">', unsafe_allow_html=True)
        st.subheader("Preview")
        st.write("Columns:", list(df.columns))
        st.dataframe(df.head(10), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel fade">', unsafe_allow_html=True)
    st.subheader("Run")
    run = st.button("⚡ Run batch generation", use_container_width=True, disabled=(df is None))
    st.caption("Tip: Keep rows low on free tier.")
    st.markdown('</div>', unsafe_allow_html=True)

    if run and df is not None:
        out_rows = []
        total = min(len(df), max_rows)
        prog = st.progress(0)
        status = st.empty()

        for i in range(total):
            review = str(df.loc[i, "review"]).strip()
            status.write(f"Processing {i+1}/{total}...")

            if not review:
                out_rows.append({
                    "review": "",
                    "sentiment": "",
                    "issue_type": "",
                    "reply_best": "",
                    "reply_short": "",
                    "reply_alternative": "",
                    "internal_fix_suggestions": "",
                    "status": "skipped_empty",
                })
                prog.progress(int(((i+1)/total)*100))
                continue

            prompt = build_prompt(review, business_type, tone, language)
            raw = generate_reply(prompt)

            try:
                data = json.loads(raw)
                out_rows.append({
                    "review": review,
                    "sentiment": data.get("sentiment",""),
                    "issue_type": data.get("issue_type",""),
                    "reply_best": data.get("replies",{}).get("best",""),
                    "reply_short": data.get("replies",{}).get("short",""),
                    "reply_alternative": data.get("replies",{}).get("alternative",""),
                    "internal_fix_suggestions": " | ".join(data.get("internal_fix_suggestions",[])),
                    "status": "ok",
                })
            except Exception:
                out_rows.append({
                    "review": review,
                    "sentiment": "",
                    "issue_type": "",
                    "reply_best": "",
                    "reply_short": "",
                    "reply_alternative": "",
                    "internal_fix_suggestions": "",
                    "status": "json_failed",
                })

            prog.progress(int(((i+1)/total)*100))
            time.sleep(delay_sec)

        status.write("Done ✅")
        out_df = pd.DataFrame(out_rows)

        st.markdown('<div class="panel fade">', unsafe_allow_html=True)
        st.subheader("Summary")
        c1, c2, c3 = st.columns(3)
        c1.metric("Processed", len(out_df))
        c2.metric("OK", int((out_df["status"] == "ok").sum()))
        c3.metric("Failed/Skipped", int((out_df["status"] != "ok").sum()))
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="panel fade">', unsafe_allow_html=True)
        st.subheader("Issue distribution")
        if out_df["issue_type"].astype(str).str.len().sum() > 0:
            st.bar_chart(out_df["issue_type"].value_counts())
        else:
            st.info("No issue_type data to chart yet.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="panel fade">', unsafe_allow_html=True)
        st.subheader("Results")
        st.dataframe(out_df, use_container_width=True)
        st.download_button(
            "⬇️ Download results CSV",
            data=out_df.to_csv(index=False).encode("utf-8"),
            file_name="batch_review_replies.csv",
            mime="text/csv",
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
