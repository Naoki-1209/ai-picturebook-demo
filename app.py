import streamlit as st
import google.generativeai as genai

# --- 1. Geminiの設定 ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # あなたのリストにあった「gemini-2.0-flash」を確実に指定します
    model = genai.GenerativeModel('gemini-2.0-flash')
else:
    st.error("APIキーが設定されていません。")

# --- 2. セッションの初期化 ---
if 'step' not in st.session_state: st.session_state.step = 1
if 'char_data' not in st.session_state: st.session_state.char_data = ""
if 'story_data' not in st.session_state: st.session_state.story_data = ""
if 'preview_data' not in st.session_state: st.session_state.preview_data = None

st.title("📖 AI絵本メーカー")

# ステップ1
if st.session_state.step == 1:
    st.header("Step 1: キャラクター設定")
    char_input = st.text_area("主人公は？", value=st.session_state.char_data)
    if st.button("次へ"):
        st.session_state.char_data = char_input
        st.session_state.step = 2
        st.rerun()

# ステップ2
elif st.session_state.step == 2:
    st.header("Step 2: お話の内容")
    story_input = st.text_area("お話の内容は？", value=st.session_state.story_data)
    if st.button("次へ"):
        st.session_state.story_data = story_input
        st.session_state.step = 3
        st.rerun()

# ステップ3: ここでAIが動きます
elif st.session_state.step == 3:
    st.header("Step 3: 最終確認")
    st.write(f"キャラ: {st.session_state.char_data}")
    st.write(f"ストーリー: {st.session_state.story_data}")
    
    if st.button("✨ AIにプランを作らせる"):
        with st.spinner("AIが分析中..."):
            try:
                # 明確な命令（プロンプト）を送る
                prompt = f"以下の設定で8ページの絵本の構成案と、画像生成用の英語プロンプトを日本語で作成してください。\nキャラ：{st.session_state.char_data}\n話：{st.session_state.story_data}"
                response = model.generate_content(prompt)
                st.session_state.preview_data = response.text
                st.session_state.step = 3.5
                st.rerun()
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")

# ステップ3.5: AI制作プランの確認
elif st.session_state.step == 3.5:
    st.header("Step 3.5: AI制作プラン")
    st.write(st.session_state.preview_data)
    if st.button("やり直す"): 
        st.session_state.step = 3
        st.rerun()
