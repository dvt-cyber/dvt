import streamlit as st

# ページ設定（必ず一番上に書く）
st.set_page_config(page_title="DVT AI Protocol Generator", layout="centered")

# =============================
# 🎨 デザイン・フォント設定 (CSS)
# =============================
st.markdown("""
    <style>
    /* 読みやすいユニバーサルフォントの指定 */
    html, body, [class*="css"] {
        font-family: 'Helvetica Neue', Arial, 'Hiragino Kaku Gothic ProN', 'Hiragino Sans', Meiryo, sans-serif;
    }
    /* 背景色を少しだけ目に優しいオフホワイトに */
    .stApp {
        background-color: #F8F9FA;
    }
    </style>
""", unsafe_allow_html=True)

# =============================
# 🌐 言語切り替えロジック
# =============================
lang = st.radio("🌐 Language / 言語", ["日本語", "English"], horizontal=True)

# 選択された言語に応じてテキストを変える辞書
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
        "diplopia": "Diplopia (Double Vision)",
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
        "desc": "活動内容と本日のコンディションから、安全で最適なプロトコルをAIが提案します。",
        "warning": "※このデモは医学的判断や診断を行うものではありません。DVTメニュー候補を整理するための試作です。",
        "act_title": "### 📋 1. 活動カテゴリ",
        "act_label": "目的に近い活動",
        "act_detail": "具体的な内容 (任意)",
        "age_label": "対象年齢",
        "exp_label": "VR / DVT経験",
        "exp_options": ["初めて", "少し経験あり", "慣れている"],
        "cond_title": "### 🩺 2. 今日のコンディション",
        "fatigue": "疲労度 (0:なし 〜 10:強い)",
        "sleep": "前日の睡眠時間",
        "mood": "気分",
        "mood_options": ["よい", "普通", "いまいち", "ストレスが強い", "疲労感が強い"],
        "focus": "集中できそうか (1:低い 〜 10:高い)",
        "eyestrain": "眼精疲労 (0:なし 〜 10:強い)",
        "headache": "頭痛 (0:なし 〜 10:強い)",
        "dizziness": "めまい・VR酔い不安 (0:なし 〜 10:強い)",
        "diplopia": "複視",
        "dip_options": ["なし", "少しある", "増えている"],
        "time_label": "本日の希望時間",
        "time_options": ["5分", "10分", "15分", "AIに任せる"],
        "btn": "🤖 DVTメニュー候補を提案する",
        "result_title": "## ✨ AI 提案結果"
    }

# =============================
# 1. データベース（日・英併記で管理しやすく）
# =============================
ACTIVITY_SKILLS = {
    "Sports / スポーツ": ["周辺視野 (Peripheral)", "視線切替 (Saccades)", "動体視力 (Dynamic VA)", "視覚反応時間 (Reaction Time)", "眼と手・足の協調 (Eye-Hand/Foot)"],
    "Reading / 読書・学習": ["固視 (Fixation)", "サッカード (Saccades)", "近見作業 (Near Work)", "視覚的注意 (Visual Attention)"],
    "PC・Digital / PC作業": ["近見作業 (Near Work)", "画面内の視覚探索 (Visual Search)", "調節負荷 (Accommodation)", "処理速度 (Processing Speed)"],
    "Daily Life / 日常生活": ["視覚探索 (Visual Search)", "図地弁別 (Figure-Ground)", "手元と周囲の切替 (Gaze Shifting)", "空間認識 (Spatial Cognition)"],
    "Work / 作業・検品": ["視覚弁別 (Visual Discrimination)", "固視 (Fixation)", "注意維持 (Sustained Attention)", "パターン認識 (Pattern Recognition)"],
}

ACTIVITY_MENU = {
    "Sports / スポーツ": {"main": "Turbo", "sub": "Hoopie / Flash Match", "bridge": "正面を見た状態から左右へ視線を切り替える。(Shift gaze left and right from center.)"},
    "Reading / 読書・学習": {"main": "Flash Match", "sub": "低負荷のTurbo", "bridge": "短文を1行ずつ読み、行飛ばしや戻りを確認する。(Read short texts line by line.)"},
    "PC・Digital / PC作業": {"main": "Flash Match", "sub": "Pepper Picker / 低負荷Turbo", "bridge": "画面内の複数箇所を順番に確認し、手元へ視線を戻す。(Check multiple points on screen, return to hands.)"},
    "Daily Life / 日常生活": {"main": "Pepper Picker", "sub": "Turbo", "bridge": "机上の物を探す。手元と周囲をゆっくり切り替える。(Search for objects on desk.)"},
    "Work / 作業・検品": {"main": "Flash Match", "sub": "Turbo", "bridge": "似た形や色の中から違いを探す。(Find differences among similar shapes/colors.)"},
}

def get_mode_setting(mode):
    if mode == "Recovery": return {"time": "0-5 min", "target_size": "Large", "speed": "Slow", "spread": "Narrow", "goal": "Rest, Record, Light Habituation", "avoid": "Fast
