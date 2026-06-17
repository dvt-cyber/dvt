import streamlit as st
from google import genai
import os

# ページ設定
st.set_page_config(page_title="DVT AI Protocol Generator", layout="centered")

# =============================
# 🎨 フォント設定 (CSS)
# =============================
st.markdown("""
    <style>
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
        "warning": "※ This demo is a prototype equipped with Gemini AI.",
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
        "btn": "🤖 Generate Protocol with Gemini",
        "result_title": "## ✨ AI Suggestion Result"
    }
else:
    t = {
        "title": "🧠 Deep Vision Training",
        "sub": "活動別・コンディション連動型メニュー提案デモ",
        "desc": "活動内容と本日のコンディションから、安全で最適なプロトコルをAIが提案します。",
        "warning": "※このデモは試作版です。裏側でGemini AIが稼働しています。",
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
        "diplopia": "複視 (モノが2重に見えるか)",
        "dip_options": ["なし", "少しある", "増えている"],
        "time_label": "希望時間",
        "time_options": ["5分", "10分", "15分", "AIに任せる"],
        "btn": "🤖 Geminiにメニューを提案してもらう",
        "result_title": "## ✨ AI 提案結果"
    }

# =============================
# 1. データベース & 関数
# =============================
ACTIVITY_SKILLS = {
    "Sports / スポーツ": ["周辺視野 (Peripheral)", "視線切替 (Saccades)", "動体視力 (Dynamic VA)", "視覚反応時間 (Reaction Time)"],
    "Reading / 読書・学習": ["固視 (Fixation)", "サッカード (Saccades)", "近見作業 (Near Work)", "視覚的注意 (Visual Attention)"],
    "PC・Digital / PC作業": ["近見作業 (Near Work)", "画面内の視覚探索 (Visual Search)", "調節負荷 (Accommodation)"],
    "Daily Life / 日常生活": ["視覚探索 (Visual Search)", "図地弁別 (Figure-Ground)", "手元と周囲の切替 (Gaze Shifting)"],
    "Work / 作業・検品": ["視覚弁別 (Visual Discrimination)", "固視 (Fixation)", "注意維持 (Sustained Attention)"],
}

ACTIVITY_MENU = {
    "Sports / スポーツ": {"main": "Turbo", "sub": "Hoopie / Flash Match"},
    "Reading / 読書・学習": {"main": "Flash Match", "sub": "低負荷のTurbo"},
    "PC・Digital / PC作業": {"main": "Flash Match", "sub": "Pepper Picker"},
    "Daily Life / 日常生活": {"main": "Pepper Picker", "sub": "Turbo"},
    "Work / 作業・検品": {"main": "Flash Match", "sub": "Turbo"},
}

def judge_mode(fatigue, focus, sleep_hours, eye_strain, headache, dizziness, diplopia, mood):
    red_flags = []
    yellow_flags = []
    
    if dizziness >= 7: red_flags.append("めまい・VR酔い不安")
    if headache >= 7: red_flags.append("強い頭痛")
    if diplopia in ["増えている", "Increasing"]: red_flags.append("複視の増悪")
    if fatigue >= 8: red_flags.append("疲労度が高い")
    if eye_strain >= 8: red_flags.append("眼精疲労が強い")
    if sleep_hours < 4: red_flags.append("睡眠不足が強い")

    if 5 <= fatigue <= 7: yellow_flags.append("疲労が中等度")
    if focus <= 4: yellow_flags.append("集中力が低い")
    if 4 <= sleep_hours < 6: yellow_flags.append("睡眠がやや不足")
    if 5 <= eye_strain <= 7: yellow_flags.append("眼精疲労が中等度")

    if mood in ["いまいち", "ストレスが強い", "疲労感が強い", "Not so good", "Stressed", "Exhausted"]:
        yellow_flags.append("気分面の不調")

    if red_flags: return "Recovery", red_flags, yellow_flags
    if len(yellow_flags) >= 2: return "Easy", red_flags, yellow_flags
    if fatigue <= 3 and focus >= 8 and eye_strain <= 3 and sleep_hours >= 7: return "Hard", red_flags, yellow_flags
    return "Normal", red_flags, yellow_flags

# =============================
# 2. UI表示部分
# =============================
st.title(t["title"])
st.subheader(t["sub"])
st.write(t["desc"])
st.info(t["warning"])
st.markdown("---")

st.markdown(t["act_title"])
col1, col2 = st.columns(2)
with col1:
    activity = st.selectbox(t["act_label"], list(ACTIVITY_SKILLS.keys()))
    target_age = st.number_input(t["age_label"], min_value=10, max_value=100, value=12)
with col2:
    activity_detail = st.text_input(t["act_detail"])
    experience = st.selectbox(t["exp_label"], t["exp_options"])

st.markdown(t["cond_title"])
col3, col4 = st.columns(2)
with col3:
    fatigue = st.slider(t["fatigue"], 0, 10, 5)
    sleep_hours = st.slider(t["sleep"], 0.0, 12.0, 6.0, 0.5)
    mood = st.selectbox(t["mood"], t["mood_options"])
    focus = st.slider(t["focus"], 1, 10, 5)

with col4:
    eye_strain = st.slider(t["eyestrain"], 0, 10, 3)
    headache = st.slider(t["headache"], 0, 10, 0)
    dizziness = st.slider(t["dizziness"], 0, 10, 0)
    diplopia = st.selectbox(t["diplopia"], t["dip_options"])

desired_time = st.selectbox(t["time_label"], t["time_options"])
st.markdown("---")

# =============================
# 3. Gemini連携 & 判定結果
# =============================
if st.button(t["btn"], use_container_width=True):
    
    # ルールベースの判定
    mode, red_flags, yellow_flags = judge_mode(fatigue, focus, sleep_hours, eye_strain, headache, dizziness, diplopia, mood)
    menu = ACTIVITY_MENU[activity]
    
    st.markdown(t["result_title"])
    
    # 警告表示
    if mode == "Recovery":
        st.error(f"🚨 判定: {mode} (安全優先 / 休止検討)")
    elif mode == "Easy":
        st.warning(f"⚠️ 判定: {mode} (低負荷 / 継続優先)")
    elif mode == "Hard":
        st.success(f"🔥 判定: {mode} (高負荷 / チャレンジ)")
    else:
        st.info(f"✅ 判定: {mode} (標準 / 標準負荷)")

    # ユーザー状況の文字列化（プロンプト用）
    user_status = f"""
    対象年齢: {target_age}歳, 経験: {experience}
    活動カテゴリ: {activity}, 具体的な内容: {activity_detail if activity_detail else '特になし'}
    体調モード: {mode}
    アラート(赤): {', '.join(red_flags) if red_flags else 'なし'}
    アラート(黄): {', '.join(yellow_flags) if yellow_flags else 'なし'}
    システム推奨ゲーム: メイン {menu['main']}, サブ {menu['sub']}
    """

    # Geminiへのプロンプト
    prompt = f"""
    あなたは優秀なビジョントレーナーです。以下のユーザーの今日のコンディションと活動目的に合わせて、最適なトレーニングのアドバイスを150文字程度で、温かく励ますようなトーンで出力してください。また、日常でできるちょっとした目の使い方の工夫（Bridge task）を1つ提案してください。

    【ユーザー情報】
    {user_status}
    """

    try:
        # APIキーをSecretsから取得してGeminiクライアントを初期化
        api_key = st.secrets["GEMINI_API_KEY"]
        client = genai.Client(api_key=api_key)
        
        with st.spinner("Geminiがパーソナライズされたメニューを考えています...🧠"):
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            
            st.markdown("### 💬 Gemini専属トレーナーからのアドバイス")
            st.write(response.text)

    except Exception as e:
        st.error(f"AIの読み込みに失敗しました。詳細: {e}")

    # 以降は通常の詳細表示
    st.markdown("---")
    st.write(f"**システム推奨 Main:** {menu['main']} / **Sub:** {menu['sub']}")
    if red_flags or yellow_flags:
        for flag in red_flags: st.write(f"- 🔴 {flag}")
        for flag in yellow_flags: st.write(f"- 🟡 {flag}")
