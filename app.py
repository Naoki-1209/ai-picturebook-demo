import streamlit as st
import google.generativeai as genai

# --- 1. セッション（記憶）の初期化 ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'char_data' not in st.session_state:
    st.session_state.char_data = ""
if 'story_data' not in st.session_state:
    st.session_state.story_data = ""
if 'preview_data' not in st.session_state:
    st.session_state.preview_data = None

# --- 2. 診断機能付き：AI呼び出し関数 ---
def safe_generate_content(prompt):
    try:
        if "GEMINI_API_KEY" not in st.secrets:
            return "ERROR:KEY_MISSING", "Secretsにキーが設定されていません。"
        
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return "SUCCESS", response.text
    except Exception as e:
        return "ERROR:API_FAIL", str(e)

st.title("📖 AI絵本メーカー (診断・回避機能付)")

# --- Step 1: キャラクター設定 ---
if st.session_state.step == 1:
    st.header("Step 1: キャラクター設定")
    char_input = st.text_area("主人公はどんな人？", value=st.session_state.char_data)
    if st.button("次へ"):
        st.session_state.char_data = char_input
        st.session_state.step = 2
        st.rerun()

# --- Step 2: お話の内容 ---
elif st.session_state.step == 2:
    st.header("Step 2: お話の内容")
    story_input = st.text_area("どんなお話？", value=st.session_state.story_data)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("戻る"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("次へ"):
            st.session_state.story_data = story_input
            st.session_state.step = 3
            st.rerun()

# --- Step 3: 最終確認と診断実行 ---
elif st.session_state.step == 3:
    st.header("Step 3: 最終確認")
    st.info(f"キャラ: {st.session_state.char_data}\n\nストーリー: {st.session_state.story_data}")
    
    if st.button("✨ 制作プランを確定する"):
        with st.spinner("AIによる分析を実行中..."):
            status, result = safe_generate_content(
                f"絵本作家として構成案を作って。キャラ：{st.session_state.char_data}、話：{st.session_state.story_data}"
            )
            
            if status == "SUCCESS":
                st.session_state.preview_data = result
            else:
                st.error(f"【APIエラー】原因: {result}")
                st.warning("現在、APIが制限されています。画面確認のためダミー案を表示します。")
                st.session_state.preview_data = f"（デモ用）\n主人公：{st.session_state.char_data}の物語\n1. 森での出会い..."
            
            st.session_state.step = 3.5
            st.rerun()

# --- Step 3.5: AI制作プランの確認（強化版） ---
elif st.session_state.step == 3.5:
    st.header("🎨 絵本の構成案を確認")
    
    # AIの回答を「行」で分割
    # 本物のAIなら P1: ... P2: ... と返ってくるのを想定
    lines = [line for line in st.session_state.preview_data.split('\n') if line.strip()]
    
    cols = st.columns(2)
    for i in range(8):
        with cols[i % 2]:
            with st.container(border=True):
                st.subheader(f"Page {i+1}")
                
                # --- ここが重要：AIの回答から該当ページを抽出するロジック ---
                if len(lines) > i:
                    content = lines[i]
                else:
                    # AIの回答が足りない場合のダミー（ここをページごとに変える）
                    content = f"{st.session_state.char_data}が活躍する、第{i+1}のシーン"
                
                st.write(f"【挿絵案】: {content}")
                st.caption(f"📷 生成プロンプト: A scene of {st.session_state.char_data}, page {i+1}, watercolor style")

    st.divider()
    # (ボタン類はそのまま)

# --- Step 4: 完成 ---
elif st.session_state.step == 4:
    st.header("Step 4: 生成プロセス")
    st.success("（ここで画像生成への接続を待ちます）")
    if st.button("最初に戻る"):
        st.session_state.step = 1
        st.rerun()
