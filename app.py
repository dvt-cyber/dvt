import streamlit as st

st.set_page_config(page_title="DVT AI Protocol Generator", layout="centered")

st.title("🧠 DVT Vision Training")
st.subheader("AI プロトコル自動生成システム (デモ版)")
st.write("選手や患者のコンディションを入力すると、AIが最適なVRトレーニングメニューを提案します。")

st.markdown("---")

# 1. コンディション入力エリア
st.markdown("### 📋 1. 本日のコンディションを入力")
sport = st.selectbox("対象の競技・カテゴリ", ["サッカー (GK)", "野球 (バッター)", "テニス", "リハビリ (脳震盪後)", "リハビリ (PD)"])
sleep_hours = st.slider("前日の睡眠時間", min_value=0.0, max_value=12.0, value=6.0, step=0.5)
focus_score = st.slider("本日の集中力スコア (1:低い 〜 10:高い)", min_value=1, max_value=10, value=5)
mood = st.selectbox("本日の気分", ["普通", "イライラ・ストレス", "疲労感が強い", "モチベーションが高い"])

st.markdown("---")

# 2. AI判定ボタン
if st.button("🤖 AIにプロトコルを提案させる"):
    
    st.markdown("### ✨ AIからの提案プロトコル")
    
    # デモ用の簡単な条件分岐（睡眠不足または集中力低下の場合）
    if sleep_hours < 5.0 or focus_score <= 4 or mood == "疲労感が強い":
        st.warning("⚠️ **AIコンディション分析:** 睡眠不足または脳の疲労が検出されました。本日は眼球運動の負荷を下げ、認知リカバリーを優先する安全なメニューを提案します。")
        
        st.write("#### 🎮 Vivid Vision 設定値 (リカバリーモード)")
        st.write("- **推奨ゲーム:** Pepper Picker")
        st.write("- **プレイ時間:** 5分 (通常より短縮)")
        st.write("- **Target Size:** LARGE")
        st.write("- **Spread:** NARROW (首の動きを最小限に)")
        st.write("- **AIからのアドバイス:** 視界が広く動くゲームは避け、シンプルなシングルタスクに集中させてください。")
        
    # コンディションが良好な場合
    else:
        st.success("✅ **AIコンディション分析:** 心身ともに良好な状態です。本日は脳の情報処理（Deep Vision）に負荷をかける実践的なメニューを提案します。")
        
        st.write("#### 🎮 Vivid Vision 設定値 (パフォーマンスアップモード)")
        st.write("- **推奨ゲーム:** Flash Match + Bubbles")
        st.write("- **プレイ時間:** 12分")
        st.write("- **Target Size:** SMALL")
        st.write("- **Spread:** WIDE (周辺視野をフル活用)")
        st.write("- **AIからのアドバイス:** ターゲットの表示時間を短く設定し、瞬間的な判断とノイズ（ダミー）の処理能力を鍛えます。")
