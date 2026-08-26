import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import requests
import streamlit as st

from app.models.research import ResearchRequest
from app.services.research_service import run_research
from app.repositories.research_repository import get_recent_research


st.set_page_config(
    page_title="Enterprise AI Research Agent",
    layout="wide",
)


st.title(
    "Enterprise AI Research Agent"
)

st.write(
    "Ask a business research question and "
    "receive a grounded AI-generated report."
)


query = st.text_area(
    "Research Question",
    placeholder=(
        "Example: What AI opportunities can "
        "help a manufacturing company?"
    ),
)


industry = st.text_input(
    "Industry",
    value="manufacturing",
)


run_button = st.button(
    "Run Research"
)


if run_button:

    if not query.strip():

        st.warning(
            "Please enter a research question."
        )

    else:

        try:

            with st.spinner(
                "Running research..."
            ):

                request = ResearchRequest(
                    query=query.strip(),
                    industry=(
                        industry.strip()
                        if industry.strip()
                        else None
                    ),
                )

                result = run_research(
                    request
                )

                result = result.model_dump()

            st.success(
                "Research completed."
            )

            st.subheader(
                "Research Summary"
            )

            st.write(
                result["summary"]
            )


            st.subheader(
                "Key Findings"
            )

            if result["findings"]:

                for finding in result["findings"]:

                    st.markdown(
                        f"### {finding['title']}"
                    )

                    st.write(
                        finding["description"]
                    )

                    st.caption(
                        "Sources: "
                        + ", ".join(
                            finding[
                                "source_ids"
                            ]
                        )
                    )

            else:

                st.info(
                    "No findings available."
                )


            st.subheader(
                "Recommended AI Opportunities"
            )

            if result["opportunities"]:

                for opportunity in (
                    result["opportunities"]
                ):

                    st.markdown(
                        f"### {opportunity['title']}"
                    )

                    st.write(
                        opportunity[
                            "description"
                        ]
                    )

                    st.write(
                        "Expected Value:",
                        opportunity[
                            "expected_value"
                        ],
                    )

                    st.write(
                        "Difficulty:",
                        opportunity[
                            "difficulty"
                        ],
                    )

                    st.caption(
                        "Sources: "
                        + ", ".join(
                            opportunity[
                                "source_ids"
                            ]
                        )
                    )

            else:

                st.info(
                    "No opportunities available."
                )


            st.subheader(
                "Risks and Gaps"
            )

            if result["risks"]:

                for risk in result["risks"]:

                    st.markdown(
                        f"### {risk['title']}"
                    )

                    st.write(
                        risk["description"]
                    )

                    st.caption(
                        "Sources: "
                        + ", ".join(
                            risk[
                                "source_ids"
                            ]
                        )
                    )

            else:

                st.info(
                    "No risks available."
                )


            st.subheader(
                "Supporting Evidence"
            )

            if result["sources"]:

                for source in result["sources"]:

                    source_id = source[
                        "source_id"
                    ]

                    source_name = source[
                        "source_name"
                    ]

                    source_type = source.get(
                        "source_type",
                        "internal",
                    )

                    source_url = source.get(
                        "source_url"
                    )

                    evidence_text = source[
                        "evidence_text"
                    ]

                    st.markdown(
                        f"### {source_id} — "
                        f"{source_name}"
                    )

                    st.write(
                        f"Source Type: "
                        f"{source_type}"
                    )

                    if (
                        source_type == "web"
                        and source_url
                    ):

                        st.markdown(
                            f"[Open Source]("
                            f"{source_url}"
                            f")"
                        )

                    with st.expander(
                        "View Evidence"
                    ):

                        st.write(
                            evidence_text
                        )

            else:

                st.info(
                    "No supporting evidence available."
                )


            st.subheader(
                "Evidence Confidence"
            )

            st.write(
                result["confidence"]["level"]
            )

            st.write(
                result["confidence"][
                    "explanation"
                ]
            )

            st.caption(
                "Research ID: "
                + result["research_id"]
            )


        except requests.HTTPError as error:

            try:

                detail = (
                    error.response.json().get(
                        "detail",
                        "Research failed.",
                    )
                )

            except ValueError:

                detail = (
                    "Research failed."
                )

            st.error(
                detail
            )


        except requests.RequestException:

            st.error(
                "Could not connect to "
                "the backend API."
            )

        except Exception as error:

            st.error(
                "Research failed. "
                "Please try again."
            )

            st.exception(
                error
            )


st.divider()


st.subheader(
    "Recent Research History"
)


try:

    history = get_recent_research(
        limit=5
    )


    if not history:

        st.info(
            "No research history available."
        )

    else:

        for item in history:

            with st.expander(
                item["query"]
            ):

                st.write(
                    item["summary"]
                )

                st.write(
                    "Confidence:",
                    item[
                        "confidence_level"
                    ],
                )

                st.write(
                    item[
                        "confidence_explanation"
                    ]
                )

                st.caption(
                    "Research ID: "
                    + item["research_id"]
                )

                st.caption(
                    "Created at: "
                    + item["created_at"]
                )


except Exception:

    st.warning(
        "Research history is "
        "temporarily unavailable."
    )