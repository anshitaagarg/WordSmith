from email.policy import default

import streamlit as st
from speech import text_to_speech
from translator import translate_text, detect_language
from languages import LANGUAGES, LANGUAGE_NAMES
from history_manager import save_translation, load_history

st.set_page_config(
    page_title="WordSmith",
    page_icon="⚒️",
    layout="wide"
)

st.markdown("""
<style>

.block-container {
    padding-top: 0.5rem;
}

h1 {
    text-align: center;
}

[data-testid="stMetric"] {
    border: 1px solid #444;
    padding: 15px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding:10px 0;">
    <h1 style="margin-bottom:0;">
        ⚒️ WordSmith
    </h1>
    <p style="
        font-size:22px;
        color:#A0A0A0;
        margin-top:0;
    ">
        AI-Powered Language Translator
    </p>
</div>
""", unsafe_allow_html=True)

if "source_lang" not in st.session_state:
    st.session_state.source_lang = "Auto Detect"

if "target_lang" not in st.session_state:
    st.session_state.target_lang = "English"
    
col1, col_swap, col2 = st.columns([5, 1.2, 5])

with col1:
    source_language = st.selectbox(
        "Source Language",
        list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index(st.session_state.source_lang)
    )

with col_swap:
    st.write("")
    st.write("")
    if st.button("⇄"):
        temp = st.session_state.source_lang
        st.session_state.source_lang = (
            st.session_state.target_lang
        )
        st.session_state.target_lang = temp
        st.rerun()
        
with col2:
    target_language = st.selectbox(
        "Target Language",
        list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index(st.session_state.target_lang)
    )

st.session_state.source_lang = source_language
st.session_state.target_lang = target_language

input_text = st.text_area(
    "Enter text to translate:",
    height=100,
)

if input_text.strip() and len(input_text.split()) > 3:
    detected_code = detect_language(input_text)
    if detected_code:
        detected_name = LANGUAGE_NAMES.get(
            detected_code.lower(),
            detected_code.upper()
        )
        st.caption(f" **Detected:** {detected_name}")

word_count = len(input_text.split())
char_count = len(input_text)

st.caption(f"Words: {word_count} | Characters: {char_count}")

if st.button("Translate"):

    if input_text.strip():

        with st.spinner("Translating..."):

            translated_text = translate_text(
                input_text,
                LANGUAGES[source_language],
                LANGUAGES[target_language]
            )

        target_code = LANGUAGES[target_language].lower()

        st.session_state["translated_text"] = translated_text
        st.session_state["target_code"] = target_code

        save_translation(
            source_language,
            target_language,
            input_text,
            translated_text
        )

        st.success("Translation Complete!")


# --------------------------
# DISPLAY SAVED TRANSLATION
# --------------------------

if "translated_text" in st.session_state:

    st.markdown("### Translated Text")
    st.code(
        st.session_state["translated_text"],
        language=None
    )
    if st.button("🔊"):

        try:

            audio_file = text_to_speech(
                st.session_state["translated_text"],        
                st.session_state["target_code"]
            )

            st.audio(
                audio_file,
                format="audio/mp3"
            )

        except Exception as e:
            st.warning(
                f"Audio unavailable: {e}"
            )
    
st.divider()
st.subheader("📜 Translation History")

history_df = load_history()

if not history_df.empty:
    st.dataframe(
        history_df.tail(10),
        use_container_width=True
   )

else:
    st.info("No translations yet.")
    
st.markdown("---")

st.caption(
    "⚒️ WordSmith | By anshitaagarg"
)