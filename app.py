# --- セッション（記憶）の初期化 ---
if 'step' not in st.session_state:
    st.session_state.step = 1
# プレビュー用のデータを保存する場所
if 'preview_data' not in st.session_state:
    st.session_state.preview_data = None

# ... (Step 1, 2, 3 のコード) ...

# --- ステップ3: 構成確認 ---
elif st.session_state.step == 3:
    st.header("Step 3: 入力内容の最終確認")
    # (中略：これまでの確認画面)
    
    if st.button("AIに下書き（プレビュー）を作らせる"):
        # ここで本来はGemini APIを叩き、プレビュー用データを生成する
        st.session_state.preview_data = {
            "char_prompt": f"【AIの解釈】: {st.session_state.char_data} を反映した、水彩画風の可愛らしいキャラクター",
            "storyboard": [f"P{i+1}: {st.session_state.story_data[:10]}...のシーンの挿絵案" for i in range(8)]
        }
        st.session_state.step = 3.5
        st.rerun()

# --- ステップ3.5: プレビュー確認 (New!) ---
elif st.session_state.step == 3.5:
    st.header("Step 3.5: AIによる制作プランの確認")
    st.info("AIがあなたの指示を元に、このようなイメージで描き出そうとしています。")

    st.subheader("🖼 キャラクターのビジュアル案")
    st.write(st.session_state.preview_data["char_prompt"])
    
    st.subheader("📚 各ページの絵コンテ案")
    for scene in st.session_state.preview_data["storyboard"]:
        st.write(f"・{scene}")

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Step 3に戻って修正する"):
            st.session_state.step = 3
            st.rerun()
    with col2:
        if st.button("このプランで本番生成を開始！"):
            st.session_state.step = 4
            st.rerun()

# --- ステップ4: 生成実行 ---
elif st.session_state.step == 4:
    st.header("Step 4: 最終生成プロセス")
    st.progress(100)
    st.success("（デモ版：ここでAPIを叩き、実際に画像を8枚生成します）")
