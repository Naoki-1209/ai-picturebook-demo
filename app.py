import streamlit as st

# --- 1. セッション（記憶）の初期化 ---
# ここでアプリの「現在の状態」を保存します
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'char_data' not in st.session_state:
    st.session_state.char_data = ""
if 'story_data' not in st.session_state:
    st.session_state.story_data = ""
if 'preview_data' not in st.session_state:
    st.session_state.preview_data = None

st.title("📖 AI絵本メーカー (Demo Ver.)")

# --- 2. 各ステップの画面描画 ---

# ステップ1: キャラクターの設定 (A)
if st.session_state.step == 1:
    st.header("Step 1: キャラクターの設定 (A)")
    char_input = st.text_area("どんな主人公がいいですか？", value=st.session_state.char_data)
    if st.button("次へ（ストーリー設定へ）"):
        st.session_state.char_data = char_input
        st.session_state.step = 2
        st.rerun()

# ステップ2: お話の内容 (B)
elif st.session_state.step == 2:
    st.header("Step 2: お話の内容 (B)")
    story_input = st.text_area("全8ページのお話の内容を書いてください。", value=st.session_state.story_data)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("戻る（キャラ設定へ）"):
            st.session_state.story_data = story_input
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("次へ（最終確認へ）"):
            st.session_state.story_data = story_input
            st.session_state.step = 3
            st.rerun()

# ステップ3: 入力内容の最終確認
elif st.session_state.step == 3:
    st.header("Step 3: 最終確認")
    c1, c2 = st.columns(2)
    with c1:
        st.info(f"**【キャラクター】**\n\n{st.session_state.char_data}")
        if st.button("A：キャラを修正"):
            st.session_state.step = 1
            st.rerun()
    with c2:
        st.info(f"**【ストーリー】**\n\n{st.session_state.story_data}")
        if st.button("B：お話を修正"):
            st.session_state.step = 2
            st.rerun()
    
    st.divider()
    if st.button("AIに制作プラン（プレビュー）を作らせる"):
        # デモ用の仮データ作成（本来はここでGemini APIを叩く）
        st.session_state.preview_data = {
            "char_prompt": f"【AI解釈】: {st.session_state.char_data} の特徴を持つ絵本キャラクター",
            "storyboard": [f"P{i+1}: {st.session_state.story_data[:10]}...のシーンを描画" for i in range(8)]
        }
        st.session_state.step = 3.5
        st.rerun()

# ステップ3.5: AI制作プランの確認 (New!)
elif st.session_state.step == 3.5:
    st.header("Step 3.5: AI制作プランの確認")
    st.warning("AIが以下のプランで描き出そうとしています。修正が必要なら戻ってください。")

    st.subheader("🖼 キャラクター描画プラン")
    st.write(st.session_state.preview_data["char_prompt"])
    
    st.subheader("📚 各ページの挿絵イメージ")
    for scene in st.session_state.preview_data["storyboard"]:
        st.write(f"・{scene}")

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Step 3に戻って練り直す"):
            st.session_state.step = 3
            st.rerun()
    with col2:
        if st.button("このプランで本番生成を開始！"):
            st.session_state.step = 4
            st.rerun()

# ステップ4: 最終生成
elif st.session_state.step == 4:
    st.header("Step 4: 絵本完成！")
    st.balloons()
    st.success("おめでとうございます！絵本が生成されました（※現在はデモ表示です）")
    if st.button("最初から作り直す"):
        st.session_state.step = 1
        st.rerun()
