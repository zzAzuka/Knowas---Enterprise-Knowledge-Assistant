from app.services.pdfTextExtraction import (
    cleanExtractedText,
    chunkingText,
)

def test_clean_extracted_text_removes_blank_lines():
    input_text = "Line 1\n\n   \nLine 2  \n  Line 3\n\n"
    expected_output = "Line 1\nLine 2\nLine 3"

    result = cleanExtractedText(input_text)
    assert result == expected_output

def test_chunking_text_splits_long_text():
    long_text = "A" * 2500
    chunks = chunkingText(long_text)
    assert isinstance(chunks, list)
    assert len(chunks) > 1
    assert all(isinstance(c, str) for c in chunks)

