import streamlit as st
import google.generativeai as genai

# --- 1. Geminiの設定 ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-pro')
else:
    st.error("APIキーが設定されていません。StreamlitのSettings > Secretsを確認してください。")

# --- 2. セッション（記憶）の初期化 ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'char_data' not in st.session_state:
    st.session_state.char_data = ""
if 'story_data' not in st.session_state:
    st.session_state.story_data = ""
if 'preview_data' not in st.session_state:
    st.session_state.preview_data = None

st.title("📖 AI絵本メーカー (AI搭載版)")

# ステップ1: キャラクター (A)
if st.session_state.step == 1:
    st.header("Step 1: キャラクターの設定 (A)")
    char_input = st.text_area("どんな主人公がいいですか？", value=st.session_state.char_data)
    if st.button("次へ"):
        st.session_state.char_data = char_input
        st.session_state.step = 2
        st.rerun()

# ステップ2: お話 (B)
elif st.session_state.step == 2:
    st.header("Step 2: お話の内容 (B)")
    story_input = st.text_area("お話の内容を書いてください。", value=st.session_state.story_data)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("戻る"):
            st.session_state.story_data = story_input
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("次へ"):
            st.session_state.story_data = story_input
            st.session_state.step = 3
            st.rerun()

# ステップ3: 最終確認
elif st.session_state.step == 3:
    st.header("Step 3: 最終確認")
    c1, c2 = st.columns(2)
    with c1:
        st.info(f"**【キャラクター】**\n\n{st.session_state.char_data}")
        if st.button("Aを修正"): st.session_state.step = 1; st.rerun()
    with c2:
        st.info(f"**【ストーリー】**\n\n{st.session_state.story_data}")
        if st.button("Bを修正"): st.session_state.step = 2; st.rerun()
    
    st.divider()
    if st.button("✨ AIに制作プランを作らせる"):
        with st.spinner("AIが物語を分析中..."):
            prompt = f"""
            プロの絵本作家として、以下の設定から8ページの制作プランを作ってください。
            
            【キャラ】: {st.session_state.char_data}
            【物語】: {st.session_state.story_data}
            
            1. char_prompt: 主人公の英語の画像生成用プロンプト（100語程度）
            2. storyboard: P1からP8までの挿絵の構図案（日本語）
            を詳しく出力してください。
            """
            try:
                response = model.generate_content(prompt)
                st.session_state.preview_data = response.text
                st.session_state.step = 3.5
                st.rerun()
            except Exception as e:
                st.error(f"AIエラー: {e}")

# ステップ3.5: プレビュー確認
elif st.session_state.step == 3.5:
    st.header("Step 3.5: AI制作プランの確認")
    st.write(st.session_state.preview_data)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("やり直す"): st.session_state.step = 3; st.rerun()
    with col2:
        if st.button("これで本番生成！"): st.session_state.step = 4; st.rerun()

# ステップ4: 完成
elif st.session_state.step == 4:
    st.header("Step 4: 生成開始")
    st.balloons()
    st.success("ここから画像生成APIに繋がります（開発中）")
