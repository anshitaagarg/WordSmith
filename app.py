import streamlit as st

from translator import translate_text
from languages import LANGUAGES
from history_manager import save_translation, load_history

st.set_page_config(
    page_title="WordSmith",
    page_icon="🌍",
    layout="wide"
)

st.markdown("""
<style>

.main {
    padding-top: 1rem;
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

st.title("🌍 WordSmith")
st.subheader("AI-Powered Language Translator")

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
    height=200
)

word_count = len(input_text.split())
char_count = len(input_text)

col1, col2 = st.columns(2)

with col1:
    st.metric("Words", word_count)

with col2:
    st.metric("Characters", char_count)

if st.button("Translate"):
    
    if input_text.strip():

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
            height=200
        )

        st.download_button(
            label="📥 Download Translation",
            data=translated_text,
            file_name="translation.txt",
            mime="text/plain"
        )

    #else:
    #    st.warning("Please enter some text.")

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