import streamlit as st

st.set_page_config(
    page_title="DVT AI Menu Suggestion",
    layout="centered"
)

st.title("DVT Vision Training Menu")
st.subheader("活動別・コンディション連動型メニュー提案デモ")




st.info(
    "このデモは医学的判断や診断を行うものではありません。"
    "入力内容に応じて、DVTメニュー候補を整理するための試作です。"
)

st.markdown("---")


# -----------------------------
# 活動カテゴリごとの視覚スキル
# -----------------------------
ACTIVITY_SKILLS = {
    "スポーツ": [
        "周辺視野",
        "視線切替",
        "動体視力",
        "視覚反応時間",
        "眼と手・足の協調",
        "状況認識",
    ],
    "読書・学習": [
        "固視",
        "サッカード",
        "近見作業",
        "視線移動",
        "視覚的注意",
        "眼球運動持久力",
    ],
    "PC・デジタル作業": [
        "近見作業",
        "画面内の視覚探索",
        "視線切替",
        "調節負荷",
        "注意維持",
        "処理速度",
    ],
    "家事・日常生活": [
        "視覚探索",
        "図地弁別",
        "手元と周囲の切替",
        "眼と手の協調",
        "空間認識",
        "注意切替",
    ],
    "ライン作業・検品": [
        "視覚弁別",
        "視覚探索",
        "固視",
        "注意維持",
        "処理速度",
        "パターン認識",
    ],
    "子どもとの遊び": [
        "動くものを追う",
        "周辺視野",
        "視線切替",
        "眼と手・足の協調",
        "頭部と眼の協調",
        "安全確認",
    ],
}


# -----------------------------
# 活動カテゴリごとのメニュー例
# -----------------------------
ACTIVITY_MENU = {
    "スポーツ": {
        "main": "Turbo",
        "sub": "Hoopie / Flash Match",
        "bridge": "正面を見た状態から左右へ視線を切り替える。必要に応じて頭部回旋も加える。",
    },
    "読書・学習": {
        "main": "Flash Match",
        "sub": "低負荷のTurbo",
        "bridge": "短文を1行ずつ読み、行飛ばしや戻りを確認する。",
    },
    "PC・デジタル作業": {
        "main": "Flash Match",
        "sub": "Pepper Picker / 低負荷Turbo",
        "bridge": "画面内の複数箇所を順番に確認し、手元や資料へ視線を戻す。",
    },
    "家事・日常生活": {
        "main": "Pepper Picker",
        "sub": "Turbo",
        "bridge": "机上の物を順番に探す。手元と周囲をゆっくり切り替える。",
    },
    "ライン作業・検品": {
        "main": "Flash Match",
        "sub": "Turbo",
        "bridge": "似た形や色の中から違いを探す。短時間で区切る。",
    },
    "子どもとの遊び": {
        "main": "Hoopie",
        "sub": "Turbo / Pepper Picker",
        "bridge": "ボールや動く対象を追いながら、周囲の安全確認を行う。",
    },
}


# -----------------------------
# コンディションからモードを判定
# -----------------------------
def judge_mode(
    fatigue,
    focus,
    sleep_hours,
    eye_strain,
    headache,
    dizziness,
    diplopia,
    mood,
):
    red_flags = []
    yellow_flags = []

    # 強い中止・回復寄りの条件
    if dizziness >= 7:
        red_flags.append("めまい・VR酔い不安が強い")
    if headache >= 7:
        red_flags.append("頭痛が強い")
    if diplopia == "増えている":
        red_flags.append("複視が増えている")
    if fatigue >= 8:
        red_flags.append("疲労度が高い")
    if eye_strain >= 8:
        red_flags.append("眼精疲労が強い")
    if sleep_hours < 4:
        red_flags.append("睡眠不足が強い")

    # Easy寄りの条件
    if 5 <= fatigue <= 7:
        yellow_flags.append("疲労が中等度")
    if focus <= 4:
        yellow_flags.append("集中力が低い")
    if 4 <= sleep_hours < 6:
        yellow_flags.append("睡眠がやや不足")
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

    if fatigue <= 3 and focus >= 8 and eye_strain <= 3 and sleep_hours >= 7 and mood == "よい":
        return "Hard", red_flags, yellow_flags

    return "Normal", red_flags, yellow_flags


def get_mode_setting(mode):
    if mode == "Recovery":
        return {
            "time": "0〜5分",
            "target_size": "大きめ",
            "speed": "遅め",
            "spread": "狭め",
            "goal": "鍛えるより、休む・記録する・軽く慣らす",
            "avoid": "速い反応課題、広い視野移動、強い立体視、長時間連続",
        }

    if mode == "Easy":
        return {
            "time": "5〜8分",
            "target_size": "大きめ",
            "speed": "やや遅め",
            "spread": "狭め〜中等度",
            "goal": "無理なく完了する。継続と達成感を優先する",
            "avoid": "高スピード、難易度急上昇、長時間連続",
        }

    if mode == "Hard":
        return {
            "time": "10〜15分",
            "target_size": "やや小さめ",
            "speed": "やや速め",
            "spread": "中等度〜広め",
            "goal": "反応、探索、視線切替に負荷をかける",
            "avoid": "症状が出ても継続すること",
        }

    return {
        "time": "8〜12分",
        "target_size": "標準",
        "speed": "標準",
        "spread": "中等度",
        "goal": "目的に応じた標準メニューを行う",
        "avoid": "疲労や眼精疲労が出た状態での延長",
    }


# -----------------------------
# 入力フォーム
# -----------------------------
st.markdown("### 1. 活動カテゴリ")

activity = st.selectbox(
    "目的に近い活動を選択してください",
    list(ACTIVITY_SKILLS.keys())
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
st.markdown("### 2. 今日のコンディション")

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


# -----------------------------
# 判定ボタン
# -----------------------------
if st.button("DVTメニュー候補を提案する"):

    mode, red_flags, yellow_flags = judge_mode(
        fatigue=fatigue,
        focus=focus,
        sleep_hours=sleep_hours,
        eye_strain=eye_strain,
        headache=headache,
        dizziness=dizziness,
        diplopia=diplopia,
        mood=mood,
    )

    mode_setting = get_mode_setting(mode)
    skills = ACTIVITY_SKILLS[activity]
    menu = ACTIVITY_MENU[activity]

    st.markdown("### 提案結果")

    if mode == "Recovery":
        st.error("本日の判定: Recovery")
        st.write("今日はDVTを強く進めず、休む・記録する・ごく短時間にする判断が適しています。")
    elif mode == "Easy":
        st.warning("本日の判定: Easy")
        st.write("今日は低負荷・短時間で、継続を優先するメニューが適しています。")
    elif mode == "Hard":
        st.success("本日の判定: Hard")
        st.write("大きな不調がなければ、少し負荷を上げたメニューも検討できます。")
    else:
        st.info("本日の判定: Normal")
        st.write("標準的な負荷で、目的に沿ったDVTメニューを行います。")

    st.markdown("#### 活動から分解した目の使い方")
    for skill in skills:
        st.write(f"- {skill}")

    st.markdown("#### 推奨メニュー候補")
    st.write(f"- メイン候補: {menu['main']}")
    st.write(f"- サブ候補: {menu['sub']}")

    st.markdown("#### 本日の設定目安")
    st.write(f"- プレイ時間: {mode_setting['time']}")
    st.write(f"- Target Size: {mode_setting['target_size']}")
    st.write(f"- Speed: {mode_setting['speed']}")
    st.write(f"- Spread: {mode_setting['spread']}")
    st.write(f"- 本日の目的: {mode_setting['goal']}")
    st.write(f"- 避けたい負荷: {mode_setting['avoid']}")

    st.markdown("#### Bridge task")
    st.write(menu["bridge"])

    st.markdown("#### 判定に影響した条件")

    if red_flags:
        st.write("Recovery寄りの条件:")
        for flag in red_flags:
            st.write(f"- {flag}")

    if yellow_flags:
        st.write("Easy寄りの条件:")
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
        "この提案はデモ用です。実際の運用では、医療者・開発者・DVT担当者による確認が必要です。"
    )
