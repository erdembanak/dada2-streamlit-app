from __future__ import annotations

from dataclasses import dataclass

import streamlit as st


@dataclass(frozen=True)
class Criterion:
    key: str
    label: str
    points: int
    help_text: str


FEATURE_META = {
    "hem_bicytopenia": "Two or more blood cell lines affected.",
    "hypogammaglob": "Low immunoglobulin levels.",
    "neuro_involv": "Neurologic or central nervous system involvement.",
    "AFR_high": "Elevated acute phase reactants.",
    "musculoskeletal": "Musculoskeletal involvement such as arthritis or myalgia.",
    "skin_involv": "Skin involvement such as vasculitic lesions or livedo.",
    "constutional": "Constitutional symptoms.",
    "ulcer": "Ulcer present.",
    "thrombocytosis": "Elevated platelet count.",
    "family_history": "Relevant family history.",
    "thrombocytopenia": "Low platelet count.",
    "renal_invol": "Renal involvement.",
    "consanguinity": "Parental consanguinity.",
}


SCORE_NAME = "DADA2 Clinical Score"
SCORE_HEADLINE = "Select the relevant clinical findings to calculate the score."
SCORE_THRESHOLD = 10
SCORE_CRITERIA = [
    Criterion("hem_bicytopenia", "Bicytopenia", 5, FEATURE_META["hem_bicytopenia"]),
    Criterion("musculoskeletal", "Musculoskeletal involvement", 4, FEATURE_META["musculoskeletal"]),
    Criterion("hypogammaglob", "Hypogammaglobulinemia", 4, FEATURE_META["hypogammaglob"]),
    Criterion("neuro_involv", "Neurologic involvement", 3, FEATURE_META["neuro_involv"]),
    Criterion("AFR_high", "High acute phase reactants", 2, FEATURE_META["AFR_high"]),
    Criterion("family_history", "Family history", 2, FEATURE_META["family_history"]),
    Criterion("skin_involv", "Skin involvement", 1, FEATURE_META["skin_involv"]),
    Criterion("consanguinity", "Consanguinity", 1, FEATURE_META["consanguinity"]),
    Criterion("thrombocytosis", "Thrombocytosis", -3, FEATURE_META["thrombocytosis"]),
]


def apply_styles() -> None:
    st.markdown(
        """
        <style>
            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(214, 167, 93, 0.22), transparent 28%),
                    linear-gradient(180deg, #f6f2e9 0%, #fbf8f3 100%);
                color: #1f2933;
            }
            .block-container {
                max-width: 920px;
                padding-top: 2rem;
                padding-bottom: 3rem;
            }
            [data-testid="stSidebar"] {
                background:
                    radial-gradient(circle at top left, rgba(214, 167, 93, 0.18), transparent 32%),
                    linear-gradient(180deg, #efe3cd 0%, #f7efe1 100%);
                border-right: 1px solid #dbc8aa;
            }
            [data-testid="stSidebar"] > div:first-child {
                background: transparent;
            }
            [data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
                padding: 0.9rem 0.85rem 1rem 0.85rem;
            }
            [data-testid="stSidebar"] [data-testid="stExpander"] {
                background: rgba(255, 255, 255, 0.65);
                border: 1px solid #dbc8aa;
                border-radius: 14px;
                overflow: hidden;
            }
            [data-testid="stSidebar"] [data-testid="stExpander"] details summary {
                padding: 0.45rem 0.8rem;
                font-size: 0.92rem;
            }
            [data-testid="stSidebar"] [data-testid="stExpanderDetails"] {
                padding: 0.15rem 0.8rem 0.65rem 0.8rem;
            }
            [data-testid="stSidebar"] .stMarkdown p,
            [data-testid="stSidebar"] .stMarkdown li {
                font-size: 0.9rem;
                line-height: 1.35;
            }
            [data-testid="stSidebar"] .stButton > button {
                background: #8b5e34;
                color: #fffdf9;
                border: 1px solid #7a512d;
                border-radius: 12px;
                min-height: 2.35rem;
                padding: 0.35rem 0.75rem;
                font-size: 0.92rem;
            }
            [data-testid="stSidebar"] .stButton > button:hover {
                background: #744a28;
                color: #fffdf9;
                border-color: #744a28;
            }
            @media (max-width: 768px) {
                [data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
                    padding: 0.7rem 0.65rem 0.85rem 0.65rem;
                }
                [data-testid="stSidebar"] [data-testid="stExpander"] details summary {
                    padding: 0.38rem 0.65rem;
                    font-size: 0.88rem;
                }
                [data-testid="stSidebar"] [data-testid="stExpanderDetails"] {
                    padding: 0.1rem 0.65rem 0.55rem 0.65rem;
                }
                [data-testid="stSidebar"] .stButton > button {
                    min-height: 2.1rem;
                    padding: 0.3rem 0.65rem;
                    font-size: 0.88rem;
                }
            }
            .app-card {
                background: rgba(255, 255, 255, 0.86);
                border: 1px solid #dbc8aa;
                border-radius: 18px;
                padding: 1rem 1.1rem;
                box-shadow: 0 12px 32px rgba(69, 54, 32, 0.08);
                margin-bottom: 1rem;
            }
            .app-kicker {
                font-size: 0.8rem;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: #8b5e34;
                margin-bottom: 0.4rem;
            }
            .result-ok {
                border-left: 6px solid #2f6f4f;
            }
            .result-watch {
                border-left: 6px solid #9a6b11;
            }
            .mono-chip {
                display: inline-block;
                border-radius: 999px;
                padding: 0.18rem 0.6rem;
                background: #f0e4cf;
                color: #6a4a24;
                margin-right: 0.4rem;
                margin-bottom: 0.35rem;
                font-size: 0.88rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def format_points(points: int) -> str:
    return f"{points:+d}"


def compute_score(criteria: list[Criterion]) -> tuple[int, list[Criterion]]:
    selected: list[Criterion] = []
    total = 0
    for criterion in criteria:
        if st.session_state.get(criterion.key, False):
            selected.append(criterion)
            total += criterion.points
    return total, selected


def reset_selected() -> None:
    for criterion in SCORE_CRITERIA:
        st.session_state[criterion.key] = False


def render_rule_table(criteria: list[Criterion], threshold: int) -> None:
    st.markdown("### Scoring rule")
    for criterion in criteria:
        st.markdown(
            f"- **{criterion.label}**: {format_points(criterion.points)} point(s)",
        )
    st.markdown(f"- **Threshold**: score >= {threshold}")


def build_summary(
    threshold: int,
    score: int,
    selected: list[Criterion],
) -> str:
    selected_lines = "\n".join(
        f"- {criterion.label}: {format_points(criterion.points)}"
        for criterion in selected
    ) or "- No findings selected"
    verdict = (
        "Threshold met or exceeded"
        if score >= threshold
        else "Below selected threshold"
    )
    return (
        f"DADA2 score summary\n\n"
        f"System: {SCORE_NAME}\n"
        f"Score: {score}\n"
        f"Threshold: {threshold}\n"
        f"Result: {verdict}\n\n"
        f"Selected findings:\n{selected_lines}\n"
    )


def main() -> None:
    st.set_page_config(
        page_title="DADA2 Clinical Score",
        page_icon="🩺",
        layout="centered",
    )
    apply_styles()

    st.title("DADA2 Clinical Score")
    st.caption(
        "Patient-level calculator only. This app does not load or display any existing dataset."
    )
    criteria = SCORE_CRITERIA
    threshold = SCORE_THRESHOLD

    with st.container():
        st.markdown(
            f"""
            <div class="app-card">
                <div class="app-kicker">Clinical Score</div>
                <strong>{SCORE_NAME}</strong><br/>
                {SCORE_HEADLINE}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with st.sidebar:
        if st.button("Clear all inputs", use_container_width=True):
            reset_selected()
            st.rerun()
        with st.expander("Scoring rule"):
            render_rule_table(criteria, threshold)

    st.markdown("### Findings")
    left_col, right_col = st.columns(2)
    for index, criterion in enumerate(criteria):
        container = left_col if index % 2 == 0 else right_col
        container.checkbox(
            f"{criterion.label} ({format_points(criterion.points)})",
            key=criterion.key,
            help=criterion.help_text,
        )

    score, selected = compute_score(criteria)
    meets_threshold = score >= threshold
    delta = score - threshold

    result_class = "result-ok" if meets_threshold else "result-watch"
    verdict = "Threshold met" if meets_threshold else "Below threshold"
    guidance = (
        "The entered findings reach the selected score threshold. Use this as decision support and confirm with clinical judgment and genetic testing as appropriate."
        if meets_threshold
        else "The entered findings do not reach the selected threshold. A low score does not exclude disease when suspicion remains high."
    )

    st.markdown("### Result")
    st.markdown(
        f"""
        <div class="app-card {result_class}">
            <div class="app-kicker">Interpretation</div>
            <strong>{verdict}</strong><br/>
            Score: {score} | Threshold: {threshold} | Delta: {delta:+d}<br/><br/>
            {guidance}
        </div>
        """,
        unsafe_allow_html=True,
    )

    metric_cols = st.columns(3)
    metric_cols[0].metric("Score", score)
    metric_cols[1].metric("Threshold", threshold)
    metric_cols[2].metric("Status", "Positive" if meets_threshold else "Negative")

    st.markdown("### Selected contributions")
    if selected:
        chip_markup = "".join(
            f'<span class="mono-chip">{criterion.label}: {format_points(criterion.points)}</span>'
            for criterion in selected
        )
        st.markdown(chip_markup, unsafe_allow_html=True)
    else:
        st.info("No findings selected yet.")

    summary = build_summary(threshold, score, selected)
    st.download_button(
        "Download summary",
        data=summary,
        file_name="dada2_score_summary.txt",
        mime="text/plain",
        use_container_width=False,
    )

if __name__ == "__main__":
    main()
