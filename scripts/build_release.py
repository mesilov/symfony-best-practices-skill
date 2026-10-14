#!/usr/bin/env python3
"""Build deterministic skill archives; never execute application or network commands."""
from pathlib import Path
import argparse
import gzip
import hashlib
import io
import sys
import tarfile
import zipfile

from validate import ROOT, SKILL, validate


def build(output_dir):
    errors = validate()
    if errors: raise ValueError("; ".join(errors))
    output_dir = Path(output_dir).resolve()
    if output_dir.is_relative_to(SKILL.resolve()): raise ValueError("Output directory must be outside the skill")
    output_dir.mkdir(parents=True, exist_ok=True)
    version = (ROOT / "VERSION").read_text().strip()
    stem = f"symfony-best-practices-{version}"
    tar_path, zip_path = output_dir / f"{stem}.tar.gz", output_dir / f"{stem}.zip"
    sums_path = output_dir / "SHA256SUMS"
    for path in [tar_path, zip_path, sums_path]:
        if path.is_symlink(): raise ValueError(f"Refusing symlink output: {path}")
    files = sorted(p for p in SKILL.rglob("*") if p.is_file())
    data = io.BytesIO()
    with tarfile.open(fileobj=data, mode="w", format=tarfile.USTAR_FORMAT) as archive:
        for path in files:
            payload = path.read_bytes()
            member = tarfile.TarInfo("symfony-best-practices/" + path.relative_to(SKILL).as_posix())
            member.size, member.mode, member.mtime = len(payload), 0o644, 0
            member.uid = member.gid = 0
            member.uname = member.gname = ""
            archive.addfile(member, io.BytesIO(payload))
    with tar_path.open("wb") as stream:
        with gzip.GzipFile(fileobj=stream, filename="", mode="wb", mtime=0) as compressed:
            compressed.write(data.getvalue())
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            member = zipfile.ZipInfo("symfony-best-practices/" + path.relative_to(SKILL).as_posix(), date_time=(1980, 1, 1, 0, 0, 0))
            member.create_system = 3
            member.external_attr = 0o100644 << 16
            member.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(member, path.read_bytes())
    sums_path.write_text("".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n" for p in [tar_path, zip_path]))
    return [tar_path, zip_path, sums_path]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    try:
        for path in build(args.output_dir): print(path)
    except (ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__": sys.exit(main())
