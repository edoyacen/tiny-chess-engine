# tiny-chess-01

An authored 0x88 chess engine for make.fun tiny-chess-01. It speaks the
env's JSON `/game` and `/move` protocol and searches with alpha-beta,
a transposition table, killer moves, capture-aware move ordering,
quiescence and piece-square evaluation.

`main.py` is generated, not hand-edited. `build.py` reads the engine source,
safely strips comments and blank lines, compresses the result as a raw
LZMA2 stream (`lc=lp=pb=0`, preset 9), base85-encodes it and writes the
self-unpacking `main.py` stub. It round-trip checks the payload and asserts
the 4096-byte cap.

    python3 build.py [source.py]
