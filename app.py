import streamlit as st

st.set_page_config(
    page_title="DVT AI Protocol Generator",
    layout="centered"
)

st.title("DVT Vision Training")
st.subheader("AIプロトコル提案デモ")
st.write(
    "活動内容と本日のコンディションを入力すると、"
    "Vivid Visionのゲーム候補と負荷レベルを提案します。"
)

st.info(
    "このデモは医学的診断や治療方針を決定するものではありません。"
    "DVTメニュー候補を整理するための試作です。"
)

st.markdown("---")


# =============================
# 活動カテゴリごとのゲーム候補
# =============================

ACTIVITY_MENU = {
    "スポーツ": {
        "games": ["Turbo", "Hoopie", "Flash Match"],
        "advice": "反応や周辺認識を使うゲームを中心に提案します。"
    },
    "読書・学習": {
        "games": ["Flash Match", "Pepper Picker"],
        "advice": "短時間で集中しやすいゲームを中心に提案します。"
    },
    "PC・デジタル作業": {
        "games": ["Flash Match", "Pepper Picker"],
        "advice": "画面作業後でも負担が強くなりにくい内容を優先します。"
    },
    "家事・日常生活": {
        "games": ["Pepper Picker", "Turbo"],
        "advice": "探す・選ぶ動きに近いゲームを中心に提案します。"
    },
    "ライン作業・検品": {
        "games": ["Flash Match", "Turbo"],
        "advice": "正確性と注意の維持を意識したゲームを提案します。"
    },
    "子どもとの遊び": {
        "games": ["Hoopie", "Turbo"],
        "advice": "楽しく取り組みやすいゲームを中心に提案します。"
    },
}


# =============================
# モード別アドバイス
# =============================

MODE_ADVICE = {
    "Recovery": "今日は無理に行わず、休止またはごく短時間にします。",
    "Easy": "今日は短時間・低負荷で行います。",
    "Normal": "今日は標準的な負荷で開始します。",
    "Hard": "今日は少し負荷を上げたメニューも検討できます。"
}


# =============================
# コンディション判定
# =============================

def judge_mode(
    fatigue,
    focus,
    sleep_hours,
    eye_strain,
    headache,
    dizziness,
    diplopia,
    mood
):
    red_flags = []
    yellow_flags = []

    # Recovery寄りの条件
    if fatigue >= 8:
        red_flags.append("疲労度が高い")
    if sleep_hours < 4:
        red_flags.append("睡眠不足が強い")
    if eye_strain >= 8:
        red_flags.append("眼精疲労が強い")
    if headache >= 7:
        red_flags.append("頭痛が強い")
    if dizziness >= 7:
        red_flags.append("めまい・VR酔い不安が強い")
    if diplopia == "増えている":
        red_flags.append("複視が増えている")

    # Easy寄りの条件
    if 5 <= fatigue <= 7:
        yellow_flags.append("疲労が中等度")
    if 4 <= sleep_hours < 6:
        yellow_flags.append("睡眠がやや不足")
    if focus <= 4:
        yellow_flags.append("集中力が低い")
    if 5 <= eye_strain <= 7:
        yellow_flags.append("眼精疲労が中等度")
    if 4 <= headache <= 6:
        yellow_flags.append("軽度から中等度の頭痛")
    if 4 <= dizziness <= 6:
        yellow_flags.append("VR酔い不安がある")
    if diplopia == "少しある":
        yellow_flags.append("複視が少しある")
    if mood in ["いまいち", "ストレスが強い", "疲労感が強い"]:
        yellow_flags.append("気分面の不調がある")

    # 判定
    if red_flags:
        return "Recovery", red_flags, yellow_flags

    if len(yellow_flags) >= 2:
        return "Easy", red_flags, yellow_flags

    if (
        fatigue <= 3
        and focus >= 8
        and sleep_hours >= 7
        and eye_strain <= 3
        and headache <= 2
        and dizziness <= 2
        and diplopia == "なし"
        and mood == "よい"
    ):
        return "Hard", red_flags, yellow_flags

    return "Normal", red_flags, yellow_flags


# =============================
# 入力画面
# =============================

st.markdown("### 1. 活動カテゴリ")

activity = st.selectbox(
    "目的に近い活動を選択してください",
    list(ACTIVITY_MENU.keys())
)

activity_detail = st.text_input(
    "具体的な内容があれば入力してください",
    placeholder="例：サッカー、読書、PC作業、料理、検品、キャッチボール"
)

target_age = st.number_input(
    "対象年齢",
    min_value=10,
    max_value=100,
    value=12,
    step=1
)

experience = st.selectbox(
    "VR / DVT経験",
    ["初めて", "少し経験あり", "慣れている"]
)

st.markdown("---")

st.markdown("### 2. 本日のコンディション")

sleep_hours = st.slider(
    "睡眠時間",
    min_value=0.0,
    max_value=12.0,
    value=6.0,
    step=0.5
)

fatigue = st.slider(
    "疲労度 0:なし 〜 10:強い",
    min_value=0,
    max_value=10,
    value=5
)

focus = st.slider(
    "集中できそうか 1:低い 〜 10:高い",
    min_value=1,
    max_value=10,
    value=5
)

mood = st.selectbox(
    "気分",
    ["よい", "普通", "いまいち", "ストレスが強い", "疲労感が強い"]
)

eye_strain = st.slider(
    "眼精疲労 0:なし 〜 10:強い",
    min_value=0,
    max_value=10,
    value=3
)

headache = st.slider(
    "頭痛 0:なし 〜 10:強い",
    min_value=0,
    max_value=10,
    value=0
)

dizziness = st.slider(
    "めまい・VR酔い不安 0:なし 〜 10:強い",
    min_value=0,
    max_value=10,
    value=0
)

diplopia = st.selectbox(
    "複視",
    ["なし", "少しある", "増えている"]
)

desired_time = st.selectbox(
    "希望時間",
    ["5分", "10分", "15分", "AIに任せる"]
)

st.markdown("---")


# =============================
# 結果表示
# =============================

if st.button("DVTメニュー候補を提案する"):

    mode, red_flags, yellow_flags = judge_mode(
        fatigue=fatigue,
        focus=focus,
        sleep_hours=sleep_hours,
        eye_strain=eye_strain,
        headache=headache,
        dizziness=dizziness,
        diplopia=diplopia,
        mood=mood
    )

    menu = ACTIVITY_MENU[activity]

    st.markdown("### 提案結果")

    if activity_detail.strip():
        st.write(f"具体内容：{activity_detail}")

    if mode == "Recovery":
        st.error("本日の判定：Recovery")
    elif mode == "Easy":
        st.warning("本日の判定：Easy")
    elif mode == "Hard":
        st.success("本日の判定：Hard")
    else:
        st.info("本日の判定：Normal")

    st.markdown("#### 推奨Vivid Visionゲーム")

    for game in menu["games"]:
        st.write(f"- {game}")

   if activity_detail.strip():
    st.write(f"具体内容：{activity_detail}")

    st.markdown("#### 判定に影響した条件")

    if red_flags:
        st.write("Recovery寄りの条件：")
        for flag in red_flags:
            st.write(f"- {flag}")

    if yellow_flags:
        st.write("Easy寄りの条件：")
        for flag in yellow_flags:
            st.write(f"- {flag}")

    if not red_flags and not yellow_flags:
        st.write("- 大きな不調入力はありません。")

    st.markdown("#### 中止・中断の目安")
    st.write("- 複視が増える")
    st.write("- 頭痛、めまい、吐き気が出る")
    st.write("- 眼精疲労が強くなる")
    st.write("- 気分不快が出る")
    st.write("- 本人が続けたくないと訴える")

    st.caption(
        "この提案はデモ用です。実際の運用では、DVT担当者による確認が必要です。"
    )
