import base64
import html
import json
import logging
import mimetypes
import time
from pathlib import Path

import streamlit as st
from google.genai import errors

from rag.retriever import (
    build_index,
    get_error_code,
    load_rules,
    retrieve,
)
from ui.styles import apply_styles


logging.basicConfig(
    level=logging.ERROR
)

logger = logging.getLogger(__name__)


st.set_page_config(
    page_title="Ask My Portfolio",
    page_icon="🤖",
    layout="wide",
)

apply_styles()

st.markdown(
    '<div id="top"></div>',
    unsafe_allow_html=True,
)


PROJECTS_FILE = Path(
    "data/projects.json"
)

GEMINI_MODEL = "gemini-3.6-flash"


@st.cache_data(show_spinner=False)
def image_to_data_uri(image_path):
    path = Path(image_path)

    if not path.exists():
        return None

    mime_type, _ = mimetypes.guess_type(path.name)

    if mime_type is None:
        mime_type = "image/jpeg"

    encoded = base64.b64encode(
        path.read_bytes()
    ).decode("utf-8")

    return f"data:{mime_type};base64,{encoded}"


with PROJECTS_FILE.open(
    "r",
    encoding="utf-8",
) as file:
    projects = json.load(file)


if "project_index" not in st.session_state:
    st.session_state.project_index = 0


if "messages" not in st.session_state:
    st.session_state.messages = []


def previous_projects():
    st.session_state.project_index = max(
        0,
        st.session_state.project_index - 2,
    )


def next_projects():
    if (
        st.session_state.project_index + 2
        < len(projects)
    ):
        st.session_state.project_index += 2


@st.cache_resource(
    show_spinner=False
)
def get_rag_index():
    return build_index(
        st.secrets["GEMINI_API_KEY"]
    )


@st.cache_resource(
    show_spinner=False
)
def get_assistant_rules():
    return load_rules()


def run_with_retry(
    operation,
    max_attempts=3,
    retry_delay=2,
):
    last_error = None

    for attempt in range(max_attempts):
        try:
            return operation()

        except errors.ServerError as exc:
            last_error = exc
            code = get_error_code(exc)

            if (
                code in {500, 502, 503, 504}
                and attempt < max_attempts - 1
            ):
                time.sleep(retry_delay)
                continue

            raise

        except errors.ClientError as exc:
            last_error = exc
            code = get_error_code(exc)

            if (
                code == 429
                and attempt < max_attempts - 1
            ):
                time.sleep(retry_delay)
                continue

            raise

    if last_error:
        raise last_error


def get_public_error_message(exc):
    if isinstance(exc, errors.ServerError):
        code = get_error_code(exc)

        if code == 503:
            return (
                "The AI service is temporarily unavailable "
                "due to high demand. Please try again shortly."
            )

        return (
            "The AI service is temporarily unavailable. "
            "Please try again shortly."
        )

    if isinstance(exc, errors.ClientError):
        code = get_error_code(exc)

        if code == 429:
            return (
                "The AI service has reached its temporary "
                "usage limit. Please try again shortly."
            )

        if code in {401, 403}:
            return (
                "The portfolio assistant is temporarily "
                "unavailable."
            )

        return (
            "The AI service could not process the request. "
            "Please try again."
        )

    if isinstance(
        exc,
        (
            FileNotFoundError,
            ValueError,
        ),
    ):
        return (
            "The portfolio assistant is temporarily "
            "unavailable."
        )

    return (
        "Something went wrong while processing the request. "
        "Please try again shortly."
    )


st.title(
    "Abdallah Al-Habaibeh"
)

st.markdown(
    """
    <div class="hero-role">
        AI / ML Engineer
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-description">
        Artificial Intelligence & Data Science graduate focused on
        computer vision, NLP, LLM systems, and practical AI applications.
        Explore my projects or ask the portfolio assistant about my work,
        technical experience, skills, and background.
    </div>
    """,
    unsafe_allow_html=True,
)


button_columns = st.columns(
    [1.1, 1.1, 1.1, 1.2, 4]
)


with button_columns[0]:
    st.link_button(
        "GitHub",
        "https://github.com/Abdallh-AlHabaibeh",
        use_container_width=True,
    )


with button_columns[1]:
    st.link_button(
        "LinkedIn",
        "https://www.linkedin.com/in/abdallh-alhabaibeh-93a5252b2",
        use_container_width=True,
    )


with button_columns[2]:
    st.link_button(
        "Email",
        "mailto:abdallhsameer449@yahoo.com",
        use_container_width=True,
    )


with button_columns[3]:
    cv_path = Path(
        "assets/Abdallah_Habaibeh_CV.pdf"
    )

    if cv_path.exists():
        with cv_path.open(
            "rb"
        ) as cv_file:
            st.download_button(
                "Download CV",
                data=cv_file,
                file_name=(
                    "Abdallah_Habaibeh_CV.pdf"
                ),
                mime="application/pdf",
                use_container_width=True,
            )

    else:
        st.button(
            "Download CV",
            disabled=True,
            use_container_width=True,
        )


st.divider()


projects_title_col, arrows_col = (
    st.columns(
        [8, 2]
    )
)


with projects_title_col:
    st.markdown(
        '<div class="section-title">'
        'Projects'
        '</div>',
        unsafe_allow_html=True,
    )


with arrows_col:
    left_arrow, right_arrow = (
        st.columns(2)
    )

    with left_arrow:
        st.button(
            "←",
            on_click=previous_projects,
            disabled=(
                st.session_state.project_index == 0
            ),
            use_container_width=True,
        )

    with right_arrow:
        st.button(
            "→",
            on_click=next_projects,
            disabled=(
                st.session_state.project_index + 2
                >= len(projects)
            ),
            use_container_width=True,
        )


visible_projects = projects[
    st.session_state.project_index:
    st.session_state.project_index + 2
]


project_columns = st.columns(2)


for column, project in zip(
    project_columns,
    visible_projects,
):
    with column:
        thumbnail = project.get(
            "thumbnail"
        )

        image_uri = (
            image_to_data_uri(thumbnail)
            if thumbnail
            else None
        )

        title = html.escape(
            str(project["title"])
        )

        description = html.escape(
            str(project["description"])
        )

        metric = html.escape(
            str(project.get("metric", ""))
        )

        tech_string = html.escape(
            " • ".join(project["tech"])
        )

        if image_uri:
            background_style = (
                "background-image:"
                "linear-gradient("
                "rgba(2, 6, 23, 0.50),"
                "rgba(2, 6, 23, 0.88)"
                "),"
                f"url('{image_uri}');"
            )
        else:
            background_style = ""

        st.markdown(
            f"""
            <div class="project-card" style="{background_style}">
                <div class="project-card-overlay"></div>
                <div class="project-card-content">
                    <h3>{title}</h3>
                    <div class="project-card-description">
                        {description}
                    </div>
                    <div class="project-card-bottom">
                        <div class="project-card-metric">
                            {metric}
                        </div>
                        <div class="project-card-tech">
                            {tech_string}
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        github_button, demo_button = (
            st.columns(2)
        )

        with github_button:
            st.link_button(
                "GitHub",
                project["github"],
                use_container_width=True,
            )

        with demo_button:
            if project["demo"]:
                st.link_button(
                    "Live Demo",
                    project["demo"],
                    use_container_width=True,
                )

            else:
                st.button(
                    "Live Demo",
                    disabled=True,
                    use_container_width=True,
                    key=(
                        f'demo_{project["title"]}'
                    ),
                )

st.divider()


st.markdown(
    '<div class="section-title">'
    'Ask My Portfolio'
    '</div>',
    unsafe_allow_html=True,
)


st.write(
    """
    Ask questions about my projects, technical experience,
    skills, education, or background.
    """
)


rag_available = True
rag_error_message = None

client = None
rag_chunks = []
rag_embeddings = []
assistant_rules = ""


try:
    client, rag_chunks, rag_embeddings = (
        run_with_retry(
            get_rag_index
        )
    )

    assistant_rules = (
        get_assistant_rules()
    )

except Exception as exc:
    rag_available = False

    rag_error_message = (
        get_public_error_message(
            exc
        )
    )

    logger.exception(
        "Portfolio assistant initialization failed."
    )


if not rag_available:
    st.warning(
        rag_error_message
    )


for message in st.session_state.messages:
    with st.chat_message(
        message["role"]
    ):
        st.markdown(
            message["content"]
        )


question = st.chat_input(
    (
        "Ask about my projects, experience, "
        "skills, or background"
    ),
    disabled=not rag_available,
)


if question and rag_available:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message(
        "user"
    ):
        st.markdown(
            question
        )

    answer = None

    with st.chat_message(
        "assistant"
    ):
        with st.spinner(
            "Thinking..."
        ):
            try:
                retrieved_chunks = (
                    run_with_retry(
                        lambda: retrieve(
                            client,
                            rag_chunks,
                            rag_embeddings,
                            question,
                            top_k=4,
                        )
                    )
                )

                context = "\n\n".join(
                    chunk["text"]
                    for chunk in retrieved_chunks
                )

                prompt = f"""
{assistant_rules}

Portfolio context:

{context}

User question:

{question}
"""

                response = (
                    run_with_retry(
                        lambda: (
                            client.models.generate_content(
                                model=GEMINI_MODEL,
                                contents=prompt,
                            )
                        )
                    )
                )

                if (
                    response is None
                    or not getattr(
                        response,
                        "text",
                        None,
                    )
                    or not response.text.strip()
                ):
                    answer = (
                        "I could not generate a response "
                        "right now. Please try again."
                    )

                else:
                    answer = (
                        response.text.strip()
                    )

            except Exception as exc:
                logger.exception(
                    "Portfolio assistant request failed."
                )

                answer = (
                    get_public_error_message(
                        exc
                    )
                )

            st.markdown(
                answer
            )


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

st.markdown(
    """
    <div class="back-to-top">
        <a href="#top">↑ Back to top</a>
    </div>
    """,
    unsafe_allow_html=True,
)
