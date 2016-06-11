from plugin.core.environment import translate as _
from plugin.preferences.options.core.base import SimpleOption
from plugin.preferences.options.o_sync.constants import MODE_KEYS_BY_LABEL, MODE_LABELS_BY_KEY, MODE_IDS_BY_KEY

import logging

log = logging.getLogger(__name__)


class SyncListsPersonalOption(SimpleOption):
    key = 'sync.lists.personal.mode'
    type = 'enum'

    choices = MODE_LABELS_BY_KEY
    default = None

    group = (_('Sync - Lists (Beta)'), _('Personal'))
    label = _('Mode')
    description = _(
        "Syncing mode for personal lists *(applies to both automatic and manual syncs)*.\n"
        "\n"
        " - **Full** - Synchronize personal lists with your Trakt.tv profile\n"
        " - **Pull** - Only pull personal lists from your Trakt.tv profile\n"
        " - **Push** - *Not implemented yet*\n"
        " - **Fast Pull** - Only pull changes to personal lists from your Trakt.tv profile\n"
        " - **Disabled** - Completely disable syncing of personal lists"
    )
    order = 310

    preference = 'sync_personal_lists'

    def on_database_changed(self, value, account=None):
        if value not in MODE_IDS_BY_KEY:
            log.warn('Unknown value: %r', value)
            return

        # Map `value` to plex preference
        value = MODE_IDS_BY_KEY[value]

        # Update preference
        return self._update_preference(value, account)

    def on_plex_changed(self, value, account=None):
        if value not in MODE_KEYS_BY_LABEL:
            log.warn('Unknown value: %r', value)
            return

        # Map plex `value`
        value = MODE_KEYS_BY_LABEL[value]

        # Update database
        self.update(value, account, emit=False)
        return value


class SyncListsPersonalPlaylistsOption(SimpleOption):
    key = 'sync.lists.personal.playlists'
    type = 'boolean'

    default = True

    group = (_('Sync - Lists (Beta)'), _('Personal'))
    label = _('Create playlists in plex')
    description = _(
        "Create playlists in Plex if they don't already exist."
    )
    order = 311

    # preference = 'sync_watched'
    #
    # def on_database_changed(self, value, account=None):
    #     if value not in MODE_IDS_BY_KEY:
    #         log.warn('Unknown value: %r', value)
    #         return
    #
    #     # Map `value` to plex preference
    #     value = MODE_IDS_BY_KEY[value]
    #
    #     # Update preference
    #     return self._update_preference(value, account)
    #
    # def on_plex_changed(self, value, account=None):
    #     if value not in MODE_KEYS_BY_LABEL:
    #         log.warn('Unknown value: %r', value)
    #         return
    #
    #     # Map plex `value`
    #     value = MODE_KEYS_BY_LABEL[value]
    #
    #     # Update database
    #     self.update(value, account, emit=False)
    #     return value
