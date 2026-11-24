#!/usr/bin/env python3
"""news-23 b112 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import hashlib
import os
import struct
import sys
import zlib

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
MIN_BYTES = 10_000
MAX_BYTES = 1_048_576


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    return 1


def validate_png(data):
    """Parse the PNG header by hand (struct): signature, IHDR, chunk walk, CRCs.

    Layout of the first 33 bytes: 8-byte signature, then the IHDR chunk
    (4-byte length, 4-byte type, 13-byte payload, 4-byte CRC).
    """
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return "bad PNG signature"
    if len(data) < 33:
        return "file too short for IHDR"
    length, ctype = struct.unpack(">I4s", data[8:16])
    if ctype != b"IHDR" or length != 13:
        return "first chunk must be a 13-byte IHDR"
    w, h, depth, ctype2, comp, filt, inter = struct.unpack(">IIBBBBB", data[16:29])
    if (w, h) != (1024, 1024):
        return "expected 1024x1024, got %dx%d" % (w, h)
    if depth != 8 or ctype2 not in (2, 6):
        return "expected 8-bit RGB/RGBA, got depth=%d type=%d" % (depth, ctype2)
    if comp != 0 or filt != 0 or inter != 0:
        return "expected compression/filter/interlace all 0"
    if zlib.crc32(b"IHDR" + data[16:29]) & 0xFFFFFFFF != struct.unpack(">I", data[29:33])[0]:
        return "IHDR CRC mismatch"
    # Walk the chunks: each IDAT non-empty, IEND last, CRCs verified.
    pos, idat_total, seen_iend = 8, 0, False
    while pos < len(data):
        if pos + 8 > len(data):
            return "truncated chunk header"
        clen, cname = struct.unpack(">I4s", data[pos:pos + 8])
        end = pos + 8 + clen + 4
        if end > len(data):
            return "truncated chunk " + cname.decode("latin1")
        if zlib.crc32(cname + data[pos + 8:pos + 8 + clen]) & 0xFFFFFFFF != struct.unpack(
                ">I", data[pos + 8 + clen:end])[0]:
            return "CRC mismatch in chunk " + cname.decode("latin1")
        if cname == b"IDAT":
            if clen == 0:
                return "empty IDAT chunk"
            idat_total += clen
        if cname == b"IEND":
            if clen != 0 or end != len(data):
                return "IEND must be a 0-byte final chunk"
            seen_iend = True
            break
        pos = end
    if not seen_iend:
        return "missing IEND chunk"
    if idat_total < 1000:
        return "IDAT payload too small"
    return None


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    repo = os.path.dirname(os.path.abspath(__file__))
    out_dir_abs = os.path.abspath(out_dir)
    if out_dir_abs == repo or out_dir_abs.startswith(repo + os.sep):
        return fail("MAKEFUN_OUTPUT_DIR must be outside the repository")
    if os.path.exists(out_dir_abs) and not os.path.isdir(out_dir_abs):
        return fail("MAKEFUN_OUTPUT_DIR is a file, not a directory")
    try:
        with open(SRC, "rb") as f:
            data = f.read()
    except OSError as e:
        return fail("cannot read entry.png: %s" % e)
    if len(data) < MIN_BYTES:
        return fail("entry.png too small: %d bytes" % len(data))
    if len(data) > MAX_BYTES:
        return fail("entry.png too large: %d bytes" % len(data))
    err = validate_png(data)
    if err:
        return fail(err)
    dest = os.path.join(out_dir_abs, "entry.png")
    if os.path.abspath(dest) == os.path.abspath(SRC):
        return fail("refusing to overwrite the source entry.png")
    os.makedirs(out_dir_abs, exist_ok=True)
    with open(dest, "wb") as f:
        f.write(data)
    with open(dest, "rb") as f:
        written = f.read()
    if written != data:
        return fail("re-read mismatch after write")
    print("entry.png sha256 %s (%d bytes)" % (hashlib.sha256(data).hexdigest(), len(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
