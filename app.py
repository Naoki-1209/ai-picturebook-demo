import streamlit as st

# --- セッション（記憶）の初期化 ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'char_data' not in st.session_state:
    st.session_state.char_data = None
if 'story_data' not in st.session_state:
    st.session_state.story_data = None

st.title("📖 AI絵本メーカー (Demo Ver.)")

# --- ステップ1: キャラクター (A) ---
if st.session_state.step == 1:
    st.header("Step 1: キャラクターの設定 (A)")
    char_input = st.text_area("どんな主人公がいいですか？（例：青い帽子の白い猫）")
    if st.button("キャラクターを決定"):
        st.session_state.char_data = char_input
        st.session_state.step = 2
        st.rerun()

# --- ステップ2: お話 (B) ---
elif st.session_state.step == 2:
    st.header("Step 2: お話の内容 (B)")
    story_input = st.text_area("お話のあらすじや、全8ページの内容を書いてください。")
    if st.button("お話を決定"):
        st.session_state.story_data = story_input
        st.session_state.step = 3
        st.rerun()

# --- ステップ3: 構成確認 ---
elif st.session_state.step == 3:
    st.header("Step 3: 最終確認")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("キャラクター設定")
        st.write(st.session_state.char_data)
        if st.button("キャラを修正"): st.session_state.step = 1; st.rerun()
    with col2:
        st.subheader("ストーリー内容")
        st.write(st.session_state.story_data)
        if st.button("お話を修正"): st.session_state.step = 2; st.rerun()
    
    if st.button("🚀 生成を開始する"):
        st.balloons()
        st.success("（デモ版：ここでAIが絵本を生成します）")
