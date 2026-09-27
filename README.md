# Ask My Portfolio

A personal AI/ML portfolio built with Streamlit, featuring selected projects, live demos, professional background, and a RAG-based assistant that answers questions using portfolio-specific context.

Live portfolio:  
https://ask-my-portfolio.streamlit.app

## Overview

The portfolio is designed as a simple way to explore my work in AI, machine learning, computer vision, and LLM-based applications.

It includes:

- Selected AI/ML projects
- Live project demos
- Project metrics and technology stacks
- Professional experience and technical skills
- Downloadable CV
- A portfolio assistant powered by retrieval-augmented generation

## Featured Projects

### Chess Vision Tutor

A computer vision pipeline that converts a physical chessboard image into a structured board representation and provides engine-assisted chess analysis.

The system combines:

- OpenCV for board localization and perspective correction
- ResNet18 and YOLO11 for chess piece recognition
- `python-chess` for board representation and validation
- Stockfish for chess analysis
- Gemini for natural-language tutoring

Evaluation included both a formal test set and an additional real-world stress test.

### Face Recognition V2

A real-time face recognition system built with InsightFace and OpenCV.

The system:

- Generates facial embeddings from known identities
- Detects and recognizes faces from webcam input
- Distinguishes recognized and unknown faces
- Logs recognition results
- Includes controlled and group-image stress testing

The stress test achieved 93.10% known-face recognition accuracy with no false-positive identities.

## Portfolio Assistant

The portfolio includes a small retrieval-augmented generation system that answers questions using information from:

- Project documentation
- Professional experience
- Technical skills
- Public profile information

The assistant retrieves relevant portfolio context using embeddings before generating a response.

It is designed to stay grounded in the supplied portfolio information and avoid inventing unsupported details.

## Tech Stack

- Python
- Streamlit
- Gemini API
- Gemini Embeddings
- NumPy
- Retrieval-Augmented Generation
- HTML/CSS
- Git / GitHub

## Project Structure

```text
ask-my-portfolio/
├── assets/
├── config/
├── data/
├── images/
├── rag/
├── ui/
├── app.py
├── pyproject.toml
├── uv.lock
└── README.md