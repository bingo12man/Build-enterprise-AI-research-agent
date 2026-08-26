import json
from pathlib import Path

from app.models.exceptions import (
    ResearchAgentError,
)
from app.models.research import (
    ResearchRequest,
)
from app.services.research_service import (
    run_research,
)


EVAL_FILE = Path(
    "evals/evaluation_questions.json"
)


def load_evaluation_questions():
    with EVAL_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def contains_expected_topics(
    text: str,
    topics,
) -> bool:

    text_lower = text.lower()

    return all(
        topic.lower() in text_lower
        for topic in topics
    )


def collect_generated_citations(
    result,
):

    citation_ids = set()

    for finding in result.findings:
        citation_ids.update(
            finding.source_ids
        )

    for opportunity in result.opportunities:
        citation_ids.update(
            opportunity.source_ids
        )

    for risk in result.risks:
        citation_ids.update(
            risk.source_ids
        )

    return citation_ids


def calculate_percentage(
    passed: int,
    total: int,
) -> float:

    if total == 0:
        return 0.0

    return (
        passed / total
    ) * 100


def run_evaluation():

    questions = (
        load_evaluation_questions()
    )

    total = len(questions)

    overall_passed = 0
    behavior_passed_count = 0
    topic_passed_count = 0

    relevant_total = 0
    retrieval_relevant_count = 0

    unsupported_total = 0
    unsupported_rejected_count = 0

    citation_cases = 0
    citation_valid_count = 0

    execution_failure_count = 0

    for item in questions:

        print(
            "\n=============================="
        )

        print(
            "Evaluation:",
            item["id"],
        )

        print(
            "Query:",
            item["query"],
        )

        expected_behavior = (
            item["expected_behavior"]
        )

        if (
            expected_behavior
            == "insufficient_evidence"
        ):
            unsupported_total += 1

        else:
            relevant_total += 1

        request = ResearchRequest(
            query=item["query"],
            industry=item["industry"],
        )

        try:

            result = run_research(
                request
            )

        except ResearchAgentError as error:

            execution_failure_count += 1

            print(
                "Research execution failed:",
                str(error),
            )

            print(
                "Expected behavior:",
                expected_behavior,
            )

            print(
                "Behavior passed:",
                False,
            )

            print(
                "Topic check passed:",
                False,
            )

            print(
                "Citation check passed:",
                False,
            )

            print(
                "TEST PASSED:",
                False,
            )

            continue

        if (
            expected_behavior
            == "insufficient_evidence"
        ):

            behavior_passed = (
                result.confidence.level == "Low"
                and not result.findings
                and not result.opportunities
            )

            if behavior_passed:
                unsupported_rejected_count += 1

        else:

            behavior_passed = (
                result.confidence.level
                in ["Medium", "High"]
                and bool(result.summary)
            )

            if (
                result.confidence.level
                in ["Medium", "High"]
            ):
                retrieval_relevant_count += 1

        if behavior_passed:
            behavior_passed_count += 1

        combined_text = " ".join(
            [
                result.summary,
                *[
                    finding.description
                    for finding
                    in result.findings
                ],
                *[
                    opportunity.description
                    for opportunity
                    in result.opportunities
                ],
                *[
                    risk.description
                    for risk
                    in result.risks
                ],
            ]
        )

        if item["expected_topics"]:

            topic_passed = (
                contains_expected_topics(
                    combined_text,
                    item["expected_topics"],
                )
            )

        else:
            topic_passed = True

        if topic_passed:
            topic_passed_count += 1

        valid_source_ids = {
            source.source_id
            for source in result.sources
        }

        generated_citations = (
            collect_generated_citations(
                result
            )
        )

        if generated_citations:

            citation_cases += 1

            invalid_citations = (
                generated_citations
                - valid_source_ids
            )

            citation_valid = (
                len(
                    invalid_citations
                ) == 0
            )

            if citation_valid:
                citation_valid_count += 1

        else:

            citation_valid = True

        test_passed = (
            behavior_passed
            and topic_passed
            and citation_valid
        )

        if test_passed:
            overall_passed += 1

        print(
            "Expected behavior:",
            expected_behavior,
        )

        print(
            "Actual confidence:",
            result.confidence.level,
        )

        print(
            "Behavior passed:",
            behavior_passed,
        )

        print(
            "Topic check passed:",
            topic_passed,
        )

        print(
            "Citation check passed:",
            citation_valid,
        )

        print(
            "TEST PASSED:",
            test_passed,
        )

    overall_pass_rate = calculate_percentage(
        overall_passed,
        total,
    )

    behavior_accuracy = calculate_percentage(
        behavior_passed_count,
        total,
    )

    topic_coverage_rate = calculate_percentage(
        topic_passed_count,
        total,
    )

    retrieval_relevance_rate = calculate_percentage(
        retrieval_relevant_count,
        relevant_total,
    )

    unsupported_rejection_rate = calculate_percentage(
        unsupported_rejected_count,
        unsupported_total,
    )

    citation_validity_rate = calculate_percentage(
        citation_valid_count,
        citation_cases,
    )

    print(
        "\n=============================="
    )

    print(
        "EVALUATION REPORT"
    )

    print(
        "Overall pass rate:",
        f"{overall_pass_rate:.2f}%",
    )

    print(
        "Behavior accuracy:",
        f"{behavior_accuracy:.2f}%",
    )

    print(
        "Topic coverage rate:",
        f"{topic_coverage_rate:.2f}%",
    )

    print(
        "Retrieval relevance rate:",
        f"{retrieval_relevance_rate:.2f}%",
    )

    print(
        "Unsupported query rejection rate:",
        f"{unsupported_rejection_rate:.2f}%",
    )

    print(
        "Citation validity rate:",
        f"{citation_validity_rate:.2f}%",
    )

    print(
        "\nRaw counts:"
    )

    print(
        f"Overall passed: "
        f"{overall_passed}/{total}"
    )

    print(
        f"Relevant queries accepted: "
        f"{retrieval_relevant_count}/"
        f"{relevant_total}"
    )

    print(
        f"Unsupported queries rejected: "
        f"{unsupported_rejected_count}/"
        f"{unsupported_total}"
    )

    print(
        f"Citation-valid cases: "
        f"{citation_valid_count}/"
        f"{citation_cases}"
    )

    print(
        f"Execution failures: "
        f"{execution_failure_count}/{total}"
    )


if __name__ == "__main__":
    run_evaluation()