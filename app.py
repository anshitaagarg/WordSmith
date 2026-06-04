import streamlit as st

from translator import translate_text, detect_language
from languages import LANGUAGES, LANGUAGE_NAMES
from history_manager import save_translation, load_history

st.set_page_config(
    page_title="WordSmith",
    page_icon="🌍",
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
        🌍 WordSmith
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

col1, col2 = st.columns(2)

with col1:
    source_language = st.selectbox(
        "Source Language",
        list(LANGUAGES.keys())
    )

with col2:
    target_language = st.selectbox(
        "Target Language",
        list(LANGUAGES.keys()),
        index=1
    )

input_text = st.text_area(
    "Enter text to translate:",
    height=100
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

col1, col2 = st.columns(2)

with col1:
    st.metric("Words", word_count)

with col2:
    st.metric("Characters", char_count)

if st.button("Translate"):
    
    if input_text.strip():
        detected_code = detect_language(input_text)
        if detected_code:
            detected_name = LANGUAGE_NAMES.get(
                detected_code.lower(),
                detected_code.upper()
            )

        with st.spinner("Translating..."):
            translated_text = translate_text(
                input_text,
                LANGUAGES[source_language],
                LANGUAGES[target_language]
            )
        
        st.success("Translation Complete!")
        save_translation(
            source_language,
            target_language,
            input_text,
            translated_text
        )
        
        st.text_area(
            "Translated Text",
            translated_text,
            height=100
        )

        st.download_button(
            label="📥 Download Translation",
            data=translated_text,
            file_name="translation.txt",
            mime="text/plain"
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