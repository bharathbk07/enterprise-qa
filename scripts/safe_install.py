#!/usr/bin/env python3
"""Snapshot-checked local writes. Serializes cooperating installers, not arbitrary editors."""
import hashlib
import os
import stat
import tempfile
from contextlib import contextmanager
from pathlib import Path


def snapshot(workspace, path):
    workspace, path = Path(workspace).resolve(), Path(path)
    resolved = path.resolve()
    if not resolved.is_relative_to(workspace):
        raise ValueError(f'Install destination escapes workspace: {path}')
    if path.is_symlink():
        raise ValueError(f'Install file is a symlink; review it manually: {path}')
    if not path.exists():
        return {'resolved': str(resolved), 'kind': 'missing'}
    if not path.is_file():
        raise ValueError(f'Install destination is not a regular file: {path}')
    return {'resolved': str(resolved), 'kind': 'file',
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'mode': stat.S_IMODE(path.stat().st_mode)}


def verify_expected(workspace, expected):
    for path, state in expected.items():
        if snapshot(workspace, path) != state:
            raise ValueError(f'Install destination changed after preflight; re-plan: {path}')


@contextmanager
def install_lock(workspace):
    workspace = Path(workspace).resolve()
    workspace.mkdir(parents=True, exist_ok=True)
    lock = workspace / '.qa-agent-install.lock'
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise ValueError('Another install or retained install lock exists; inspect it before retrying.') from exc
    try:
        with os.fdopen(descriptor, 'w') as stream:
            stream.write(f'{os.getpid()}\n')
        yield
    finally:
        lock.unlink()


def apply_checked(workspace, writes, expected):
    """Check the entire batch, then recheck each staged replacement. Receipt should be last."""
    workspace = Path(workspace).resolve()
    if set(writes) != set(expected):
        raise ValueError('Every install write needs its original preflight snapshot.')
    with install_lock(workspace):
        verify_expected(workspace, expected)
        for destination, data in writes.items():
            destination = Path(destination)
            if not isinstance(data, bytes):
                raise ValueError('Install payloads must be reviewed bytes.')
            state = expected[destination]
            destination.parent.mkdir(parents=True, exist_ok=True)
            verify_expected(workspace, {destination: state})
            descriptor, staged_name = tempfile.mkstemp(prefix='.qa-install-', dir=destination.parent)
            staged = Path(staged_name)
            try:
                with os.fdopen(descriptor, 'wb') as stream:
                    stream.write(data)
                    stream.flush()
                    os.fsync(stream.fileno())
                os.chmod(staged, state.get('mode', 0o600))
                verify_expected(workspace, {destination: state})
                if state['kind'] == 'missing':
                    # Exclusive publication cannot overwrite a newly created user file.
                    os.link(staged, destination)
                else:
                    os.replace(staged, destination)
            finally:
                staged.unlink(missing_ok=True)
