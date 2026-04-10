from __future__ import annotations

import math
import re


class FixedSizeChunker:
    """
    Split text into fixed-size chunks with optional overlap.

    Rules:
        - Each chunk is at most chunk_size characters long.
        - Consecutive chunks share overlap characters.
        - The last chunk contains whatever remains.
        - If text is shorter than chunk_size, return [text].
    """

    def __init__(self, chunk_size: int = 500, overlap: int = 50) -> None:
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> list[str]:
        if not text:
            return []
        if len(text) <= self.chunk_size:
            return [text]

        step = self.chunk_size - self.overlap
        chunks: list[str] = []
        for start in range(0, len(text), step):
            chunk = text[start : start + self.chunk_size]
            chunks.append(chunk)
            if start + self.chunk_size >= len(text):
                break
        return chunks


class SentenceChunker:
    """
    Split text into chunks of at most max_sentences_per_chunk sentences.

    Sentence detection: split on ". ", "! ", "? " or ".\n".
    Strip extra whitespace from each chunk.
    """

    def __init__(self, max_sentences_per_chunk: int = 3) -> None:
        self.max_sentences_per_chunk = max(1, max_sentences_per_chunk)

    def chunk(self, text: str) -> list[str]:
        if not text:
            return []

        # Split on sentence boundaries: ". ", "! ", "? ", or ".\n"
        # Use regex to split while keeping the delimiter
        sentences = re.split(r'(?<=[.!?])\s+|\.\n', text)

        # Remove empty strings
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return []

        # Group sentences into chunks
        chunks: list[str] = []
        current_chunk: list[str] = []

        for sentence in sentences:
            current_chunk.append(sentence)

            if len(current_chunk) >= self.max_sentences_per_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = []

        # Add remaining sentences as the last chunk
        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks



class RecursiveChunker:
    """
    Recursively split text using separators in priority order.

    Default separator priority:
        ["\n\n", "\n", ". ", " ", ""]
    """

    DEFAULT_SEPARATORS = ["\n\n", "\n", ". ", " ", ""]

    def __init__(self, separators: list[str] | None = None, chunk_size: int = 500) -> None:
        self.separators = self.DEFAULT_SEPARATORS if separators is None else list(separators)
        self.chunk_size = chunk_size

    def chunk(self, text: str) -> list[str]:
        if not text:
            return []

        if len(text) <= self.chunk_size:
            return [text]

        return self._split(text, self.separators)


    def _split(self, current_text: str, remaining_separators: list[str]) -> list[str]:
        # Base case: no more separators, return text as-is
        if not remaining_separators:
            if len(current_text) <= self.chunk_size:
                return [current_text] if current_text else []
            # Force split by character if still too large
            chunks = []
            for i in range(0, len(current_text), self.chunk_size):
                chunks.append(current_text[i:i + self.chunk_size])
            return chunks

        # Try splitting with the first separator
        separator = remaining_separators[0]
        next_separators = remaining_separators[1:]

        if separator == "":
            # Empty separator means split by character
            chunks = []
            for i in range(0, len(current_text), self.chunk_size):
                chunks.append(current_text[i:i + self.chunk_size])
            return chunks

        # Split by current separator
        parts = current_text.split(separator)

        chunks: list[str] = []
        current_chunk = ""

        for i, part in enumerate(parts):
            # Reconstruct with separator (except for last part)
            if i > 0:
                test_chunk = current_chunk + separator + part
            else:
                test_chunk = part

            if len(test_chunk) <= self.chunk_size:
                current_chunk = test_chunk
            else:
                # Current chunk is full, save it
                if current_chunk:
                    chunks.append(current_chunk)

                # If this part alone is too large, recurse with next separator
                if len(part) > self.chunk_size:
                    chunks.extend(self._split(part, next_separators))
                    current_chunk = ""
                else:
                    current_chunk = part

        # Add remaining chunk
        if current_chunk:
            chunks.append(current_chunk)

        return chunks



def _dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def compute_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """
    Compute cosine similarity between two vectors.

    cosine_similarity = dot(a, b) / (||a|| * ||b||)

    Returns 0.0 if either vector has zero magnitude.
    """
    if not vec_a or not vec_b or len(vec_a) != len(vec_b):
        return 0.0

    dot_product = _dot(vec_a, vec_b)

    # Compute magnitudes
    mag_a = math.sqrt(sum(x * x for x in vec_a))
    mag_b = math.sqrt(sum(x * x for x in vec_b))

    # Guard against zero magnitude
    if mag_a == 0.0 or mag_b == 0.0:
        return 0.0

    return dot_product / (mag_a * mag_b)



class ChunkingStrategyComparator:
    """Run all built-in chunking strategies and compare their results."""

    def compare(self, text: str, chunk_size: int = 200) -> dict:
        # Initialize all three chunkers
        fixed_chunker = FixedSizeChunker(chunk_size=chunk_size, overlap=50)
        sentence_chunker = SentenceChunker(max_sentences_per_chunk=3)
        recursive_chunker = RecursiveChunker(chunk_size=chunk_size)

        # Run each chunker
        fixed_chunks = fixed_chunker.chunk(text)
        sentence_chunks = sentence_chunker.chunk(text)
        recursive_chunks = recursive_chunker.chunk(text)

        # Compute statistics for each strategy
        def compute_stats(chunks: list[str]) -> dict:
            if not chunks:
                return {
                    "count": 0,
                    "avg_length": 0,
                    "chunks": [],
                }

            chunk_sizes = [len(c) for c in chunks]
            return {
                "count": len(chunks),
                "avg_length": sum(chunk_sizes) / len(chunks),
                "chunks": chunks,
            }

        return {
            "fixed_size": compute_stats(fixed_chunks),
            "by_sentences": compute_stats(sentence_chunks),
            "recursive": compute_stats(recursive_chunks),
        }

