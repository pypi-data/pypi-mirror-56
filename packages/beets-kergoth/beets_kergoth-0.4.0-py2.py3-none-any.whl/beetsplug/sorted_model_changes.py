"""Intercept and block write and move operations on items."""

from __future__ import absolute_import, division, print_function

from beets import ui
from beets.plugins import BeetsPlugin


class SortedModelChangesPlugin(BeetsPlugin):
    def __init__(self):
        super(SortedModelChangesPlugin, self).__init__()
        self.register_listener('loaded', self.loaded)

    def loaded(self):
        # Monkeypatch
        self._log.warning('loaded')
        ui.show_model_changes = show_model_changes


# Copied from beets.ui
def show_model_changes(new, old=None, fields=None, always=False):
    """Given a Model object, print a list of changes from its pristine
    version stored in the database. Return a boolean indicating whether
    any changes were found.

    `old` may be the "original" object to avoid using the pristine
    version from the database. `fields` may be a list of fields to
    restrict the detection to. `always` indicates whether the object is
    always identified, regardless of whether any changes are present.
    """
    old = old or new._db._get(type(new), new.id)

    # Build up lines showing changed fields.
    changes = []
    for field in old:
        # Subset of the fields. Never show mtime.
        if field == 'mtime' or (fields and field not in fields):
            continue

        # Detect and show difference for this field.
        line = ui._field_diff(field, old, new)
        if line:
            changes.append(u'  {0}: {1}'.format(field, line))

    # New fields.
    for field in set(new) - set(old):
        if fields and field not in fields:
            continue

        changes.append(u'  {0}: {1}'.format(
            field,
            ui.colorize('text_highlight', new.formatted()[field])
        ))

    # Print changes.
    if changes or always:
        ui.print_(format(old))
    if changes:
        ui.print_(u'\n'.join(sorted(changes)))

    return bool(changes)
