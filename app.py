import streamlit as st

# --- セッション（記憶）の初期化 ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'char_data' not in st.session_state:
    st.session_state.char_data = "" # 初期値を空文字に
if 'story_data' not in st.session_state:
    st.session_state.story_data = "" # 初期値を空文字に

st.title("📖 AI絵本メーカー (Demo Ver.)")

# --- ステップ1: キャラクター (A) ---
if st.session_state.step == 1:
    st.header("Step 1: キャラクターの設定 (A)")
    # valueに保存済みのデータを指定することで、戻ったときに前回の入力が残る
    char_input = st.text_area("どんな主人公がいいですか？", value=st.session_state.char_data)
    if st.button("次へ（ストーリー設定へ）"):
        st.session_state.char_data = char_input
        st.session_state.step = 2
        st.rerun()

# --- ステップ2: お話 (B) ---
elif st.session_state.step == 2:
    st.header("Step 2: お話の内容 (B)")
    # ここも同様に、前回の入力を表示させる
    story_input = st.text_area("お話のあらすじを書いてください。", value=st.session_state.story_data)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("戻る（キャラ設定へ）"):
            st.session_state.story_data = story_input # 入力中の中身を保存して戻る
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("次へ（最終確認へ）"):
            st.session_state.story_data = story_input
            st.session_state.step = 3
            st.rerun()

# --- ステップ3: 構成確認 ---
elif st.session_state.step == 3:
    st.header("Step 3: 最終確認")
    
    st.subheader("現在の設定")
    c1, c2 = st.columns(2)
    with c1:
        st.info(f"**【キャラクター】**\n\n{st.session_state.char_data}")
        if st.button("A：キャラだけ修正する"):
            st.session_state.step = 1
            st.rerun()
    with c2:
        st.info(f"**【ストーリー】**\n\n{st.session_state.story_data}")
        if st.button("B：お話だけ修正する"):
            st.session_state.step = 2
            st.rerun()
    
    st.divider()
    if st.button("🚀 この内容で絵本を生成する"):
        st.balloons()
        st.success("（おめでとうございます！ここからAIが動き出します）")
