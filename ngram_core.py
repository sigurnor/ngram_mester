import re
from collections import Counter
from pathlib import Path
from typing import Iterable, List, Tuple


def _tokenize_line(line: str) -> List[str]:
    """Splitter en tekstlinje i tokens med enkel, men robust tokenisering.

    Vi bruker et regulært uttrykk for å hente ut ord og enkelttegn som tegnsetting
    slik at komma, punktum og andre symboler ikke henger fast i ordet før eller
    etter. Eksempel:

    >>> _tokenize_line("I do not like this, but it is ok. Life goes on.")
    ['I', 'do', 'not', 'like', 'this', ',', 'but', 'it', 'is', 'ok', '.', 'Life', 'goes', 'on', '.']
    """

    return re.findall(r"\w+|[^\w\s]", line)


def read_tokens_from_file(path: str) -> List[str]:
    """Leser en tekstfil og returnerer en liste med tokens med enkel tokenisering."""
    tokens: List[str] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            tokens.extend(_tokenize_line(line))
    return tokens


def generate_ngrams(tokens: List[str], n: int) -> Iterable[Tuple[str, ...]]:
    """Genererer n-grammer (som tuples) fra en liste med tokens."""
    if n <= 0:
        raise ValueError("n must be >= 1")
    for i in range(len(tokens) - n + 1):
        yield tuple(tokens[i : i + n])


def count_ngrams(tokens: List[str], n: int) -> Counter:
    """Returnerer en Counter med frekvenser for alle n-grammer."""
    ngram_counter: Counter = Counter()
    for ng in generate_ngrams(tokens, n):
        ngram_counter[ng] += 1
    return ngram_counter


def write_ngrams_to_tsv(counter: Counter, out_path: str) -> None:
    """Skriver n-grammer og frekvenser til en TSV-fil."""
    with open(out_path, "w", encoding="utf-8") as f:
        for ngram, count in counter.most_common():
            ngram_str = " ".join(ngram)
            f.write(f"{ngram_str}\t{count}\n")


def write_ngrams_up_to(tokens: List[str], max_n: int, output_base: str) -> List[str]:
    """Skriver n-gramfiler for alle verdier fra 1 til og med ``max_n``.

    ``output_base`` brukes som basisnavn for filene. For eksempel vil
    ``output_base="resultat.tsv"`` generere filer som ``resultat_n1.tsv``,
    ``resultat_n2.tsv`` osv. For hver n-gram-fil opprettes det også en enkel
    tekstfil med en oppmuntrende melding.
    """

    if max_n <= 0:
        raise ValueError("max_n must be >= 1")

    base_path = Path(output_base)
    suffix = base_path.suffix or ".tsv"
    stem = base_path.stem
    output_dir = base_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    written_files: List[str] = []
    for current_n in range(1, max_n + 1):
        ngram_counts = count_ngrams(tokens, current_n)
        output_path = output_dir / f"{stem}_n{current_n}{suffix}"
        write_ngrams_to_tsv(ngram_counts, str(output_path))
        completion_note_path = output_dir / f"{stem}_n{current_n}_finished.txt"
        completion_note_path.write_text(
            "That was another n-gram finished. You are doing great.\n",
            encoding="utf-8",
        )
        written_files.append(str(output_path))

    return written_files
