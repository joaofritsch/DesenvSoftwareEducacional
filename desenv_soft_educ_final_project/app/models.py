from services import salesforce_service
import datetime
from config import Config

def check_user_exists(username):
    result = salesforce_service.get_player_by_username(username)
    return len(result) > 0

def create_player(name, username, password, email):
    salesforce_service.create_record('Player__c', {
        'Name': name,
        'Username__c': username,
        'Password__c': password,
        'Email__c': email,
        'Game__c': Config.SF_GAME_ID
    })

def validate_login(username, password):
    result = salesforce_service.get_player_by_username(username)
    if len(result) == 0:
        return False, "Erro: Usuário não encontrado.", None

    player = result[0]
    if player['Password__c'] != password:
        return False, "Senha incorreta.", None

    return True, "Login bem-sucedido.", player['Id']

def get_player_score(player_id):
    result = salesforce_service.get_player_by_id(player_id)
    if len(result) == 1:
        return int(result[0]['TotalScore__c'])
    return 0

def get_levels():
    return salesforce_service.get_levels()

def check_level_unlocked(player_id, level_id):
    result = salesforce_service.get_player_level(player_id, level_id)
    return len(result) > 0

def get_level_details(level_id):
    result = salesforce_service.get_level_details(level_id)
    if len(result) == 1:
        return result[0]
    return None

def get_character_dialogs(character_id):
    return salesforce_service.get_character_dialogs(character_id)

def get_questions(level_id):
    return salesforce_service.get_questions(level_id)

def create_question_answer(player_id, question_id, question_option_id, start_time, end_time, level_session_id):
    salesforce_service.create_question_answer({
        'Player__c': player_id,
        'Question__c': question_id,
        'QuestionOption__c': question_option_id,
        'Start__c': start_time if isinstance(start_time, str) else start_time.isoformat(),
        'End__c': end_time if isinstance(end_time, str) else end_time.isoformat(),
        'LevelSession__c': level_session_id
    })

def get_time_setting(level_id):
    level_details = get_level_details(level_id)
    if not level_details or 'Difficulty__c' not in level_details:
        return None
    difficulty = level_details['Difficulty__c']
    result = salesforce_service.get_time_setting(difficulty)
    if len(result) == 1:
        return result[0]['Time__c']
    return None

def get_level_setting(level_id):
    level_details = get_level_details(level_id)
    if not level_details or 'Difficulty__c' not in level_details:
        return None
    difficulty = level_details['Difficulty__c']
    result = salesforce_service.get_level_setting(difficulty)
    if len(result) == 1:
        return result[0]['RightQuestions__c']
    return None

def get_score_setting(type, level_id):
    level_details = get_level_details(level_id)
    if not level_details or 'Difficulty__c' not in level_details:
        return None
    difficulty = level_details['Difficulty__c']
    result = salesforce_service.get_score_setting(difficulty, type)
    if len(result) == 1:
        return result[0]['Score__c']
    return None

def mark_level_completed(player_id, level_id):
    result = salesforce_service.get_player_level(player_id, level_id)
    if len(result) == 1:
        player_level_id = result[0]['Id']
        salesforce_service.mark_level_completed(player_level_id)

def create_score_record(player_id, score):
    salesforce_service.create_score_record({
        'Player__c': player_id,
        'Total__c': score,
        'Used__c': 0
    })

def check_answer_correct(question_option_id):
    result = salesforce_service.query_salesforce(f"SELECT IsCorrect__c FROM QuestionOption__c WHERE Id = '{question_option_id}'")
    if len(result) == 1:
        return result[0]['IsCorrect__c']
    return False

def get_num_correct_answers(player_id, level_id, level_session_id):
    result = salesforce_service.query_salesforce(f"""
        SELECT COUNT(Id) 
        FROM QuestionAnswer__c 
        WHERE Player__c = '{player_id}' 
        AND Question__r.Level__c = '{level_id}' 
        AND LevelSession__c = '{level_session_id}'
        AND QuestionOption__r.IsCorrect__c = TRUE
    """)

    return result[0]['expr0']

def create_level_session(level_id, player_id):
    salesforce_service.create_record('LevelSession__c', {
        'Level__c': level_id,
        'Player__c': player_id
    })

def get_latest_level_session_id(level_id, player_id):
    result = salesforce_service.query_salesforce(f"""
        SELECT Id
        FROM LevelSession__c
        WHERE Level__c = '{level_id}' AND Player__c = '{player_id}'
        ORDER BY CreatedDate DESC LIMIT 1
    """)
    if len(result) == 1:
        return result[0]['Id']
    return None

def consume_scores(player_id, value):
    scores = salesforce_service.query_salesforce(f"""
        SELECT Id, Total__c, Used__c, Available__c
        FROM Score__c
        WHERE Player__c = '{player_id}'
        ORDER BY CreatedDate
    """)
    
    remaining_value = value

    for score in scores:
        available = score['Total__c'] - score['Used__c']

        if available == 0:
            continue

        if remaining_value == 0:
            break

        if available <= remaining_value:
            remaining_value -= available
            salesforce_service.update_record('Score__c', score['Id'], {'Used__c': score['Used__c'] + available})
        else:
            salesforce_service.update_record('Score__c', score['Id'], {'Used__c': score['Used__c'] + remaining_value})
            remaining_value = 0

def unlock_level(player_id, level_id, unlock_score):
    player_score = get_player_score(player_id)
    
    if player_score < unlock_score:
        return False, "Você não tem moedas suficientes para desbloquear este nível.", None

    # Consumir a pontuação necessária
    consume_scores(player_id, unlock_score)

    # Criar o registro PlayerLevel__c
    player_level = {
        'Player__c': player_id,
        'Level__c': level_id,
        'Completed__c': False
    }
    salesforce_service.create_record('PlayerLevel__c', player_level)

    return True, "Nível desbloqueado com sucesso!", player_level

def get_customization_items():
    query = "SELECT Id, Name, Price__c, ImageURL__c FROM Item__c WHERE RecordType.DeveloperName = 'Customization'"
    return salesforce_service.query_salesforce(query)

def get_player_inventory(player_id):
    query = f"""
        SELECT Id, Item__r.Name, Item__r.ImageURL__c 
        FROM PlayerItem__c 
        WHERE Player__c = '{player_id}'
    """
    return salesforce_service.query_salesforce(query)

def purchase_item(player_id, item_id, price):
    player_score = get_player_score(player_id)

    if player_score < price:
        return False, "Pontuação insuficiente para comprar o item."

    # Consumir os scores
    consume_scores(player_id, price)

    # Criar o registro PlayerItem__c
    salesforce_service.create_record('PlayerItem__c', {
        'Player__c': player_id,
        'Item__c': item_id
    })

    return True, "Item comprado com sucesso."
