import streamlit as st
import google.generativeai as genai

# --- 1. Geminiの設定 ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # 2026年現在、最も汎用的な名称に変更
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("APIキーが設定されていません。")

# --- 2. セッションの初期化 ---
if 'step' not in st.session_state: st.session_state.step = 1
if 'char_data' not in st.session_state: st.session_state.char_data = ""
if 'story_data' not in st.session_state: st.session_state.story_data = ""
if 'preview_data' not in st.session_state: st.session_state.preview_data = None

st.title("📖 AI絵本メーカー")

# --- Step 1 & 2 (省略：前回のコードと同じ) ---
if st.session_state.step == 1:
    st.header("Step 1: キャラクター設定")
    char_input = st.text_area("主人公は？", value=st.session_state.char_data)
    if st.button("次へ"):
        st.session_state.char_data = char_input
        st.session_state.step = 2
        st.rerun()

elif st.session_state.step == 2:
    st.header("Step 2: お話の内容")
    story_input = st.text_area("お話の内容は？", value=st.session_state.story_data)
    if st.button("次へ"):
        st.session_state.story_data = story_input
        st.session_state.step = 3
        st.rerun()

# --- Step 3: 分析実行 ---
elif st.session_state.step == 3:
    st.header("Step 3: 最終確認")
    st.write(f"キャラ: {st.session_state.char_data}")
    st.write(f"ストーリー: {st.session_state.story_data}")
    
    if st.button("✨ AIにプランを作らせる"):
        with st.spinner("AIが分析中..."):
            try:
                prompt = f"絵本のプランを考えて: {st.session_state.char_data}, {st.session_state.story_data}"
                response = model.generate_content(prompt)
                st.session_state.preview_data = response.text
                st.session_state.step = 3.5
                st.rerun()
            except Exception as e:
                st.error(f"AIエラーが発生しました。")
                st.info("【デバッグ情報】あなたのAPIキーで利用可能なモデル一覧:")
                # 使えるモデルをリストアップして表示する
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                st.write(available_models)
                st.warning("上記リストにある名前（models/ を除く）をコードの GenerativeModel('...') に書き換えてみてください。")

# --- Step 3.5: 確認 ---
elif st.session_state.step == 3.5:
    st.header("Step 3.5: AI制作プラン")
    st.write(st.session_state.preview_data)
    if st.button("やり直す"): st.session_state.step = 3; st.rerun()
    st.success("ここから画像生成APIに繋がります（開発中）")
