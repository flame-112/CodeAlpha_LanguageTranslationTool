"""Language Translation Tool."""

import html
import io
from typing import Optional

import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS

LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Japanese": "ja",
    "Korean": "ko",
    "Arabic": "ar",
    "Chinese (Simplified)": "zh-CN",
    "Portuguese": "pt",
    "Russian": "ru",
    "Italian": "it",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te",
    "Marathi": "mr",
    "Urdu": "ur",
}

PAGE_STYLE = """
<style>
    .block-container { padding-top: 2rem; max-width: 820px; }
    .hero {
        background: linear-gradient(135deg, #0f766e 0%, #0891b2 55%, #2563eb 100%);
        color: white;
        padding: 1.75rem 1.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px rgba(15, 118, 110, 0.18);
    }
    .hero h1 { margin: 0; font-size: 1.9rem; font-weight: 700; }
    .hero p { margin: 0.45rem 0 0; opacity: 0.92; font-size: 1rem; }
    div[data-testid="stTextArea"] textarea {
        border-radius: 12px;
        border: 1px solid #dbeafe;
        font-size: 1rem;
    }
    div[data-testid="stSelectbox"] > div > div {
        border-radius: 10px;
    }
    .result-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #0891b2;
        border-radius: 12px;
        padding: 1.1rem 1.2rem;
        font-size: 1.08rem;
        line-height: 1.6;
        color: #0f172a;
        min-height: 80px;
    }
    .meta-chip {
        display: inline-block;
        background: #ecfeff;
        color: #155e75;
        padding: 0.25rem 0.65rem;
        border-radius: 999px;
        font-size: 0.82rem;
        margin-top: 0.75rem;
    }
</style>
"""


def translate_text(text: str, source: str, target: str) -> str:
    translator = GoogleTranslator(source=source, target=target)
    return translator.translate(text)


def text_to_speech_bytes(text: str, lang_code: str) -> Optional[bytes]:
    if not text.strip():
        return None
    tts = gTTS(text=text, lang=lang_code)
    buffer = io.BytesIO()
    tts.write_to_fp(buffer)
    buffer.seek(0)
    return buffer.read()


def swap_languages() -> None:
    source = st.session_state.get("source_label", "English")
    target = st.session_state.get("target_label", "Hindi")
    st.session_state["source_label"] = target
    st.session_state["target_label"] = source


def main() -> None:
    st.set_page_config(
        page_title="Translate",
        page_icon="🌐",
        layout="centered",
    )
    st.markdown(PAGE_STYLE, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="hero">
            <h1>Language Translator</h1>
            <p>Convert text between languages instantly, with optional speech playback.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "source_label" not in st.session_state:
        st.session_state["source_label"] = "English"
    if "target_label" not in st.session_state:
        st.session_state["target_label"] = "Hindi"

    lang_col1, swap_col, lang_col2 = st.columns([5, 1, 5])
    with lang_col1:
        st.selectbox(
            "From",
            list(LANGUAGES.keys()),
            key="source_label",
        )
    with swap_col:
        st.markdown("<div style='height: 1.6rem;'></div>", unsafe_allow_html=True)
        if st.button("⇄", help="Swap languages", use_container_width=True):
            swap_languages()
            st.rerun()
    with lang_col2:
        target_options = [label for label in LANGUAGES if label != st.session_state["source_label"]]
        if st.session_state["target_label"] not in target_options:
            st.session_state["target_label"] = target_options[0]
        st.selectbox(
            "To",
            target_options,
            key="target_label",
        )

    source_code = LANGUAGES[st.session_state["source_label"]]
    target_code = LANGUAGES[st.session_state["target_label"]]

    input_text = st.text_area(
        "Your text",
        height=170,
        placeholder="Write or paste the text you want to translate...",
        label_visibility="collapsed",
    )

    char_count = len(input_text)
    st.caption(f"{char_count} characters")

    translate_clicked = st.button("Translate", type="primary", use_container_width=True)

    if translate_clicked:
        if not input_text.strip():
            st.warning("Enter some text before translating.")
        else:
            with st.spinner("Translating..."):
                try:
                    translated = translate_text(input_text, source_code, target_code)
                    st.session_state["translated_text"] = translated
                    st.session_state.pop("audio_bytes", None)
                except Exception as exc:
                    st.error(f"Translation failed: {exc}")

    translated_text = st.session_state.get("translated_text", "")

    if translated_text:
        st.markdown("**Result**")
        st.markdown(f'<div class="result-box">{html.escape(translated_text)}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<span class="meta-chip">{st.session_state["source_label"]} → '
            f'{st.session_state["target_label"]}</span>',
            unsafe_allow_html=True,
        )

        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            st.download_button(
                label="Save as text file",
                data=translated_text,
                file_name="translation.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with btn_col2:
            if st.button("Listen to translation", use_container_width=True):
                with st.spinner("Generating audio..."):
                    try:
                        audio_bytes = text_to_speech_bytes(translated_text, target_code)
                        if audio_bytes:
                            st.session_state["audio_bytes"] = audio_bytes
                    except Exception as exc:
                        st.error(f"Speech generation failed: {exc}")

        if "audio_bytes" in st.session_state:
            st.audio(st.session_state["audio_bytes"], format="audio/mp3")


if __name__ == "__main__":
    main()
