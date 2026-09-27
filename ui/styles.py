import streamlit as st


def apply_styles():
    st.markdown(
        """
        <style>

        html {
            scroll-behavior: smooth;
        }

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

        .project-card {
            position: relative;
            min-height: 300px;
            padding: 1.35rem;
            margin-bottom: 0.75rem;
            border-radius: 18px;
            overflow: hidden;

            background-color: rgba(15, 23, 42, 0.82);
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;

            border: 1px solid rgba(148, 163, 184, 0.16);

            box-shadow:
                0 12px 28px rgba(2, 6, 23, 0.20);

            transition:
                transform 0.22s ease,
                border-color 0.22s ease,
                box-shadow 0.22s ease;
        }

        .project-card-overlay {
            position: absolute;
            inset: 0;
            background: rgba(2, 6, 23, 0.12);
            pointer-events: none;

            transition:
                background 0.22s ease;
        }

        .project-card-content {
            position: relative;
            z-index: 2;
            min-height: 252px;
            display: flex;
            flex-direction: column;
        }

        .project-card h3 {
            margin: 0;
            color: #f8fafc !important;
            font-size: 1.55rem;
            line-height: 1.25;
            text-shadow:
                0 2px 8px rgba(0, 0, 0, 0.45);
        }

        .project-card-description {
            margin-top: 1rem;
            color: #e2e8f0;
            line-height: 1.7;

            opacity: 0;
            max-height: 0;
            overflow: hidden;

            transform: translateY(10px);

            transition:
                opacity 0.22s ease,
                transform 0.22s ease,
                max-height 0.28s ease;
        }

        .project-card-bottom {
            margin-top: auto;
            padding-top: 1.1rem;
        }

        .project-card-metric {
            color: #f1f5f9;
            font-weight: 700;
            line-height: 1.5;
            margin-bottom: 0.65rem;
            text-shadow:
                0 1px 5px rgba(0, 0, 0, 0.35);
        }

        .project-card-tech {
            color: #cbd5e1;
            font-size: 0.9rem;
            line-height: 1.5;
            text-shadow:
                0 1px 5px rgba(0, 0, 0, 0.40);
        }

        .project-card:hover {
            transform: translateY(-3px);
            border-color: rgba(96, 165, 250, 0.38);

            box-shadow:
                0 18px 36px rgba(2, 6, 23, 0.34);
        }

        .project-card:hover .project-card-overlay {
            background: rgba(2, 6, 23, 0.48);
        }

        .project-card:hover .project-card-description {
            opacity: 1;
            max-height: 180px;
            transform: translateY(0);
        }

        div.stButton > button,
        div.stLinkButton > a, 
        div.stDownloadButton > button{
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
        div.stLinkButton > a:hover,
        div.stDownloadButton > button:hover{
            transform: translateY(-1px);
            background: rgba(255, 255, 255, 0.07) !important;
            border-color: rgba(96, 165, 250, 0.35) !important;
            box-shadow:
                0 8px 24px rgba(2, 6, 23, 0.18);
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
            border-radius: 12px;
            color: #cbd5e1;
        }

        div[data-testid="stVerticalBlock"] {
            gap: 0.85rem;
        }

        div[data-testid="stChatInput"] {
            background: transparent !important;
        }

        div[data-testid="stBottomBlockContainer"] {
            background: #0b1220 !important;
            border-top: 1px solid rgba(148, 163, 184, 0.10) !important;
        }

        div[data-testid="stChatInput"] > div {
            background: rgba(15, 23, 42, 0.88) !important;
            border-radius: 8px !important;
            border: 1px solid rgba(148, 163, 184, 0.18) !important;
        }

        div[data-testid="stChatInput"] textarea {
            background: transparent !important;
            color: #f1f5f9 !important;
            -webkit-text-fill-color: #f1f5f9 !important;
            border: none !important;
            border-radius: 8px !important;
            opacity: 1 !important;
        }

        div[data-testid="stChatInput"] textarea::placeholder {
            color: #a8b3c7 !important;
            -webkit-text-fill-color: #a8b3c7 !important;
            opacity: 1 !important;
        }

        div[data-testid="stChatInput"] textarea:disabled {
            color: #cbd5e1 !important;
            -webkit-text-fill-color: #cbd5e1 !important;
            opacity: 1 !important;
        }

        div[data-testid="stChatInput"] textarea:disabled::placeholder {
            color: #94a3b8 !important;
            -webkit-text-fill-color: #94a3b8 !important;
            opacity: 1 !important;
        }

        div[data-testid="stChatInput"] button {
            background: rgba(30, 41, 59, 0.95) !important;
            color: #e5e7eb !important;
            border-radius: 8px !important;
            border: 1px solid rgba(148, 163, 184, 0.16) !important;
        }

        div[data-testid="stChatInput"] button:hover {
            background: rgba(51, 65, 85, 0.95) !important;
            border-color: rgba(96, 165, 250, 0.30) !important;
        }

        .back-to-top {
            margin-top: 1.6rem;
            text-align: right;
        }

        .back-to-top a {
            display: inline-block;
            padding: 0.55rem 0.8rem;

            color: #94a3b8;
            background: rgba(255, 255, 255, 0.03);

            border: 1px solid rgba(148, 163, 184, 0.12);
            border-radius: 8px;

            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 500;

            transition:
                color 0.18s ease,
                background 0.18s ease,
                border-color 0.18s ease,
                transform 0.18s ease;
        }

        .back-to-top a:hover {
            color: #f1f5f9;
            background: rgba(255, 255, 255, 0.06);
            border-color: rgba(96, 165, 250, 0.30);
            transform: translateY(-1px);
        }

        @media (hover: none) {
            .project-card-description {
                opacity: 1;
                max-height: 180px;
                transform: translateY(0);
            }

            .project-card-overlay {
                background: rgba(2, 6, 23, 0.42);
            }
        }

        @media (max-width: 700px) {
            .project-card {
                min-height: 320px;
            }

            .project-card-content {
                min-height: 272px;
            }

            .project-card h3 {
                font-size: 1.4rem;
            }

            .project-card-description {
                font-size: 0.95rem;
            }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )