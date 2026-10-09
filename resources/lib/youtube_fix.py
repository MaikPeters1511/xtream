# -*- coding: utf-8 -*-
# Python 3
# YouTube API Key Registration via api_keys.json (no YouTube addon file modifications)

import json
import os
import sys
import xbmc
import xbmcvfs

from resources.lib.config import cConfig
from resources.lib.logger import logger

# Pfad zur api_keys.json im YouTube Addon Userdata
storedb = xbmcvfs.translatePath('special://home/userdata/addon_data/plugin.video.youtube/api_keys.json')
# Lokale (nicht eingecheckte) Datei mit den API-Keys
localkeys = os.path.join(os.path.dirname(__file__), 'youtube_keys.json')


def YT():
    try:
        apikey = cConfig('plugin.video.youtube').getSetting('youtube.api.key')
    except:
        xbmc.executebuiltin('InstallAddon(%s)' % 'plugin.video.youtube')
        sys.exit()

    # Keys werden nicht im Repository gespeichert, sondern aus einer lokalen,
    # per .gitignore ausgeschlossenen Datei gelesen (siehe youtube_keys.example.json).
    try:
        with open(localkeys, 'r') as f:
            keys = json.load(f)
        api_key = keys['api_key']
        client_id = keys['client_id']
        client_secret = keys['client_secret']
    except Exception:
        logger.info('-> [youtube_fix]: Keine lokale youtube_keys.json gefunden, ueberspringe Key-Registrierung')
        return

    if apikey == '' or apikey is None:
        # Nicht überschreiben wenn der User bereits eigene Daten konfiguriert hat
        if os.path.exists(storedb):
            return

        data = {
            "keys": {
                "developer": {},
                "personal": {
                    "api_key": api_key,
                    "client_id": client_id,
                    "client_secret": client_secret
                }
            }
        }

        try:
            os.makedirs(os.path.dirname(storedb), exist_ok=True)
            with open(storedb, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            logger.error('-> [youtube_fix]: youtube_fix: Fehler beim Schreiben der api_keys.json: %s' % str(e))