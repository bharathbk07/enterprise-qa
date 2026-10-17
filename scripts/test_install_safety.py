"""Regression cases for user edits between preview, staging and publication."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from install import plan, apply
from safe_install import apply_checked, snapshot


class InstallSafetyTests(unittest.TestCase):
    def source(self, folder):
        root = Path(folder).resolve()
        path = root / 'README.md'; path.write_text('owned source')
        (root / 'distribution.json').write_text(json.dumps({'files': [
            {'path': 'README.md', 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}]}))
        return root

    def test_new_user_file_after_preflight_blocks_the_batch(self):
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source, workspace = self.source(source_dir), Path(target_dir).resolve()
            mapping, conflicts = plan(source, workspace, ['cursor']); self.assertFalse(conflicts)
            destination = workspace / '.qa-agent/README.md'; destination.parent.mkdir(); destination.write_text('new user work')
            with self.assertRaisesRegex(ValueError, 'changed after preflight'):
                apply(mapping, workspace)
            self.assertEqual(destination.read_text(), 'new user work')
            self.assertFalse((workspace / '.qa-agent/distribution.json').exists())
            self.assertFalse((workspace / '.qa-agent/.install-state.json').exists())

    def test_changed_managed_file_after_preflight_is_preserved(self):
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source, workspace = self.source(source_dir), Path(target_dir).resolve()
            mapping, _ = plan(source, workspace, ['cursor']); apply(mapping, workspace)
            mapping, _ = plan(source, workspace, ['cursor'], update_managed=True)
            destination = workspace / '.qa-agent/README.md'; destination.write_text('user edit after preview')
            with self.assertRaises(ValueError): apply(mapping, workspace)
            self.assertEqual(destination.read_text(), 'user edit after preview')

    def test_edit_during_staging_is_rechecked_before_replacement(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory).resolve(); destination = workspace / 'agent.md'; destination.write_text('original')
            expected = {destination: snapshot(workspace, destination)}
            original_mkstemp = tempfile.mkstemp
            def edit_during_stage(*args, **kwargs):
                result = original_mkstemp(*args, **kwargs)
                destination.write_text('user edit during stage')
                return result
            with patch('safe_install.tempfile.mkstemp', side_effect=edit_during_stage):
                with self.assertRaises(ValueError): apply_checked(workspace, {destination: b'update'}, expected)
            self.assertEqual(destination.read_text(), 'user edit during stage')
            self.assertFalse(list(workspace.glob('.qa-install-*')))
            self.assertFalse((workspace / '.qa-agent-install.lock').exists())

    def test_missing_destination_is_published_exclusively(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory).resolve(); destination = workspace / 'agent.md'
            expected = {destination: snapshot(workspace, destination)}
            import os
            original_link = os.link
            def user_creates_at_publication(source, target):
                Path(target).write_text('last moment user file')
                return original_link(source, target)
            with patch('safe_install.os.link', side_effect=user_creates_at_publication):
                with self.assertRaises(FileExistsError): apply_checked(workspace, {destination: b'update'}, expected)
            self.assertEqual(destination.read_text(), 'last moment user file')

    def test_source_and_receipt_changes_invalidate_plan(self):
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source, workspace = self.source(source_dir), Path(target_dir).resolve()
            mapping, _ = plan(source, workspace, ['cursor']); (source / 'README.md').write_text('changed source')
            with self.assertRaisesRegex(ValueError, 'source changed'): apply(mapping, workspace)
            self.assertFalse((workspace / '.qa-agent').exists())
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source, workspace = self.source(source_dir), Path(target_dir).resolve()
            mapping, _ = plan(source, workspace, ['cursor']); apply(mapping, workspace)
            mapping, _ = plan(source, workspace, ['cursor'])
            receipt = workspace / '.qa-agent/.install-state.json'; receipt.write_text('{"files": {}}')
            with self.assertRaises(ValueError): apply(mapping, workspace)
            self.assertEqual(receipt.read_text(), '{"files": {}}')

    def test_cooperating_installer_lock_does_not_overwrite_or_remove_existing_lock(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory).resolve(); destination = workspace / 'agent.md'
            lock = workspace / '.qa-agent-install.lock'; lock.write_text('another installer')
            with self.assertRaises(ValueError): apply_checked(workspace, {destination: b'update'}, {destination: snapshot(workspace, destination)})
            self.assertEqual(lock.read_text(), 'another installer'); self.assertFalse(destination.exists())

    def test_snapshot_used_for_conflict_check_is_not_recaptured_after_an_edit(self):
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source, workspace = self.source(source_dir), Path(target_dir).resolve()
            mapping, _ = plan(source, workspace, ['cursor']); apply(mapping, workspace)
            destination = workspace / '.qa-agent/README.md'
            def edit_after_snapshot(root, path):
                state = snapshot(root, path)
                if path == destination: destination.write_text('edit during planning')
                return state
            with patch('install.snapshot', side_effect=edit_after_snapshot):
                mapping, conflicts = plan(source, workspace, ['cursor'])
            self.assertFalse(conflicts)
            with self.assertRaises(ValueError): apply(mapping, workspace)
            self.assertEqual(destination.read_text(), 'edit during planning')
