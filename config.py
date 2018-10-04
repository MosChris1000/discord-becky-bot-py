# -*- coding: utf-8 -*-
import ast
import base64
import json
import os

# general
# ------------------------------------------------------------------------------
#ENABLE_APP = ast.literal_eval(os.environ.get('ENABLE_APP', 'True'))


GROUP_INFO_SEQUENCE = {
    "1-A": ('A4', 'B5:E6'), "1-B": ('G4', 'H5:K6'), "2-A": ('A7', 'B8:E9'), "2-B": ('G7', 'H8:K9'),
    "3-A": ('A10', 'B11:E12'), "3-B": ('G10', 'H11:K12'), "4-A": ('A13', 'B14:E15'), "4-B": ('G13', 'H14:K15'),
    "5-A": ('A16', 'B17:E18'), "5-B": ('G16', 'H17:K18'), "6-A": ('A19', 'B20:E21'), "6-B": ('G19', 'H20:K21'),
    "7-A": ('A22', 'B23:E24'), "7-B": ('G22', 'H23:K24'), "8-A": ('A25', 'B26:E27'), "8-B": ('G25', 'H26:K27'),
    "9-A": ('A28', 'B29:E30'), "9-B": ('G28', 'H29:K30'), "10-A": ('A31', 'B32:E33'), "10-B": ('G31', 'H32:K33'),
    "11-A": ('A34', 'B35:E36'), "11-B": ('G34', 'H35:K36'), "12-A": ('A37', 'B38:E39'), "12-B": ('G37', 'H38:K39'),
}  # (group_number, group_number_cell, group_cell_range)

class WorkSheetType(object):
    LukeRaidThu = u'出團表(四)'
    LukeRaidSat = u'出團表(六)'
    PlayerRoster = u'輸出職業總表'


# for discord
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')

# oauth2client config
# ------------------------------------------------------------------------------
# see: http://oauth2client.readthedocs.io/en/latest/index.html
GOOGLE_SERVICE_ACCOUNT_KEY_BASE64 = os.environ.get('GOOGLE_SERVICE_ACCOUNT_KEY_BASE64')
GOOGLE_SERVICE_ACCOUNT_KEY_JSON = base64.b64decode(GOOGLE_SERVICE_ACCOUNT_KEY_BASE64)
GOOGLE_SERVICE_ACCOUNT_KEY = json.loads(GOOGLE_SERVICE_ACCOUNT_KEY_JSON)
GOOGLE_SERVICE_ACCOUNT_CONFIG = {
    'keyfile_dict': GOOGLE_SERVICE_ACCOUNT_KEY,
    'scopes': ['https://www.googleapis.com/auth/spreadsheets',
               'https://www.googleapis.com/auth/drive']
}

# pysheet config
# ------------------------------------------------------------------------------
# ref:
GOOGLE_SPREADSHEET_KEY = os.environ.get('GOOGLE_SPREADSHEET_KEY')

# redis config
# ------------------------------------------------------------------------------
# ref:
REDIS_URL = os.environ.get('REDIS_URL_SERIA')
# SENTRY
# ------------------------------------------------------------------------------
# ref:
SENTRY_DSN = os.environ.get('SENTRY_DSN')
