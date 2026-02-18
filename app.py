import streamlit as st
import google.generativeai as genai

# --- 1. 接続診断ログ（画面には出さず、エラー時のみ詳細表示） ---
def safe_generate_content(prompt):
    try:
        if "GEMINI_API_KEY" not in st.secrets:
            return "ERROR:KEY_MISSING", "SecretsにAPIキーが見つかりません。"
        
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # あなたのリストにあった「gemini-2.0-flash」を試行
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return "SUCCESS", response.text
    
    except Exception as e:
        # ここで「真の原因」をキャッチして報告する
        return "ERROR:API_FAIL", str(e)

# --- 2. Step 3 の実行ロジック ---
if st.session_state.step == 3:
    st.header("Step 3: 最終確認")
    # (確認表示は省略)
    
    if st.button("✨ 制作プランを確定する"):
        with st.spinner("AIによる分析を実行中..."):
            status, result = safe_generate_content(f"絵本の構成案：{st.session_state.char_data}")
            
            if status == "SUCCESS":
                st.session_state.preview_data = result
            else:
                # 失敗しても、原因を警告として出しつつ、ダミーで「進める」
                st.error(f"API接続に失敗しました。原因: {result}")
                st.warning("開発を継続するため、一時的にデモ用データを作成します。")
                st.session_state.preview_data = f"（デモ用）\n主人公：{st.session_state.char_data}の物語\n1. 森での出会い..."
            
            st.session_state.step = 3.5
            st.rerun()
    if st.button("やり直す"): 
        st.session_state.step = 3
        st.rerun()
