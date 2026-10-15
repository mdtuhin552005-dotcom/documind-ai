from langchain_core.messages import AIMessage

from app.services.chat import extract_answer_text


def test_extract_answer_text_supports_gemini_text_content_blocks() -> None:
    message = AIMessage(
        content=[
            {"type": "thinking", "thinking": "Internal reasoning is not user-facing."},
            {"type": "text", "text": "  The answer is **42**.  ", "extras": {}},
        ]
    )

    assert extract_answer_text(message) == "The answer is **42**."


def test_extract_answer_text_supports_plain_string_responses() -> None:
    assert extract_answer_text(AIMessage(content="  Plain text answer.  ")) == "Plain text answer."
