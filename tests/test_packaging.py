import tarfile
from pathlib import Path

from scripts.package_submission import create_submission

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SOURCE = REPOSITORY_ROOT / "main.py"
EXPECTED_FILES = {
    "main.py": SOURCE,
    "LICENSE-APACHE-2.0.txt": REPOSITORY_ROOT / "LICENSES" / "Apache-2.0.txt",
    "THIRD_PARTY_NOTICES.txt": REPOSITORY_ROOT / "THIRD_PARTY_NOTICES.md",
}


def test_submission_archive_is_compliant_private_and_reproducible(tmp_path):
    first = tmp_path / "first.tar.gz"
    second = tmp_path / "second.tar.gz"

    create_submission(SOURCE, first)
    create_submission(SOURCE, second)

    assert first.read_bytes() == second.read_bytes()
    with tarfile.open(first, "r:gz") as archive:
        members = archive.getmembers()
        assert [member.name for member in members] == list(EXPECTED_FILES)
        for member in members:
            assert member.isfile()
            assert member.mode == 0o644
            assert member.mtime == 0
            assert member.uid == 0
            assert member.gid == 0
            assert member.uname == ""
            assert member.gname == ""
            assert (
                archive.extractfile(member).read()
                == EXPECTED_FILES[member.name].read_bytes()
            )
