import json
import os
import pytest
from agents.serialization_agent import SerializationAgent


@pytest.fixture
def serialization_agent():
    return SerializationAgent()


@pytest.fixture
def sample_page_content():
    return {
        "page_type": "product_page",
        "product_overview": {"title": "GlowBoost"},
    }


# -------------------------
# Serialization Tests
# -------------------------
def test_serialization_creates_file(
    serialization_agent,
    sample_page_content,
    tmp_path,
):
    output_dir = tmp_path / "output"

    file_path = serialization_agent.serialize(
        page_type="product_page",
        page_content=sample_page_content,
        output_dir=str(output_dir),
    )

    assert os.path.exists(file_path)

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["page_type"] == "product_page"
    assert data["product_overview"]["title"] == "GlowBoost"


def test_serialization_file_name_correct(
    serialization_agent,
    sample_page_content,
    tmp_path,
):
    output_dir = tmp_path / "output"

    file_path = serialization_agent.serialize(
        page_type="faq",
        page_content={"page_type": "faq", "questions": []},
        output_dir=str(output_dir),
    )

    assert file_path.endswith("faq.json")


def test_invalid_page_type_raises_error(serialization_agent):
    with pytest.raises(ValueError):
        serialization_agent.serialize(
            page_type="invalid_page",
            page_content={},
        )


def test_output_directory_auto_created(
    serialization_agent,
    sample_page_content,
    tmp_path,
):
    output_dir = tmp_path / "nested" / "dir" / "output"

    file_path = serialization_agent.serialize(
        page_type="product_page",
        page_content=sample_page_content,
        output_dir=str(output_dir),
    )

    assert os.path.exists(output_dir)
    assert os.path.exists(file_path)
