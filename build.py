"""Pack the authored chess engine into a self-extracting main.py."""
import base64, io, lzma, sys, tokenize

SRC = r"C:\Users\sandry-pc\makefun\v4.py"
DST = "main.py"
CAP = 4096
PRE = "import lzma,base64 as B;exec(lzma.decompress(B.b85decode(b'"
SUF = ("'),format=lzma.FORMAT_RAW,filters=[{'id':lzma.FILTER_LZMA2,"
       "'lc':0,'lp':0,'pb':0}]).decode())\n")
FLT = [{"id": lzma.FILTER_LZMA2, "preset": 9, "lc": 0, "lp": 0, "pb": 0}]


def minify(src):
    """Strip comments and blank lines, leaving string literals intact."""
    com, keep = {}, set()
    try:
        for t in tokenize.generate_tokens(io.StringIO(src).readline):
            if t.type == tokenize.COMMENT:
                com.setdefault(t.start[0], []).append((t.start[1], t.end[1]))
            elif t.type == tokenize.STRING and t.start[0] != t.end[0]:
                keep.update(range(t.start[0], t.end[0] + 1))
    except tokenize.TokenError:
        pass
    out = []
    for n, line in enumerate(src.splitlines(), 1):
        body = line.rstrip()
        if n not in keep:
            for a, b in sorted(com.get(n, []), reverse=True):
                body = (body[:a] + body[b:]).rstrip()
            if not body.strip():
                continue
        out.append(body)
    return "\n".join(out) + "\n"


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else SRC
    src = open(path, encoding="utf-8").read()
    mini = minify(src).encode()
    raw = lzma.compress(mini, format=lzma.FORMAT_RAW, filters=FLT)
    pay = base64.b85encode(raw)
    stub = PRE.encode() + pay + SUF.encode()
    body = stub[stub.index(b"b'") + 2:stub.index(b"'),format=")]
    assert lzma.decompress(base64.b85decode(body),
                           format=lzma.FORMAT_RAW, filters=FLT) == mini
    open(DST, "wb").write(stub)
    print("minified %d  lzma2 %d  b85 %d  main.py %d  cap %d"
          % (len(mini), len(raw), len(pay), len(stub), CAP))
    assert len(stub) <= CAP


if __name__ == "__main__":
    main()
