import streamlit as st

# ページ設定
st.set_page_config(page_title="DVT AI Protocol Generator", layout="centered")

# =============================
# 🎨 フォント設定 (CSS)
# =============================
st.markdown("""
    <style>
    /* 読みやすいフォントのみ指定し、色はStreamlitの標準に任せる */
    html, body, [class*="css"] {
        font-family: 'Helvetica Neue', Arial, 'Hiragino Kaku Gothic ProN', 'Hiragino Sans', Meiryo, sans-serif;
    }
    </style>
""", unsafe_allow_html=True)


# =============================
# 🌐 言語切り替えロジック
# =============================
lang = st.radio("🌐 Language / 言語", ["日本語", "English"], horizontal=True)

if lang == "English":
    t = {
        "title": "🧠 DVT Vision Training",
        "sub": "AI Protocol Generator Demo",
        "desc": "Select the activity and today's condition to get the optimal Vivid Vision protocol.",
        "warning": "※ This demo is not for medical diagnosis. It is a prototype for DVT menu suggestion.",
        "act_title": "### 📋 1. Activity Category",
        "act_label": "Select Activity",
        "act_detail": "Specific details (Optional)",
        "age_label": "Target Age",
        "exp_label": "VR Experience",
        "exp_options": ["Beginner", "Intermediate", "Advanced"],
        "cond_title": "### 🩺 2. Today's Condition",
        "fatigue": "Fatigue Level (0:None - 10:High)",
        "sleep": "Sleep Hours",
        "mood": "Mood",
        "mood_options": ["Good", "Normal", "Not so good", "Stressed", "Exhausted"],
        "focus": "Focus Level (1:Low - 10:High)",
        "eyestrain": "Eye Strain (0:None - 10:High)",
        "headache": "Headache (0:None - 10:High)",
        "dizziness": "Dizziness / VR Sickness (0:None - 10:High)",
        "diplopia": "Diplopia (Double vision)",
        "dip_options": ["None", "A little", "Increasing"],
        "time_label": "Desired Time",
        "time_options": ["5 min", "10 min", "15 min", "Let AI decide"],
        "btn": "🤖 Generate Protocol",
        "result_title": "## ✨ AI Suggestion Result"
    }
else:
    t = {
        "title": "🧠 DVT Vision Training",
        "sub": "活動別・コンディション連動型メニュー提案デモ",
        "desc": "活動内容と本日の
