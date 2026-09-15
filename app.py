import json
from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="Ask My Portfolio",
    page_icon="🤖",
    layout="wide",
)


PROJECTS_FILE = Path("data/projects.json")

with PROJECTS_FILE.open("r", encoding="utf-8") as file:
    projects = json.load(file)


if "project_index" not in st.session_state:
    st.session_state.project_index = 0


def previous_projects():
    st.session_state.project_index = max(
        0,
        st.session_state.project_index - 2,
    )


def next_projects():
    if st.session_state.project_index + 2 < len(projects):
        st.session_state.project_index += 2


st.markdown(
    """
    <style>

    header[data-testid="stHeader"] {
        display: none !important;
    }

    div[data-testid="stToolbar"] {
        display: none !important;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    html,
    body,
    [data-testid="stAppViewContainer"],
    .stApp {
        background: #0f172a;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 18% 10%,
                rgba(59, 130, 246, 0.10),
                transparent 28%
            ),
            radial-gradient(
                circle at 85% 22%,
                rgba(99, 102, 241, 0.08),
                transparent 30%
            ),
            linear-gradient(
                180deg,
                #0f172a 0%,
                #111827 45%,
                #0b1220 100%
            );

        color: #e5e7eb;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }

    h1,
    h2,
    h3 {
        color: #f8fafc !important;
        letter-spacing: -0.02em;
    }

    p,
    li,
    label {
        color: #cbd5e1 !important;
    }

    .hero-role {
        font-size: 1.35rem;
        font-weight: 500;
        color: #94a3b8;
        margin-top: -0.5rem;
        margin-bottom: 1rem;
    }

    .hero-description {
        max-width: 760px;
        font-size: 1.05rem;
        line-height: 1.8;
        color: #cbd5e1;
        margin-bottom: 1.4rem;
    }

    .section-title {
        font-size: 2rem;
        font-weight: 700;
        margin-top: 1rem;
        margin-bottom: 0;
        color: #f8fafc;
    }

    hr {
        border-color: rgba(148, 163, 184, 0.12);
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(15, 23, 42, 0.55);
        border: 1px solid rgba(148, 163, 184, 0.14);
        border-radius: 20px;
        backdrop-filter: blur(8px);
        min-height: 315px;

        transition:
            transform 0.22s ease,
            border-color 0.22s ease,
            box-shadow 0.22s ease,
            background 0.22s ease;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-4px);
        border-color: rgba(96, 165, 250, 0.30);
        background: rgba(17, 24, 39, 0.72);
        box-shadow: 0 18px 35px rgba(2, 6, 23, 0.35);
    }

    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        min-height: 285px;
    }

    .project-description {
        min-height: 88px;
        color: #cbd5e1;
        line-height: 1.7;
        margin-bottom: 0.2rem;
    }

    div.stButton > button,
    div.stLinkButton > a {
        background: rgba(255, 255, 255, 0.04) !important;
        color: #e5e7eb !important;
        border: 1px solid rgba(148, 163, 184, 0.18) !important;
        border-radius: 12px !important;
        padding: 0.65rem 1rem !important;
        text-decoration: none !important;

        transition:
            transform 0.18s ease,
            background 0.18s ease,
            border-color 0.18s ease,
            box-shadow 0.18s ease;
    }

    div.stButton > button:hover,
    div.stLinkButton > a:hover {
        transform: translateY(-2px);
        background: rgba(255, 255, 255, 0.07) !important;
        border-color: rgba(96, 165, 250, 0.35) !important;
        box-shadow: 0 8px 24px rgba(2, 6, 23, 0.18);
    }

    div.stButton > button:disabled {
        background: rgba(255, 255, 255, 0.025) !important;
        color: #94a3b8 !important;
        border: 1px solid rgba(148, 163, 184, 0.10) !important;
        opacity: 0.7 !important;
    }

    div[data-testid="stCaptionContainer"] {
        color: #94a3b8 !important;
    }

    div[data-testid="stAlert"] {
        background: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 16px;
        color: #cbd5e1;
    }

    div[data-testid="stVerticalBlock"] {
        gap: 0.85rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


st.title("Abdallah Al-Habaibeh")

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


button_columns = st.columns([1.1, 1.1, 1.1, 1.2, 4])

with button_columns[0]:
    st.link_button(
        "GitHub",
        "https://github.com/Abdallh-AlHabaibeh",
        use_container_width=True,
    )

with button_columns[1]:
    st.button(
        "LinkedIn",
        disabled=True,
        use_container_width=True,
    )

with button_columns[2]:
    st.button(
        "Email",
        disabled=True,
        use_container_width=True,
    )

with button_columns[3]:
    st.button(
        "Download CV",
        disabled=True,
        use_container_width=True,
    )


st.divider()


projects_title_col, arrows_col = st.columns([8, 2])

with projects_title_col:
    st.markdown(
        '<div class="section-title">Projects</div>',
        unsafe_allow_html=True,
    )

with arrows_col:
    left_arrow, right_arrow = st.columns(2)

    with left_arrow:
        st.button(
            "←",
            on_click=previous_projects,
            disabled=st.session_state.project_index == 0,
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
        with st.container(border=True):

            st.subheader(project["title"])

            st.markdown(
                f"""
                <div class="project-description">
                    {project["description"]}
                </div>
                """,
                unsafe_allow_html=True,
            )

            if project.get("metric"):
                st.markdown(
                    f"**{project['metric']}**"
                )

            tech_string = " • ".join(
                project["tech"]
            )

            st.caption(tech_string)

            github_button, demo_button = st.columns(2)

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
                        key=f'demo_{project["title"]}',
                    )


st.divider()


st.markdown(
    '<div class="section-title">Ask My Portfolio</div>',
    unsafe_allow_html=True,
)

st.write(
    """
    Ask questions about my projects, technical experience,
    skills, education, or background.
    """
)