#import config
import pygsheets
from oauth2client.service_account import ServiceAccountCredentials
import re
import config
from datetime import datetime
import pytz
import calendar


google_credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    **config.GOOGLE_SERVICE_ACCOUNT_CONFIG)  # https://github.com/nithinmurali/pygsheets/issues/100#issuecomment-322970227
google_client = pygsheets.authorize(credentials=google_credentials)
spreadsheet = google_client.open_by_key(config.GOOGLE_SPREADSHEET_KEY)

def get_Google_sheet(group_name, weekday):
    group_cell_range = ""
    team_list = []

    weekday_mapping = {
        'Thursday': config.WorkSheetType.LukeRaidThu,
        'Saturday': config.WorkSheetType.LukeRaidSat}
    if weekday not in weekday_mapping:
        return "WeekdayError: {weekday}", None

    title = weekday_mapping[weekday]
    #print(GROUP_INFO_SEQUENCE.keys())
    if group_name in config.GROUP_INFO_SEQUENCE:
        _, group_cell_range = config.GROUP_INFO_SEQUENCE[group_name]
    
    if len(group_cell_range) <= 0:
        return "KeyError: " + group_name, None

    try:
        luke_raid_worksheet = spreadsheet.worksheet_by_title(title)
        group_matrix = luke_raid_worksheet.range(group_cell_range, returnas='matrix')
    except:
        return "SheetError: " + group_name, None
    else:
        #print(group_matrix)
        #msg = f'{group_name} 出發囉!\n'
        player_with_job_pattern = re.compile('(?P<player>.*?)\((?P<job>.*)\)')
        for team_index, team in enumerate(group_matrix, start=1):
            #msg += f'{team_index} 隊:\n'
            party_list = []
            for player_with_job in team:

                if not player_with_job:
                    continue

                prog = player_with_job_pattern.fullmatch(player_with_job)

                if prog is None:
                    #msg += f'{player_with_job} <-- 文字分析錯誤\n'
                    continue

                matched_keyword_mapping = prog.groupdict()
                player = matched_keyword_mapping['player']
                job = matched_keyword_mapping['job']
                #msg+=f'{player} 出 {job}    '
                if player != None and job != None:
                    party_list.append(matched_keyword_mapping)
            #msg += '\n'

            if len(party_list) > 0:
                team_list.append(party_list)
        #print(msg)

    return "", team_list


def get_Google_sheet_today(group_name):
    today = datetime.utcnow().replace(tzinfo=pytz.utc)
    weekday = calendar.day_name[today.weekday()]

    #print(weekday)
    return get_Google_sheet(group_name, weekday)
    
