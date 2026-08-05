import tarfile
from pathlib import Path

from scripts.package_submission import create_submission

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SOURCE = REPOSITORY_ROOT / "main.py"


def test_submission_archive_is_minimal_private_and_reproducible(tmp_path):
    first = tmp_path / "first.tar.gz"
    second = tmp_path / "second.tar.gz"

    create_submission(SOURCE, first)
    create_submission(SOURCE, second)

    assert first.read_bytes() == second.read_bytes()
    with tarfile.open(first, "r:gz") as archive:
        members = archive.getmembers()
        assert len(members) == 1
        member = members[0]
        assert member.name == "main.py"
        assert member.isfile()
        assert member.mode == 0o644
        assert member.mtime == 0
        assert member.uid == 0
        assert member.gid == 0
        assert member.uname == ""
        assert member.gname == ""
        assert archive.extractfile(member).read() == SOURCE.read_bytes()
