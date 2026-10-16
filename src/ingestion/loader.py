
import pymupdf
from pathlib import Path


def extract_text(pdf_path: str) -> str:
    """Extract text from all pages of a PDF research paper."""

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    with pymupdf.open(path) as document:
        pages = []

        for page_number, page in enumerate(document, start=1):
            text = page.get_text()

            pages.append(
                f"\n--- Page {page_number} ---\n{text}"
            )

    return "\n".join(pages)


if __name__ == "__main__":
    pdf_path = "data/papers/diabetes_prediction.pdf"

    extracted_text = extract_text(pdf_path)

    print("Text extraction successful!")
    print(f"Total characters: {len(extracted_text)}")
    print("\nFirst 2000 characters:\n")
    print(extracted_text[:2000])
