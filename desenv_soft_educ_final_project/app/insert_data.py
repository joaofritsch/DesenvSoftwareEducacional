from simple_salesforce import Salesforce
from config import Config

# Configuração do Salesforce
sf = Salesforce(username=Config.SF_USERNAME, password=Config.SF_PASSWORD, security_token=Config.SF_SECURITY_TOKEN, domain=Config.SF_DOMAIN)

def create_level(level_data):
    return sf.Level__c.create(level_data)

def create_question(question_data):
    return sf.Question__c.create(question_data)

def create_question_option(option_data):
    return sf.QuestionOption__c.create(option_data)

def create_dialog(dialog_data):
    return sf.Dialog__c.create(dialog_data)

def insert_data():
    # Inserir o nível
    level_data = {
        'Name': 'Declaração dos Direitos do Homem e do Cidadão',
        'UnlockScore__c': 100,
        'Difficulty__c': 'Hard',
        'Description__c': 'Entenda a importância e os princípios da Declaração dos Direitos do Homem e do Cidadão.',
        'Character__c': 'a0U5Y00000xlCDUUA2',
        'ImageURL__c': 'https://ufsm-dev-ed--c.vf.force.com/resource/1721703576000/Level_DeclaracaoDireitos?',
        'Period__c' : 'a0H5Y00002IaBmUUAV'
    }
    level_result = create_level(level_data)
    level_id = level_result['id']

    # Inserir perguntas e opções
    questions = [
        {
            'Level__c': level_id,
            'Difficulty__c': 'Hard',
            'Order__c': 0,
            'Context__c': 'A Declaração dos Direitos do Homem e do Cidadão foi um documento fundamental da Revolução Francesa.',
            'Text__c': 'Qual é um dos direitos garantidos pela Declaração?',
            'options': [
                {'IsCorrect__c': True, 'Order__c': 0, 'Text__c': 'Liberdade de expressão.'},
                {'IsCorrect__c': False, 'Order__c': 1, 'Text__c': 'Direito divino dos reis.'},
                {'IsCorrect__c': False, 'Order__c': 2, 'Text__c': 'Supremacia da igreja sobre o estado.'},
                {'IsCorrect__c': False, 'Order__c': 3, 'Text__c': 'Imunidade da nobreza a impostos.'}
            ]
        },
        {
            'Level__c': level_id,
            'Difficulty__c': 'Hard',
            'Order__c': 1,
            'Context__c': 'A Declaração foi inspirada por ideias iluministas.',
            'Text__c': 'Qual princípio iluminista é refletido na Declaração?',
            'options': [
                {'IsCorrect__c': False, 'Order__c': 0, 'Text__c': 'Autoridade absoluta do rei.'},
                {'IsCorrect__c': True, 'Order__c': 1, 'Text__c': 'Igualdade perante a lei.'},
                {'IsCorrect__c': False, 'Order__c': 2, 'Text__c': 'Poder irrestrito da igreja.'},
                {'IsCorrect__c': False, 'Order__c': 3, 'Text__c': 'Direito divino.'}
            ]
        },
        {
            'Level__c': level_id,
            'Difficulty__c': 'Hard',
            'Order__c': 2,
            'Context__c': 'A Declaração foi um marco na luta pelos direitos humanos.',
            'Text__c': 'Quando foi adotada a Declaração dos Direitos do Homem e do Cidadão?',
            'options': [
                {'IsCorrect__c': True, 'Order__c': 0, 'Text__c': '1789'},
                {'IsCorrect__c': False, 'Order__c': 1, 'Text__c': '1776'},
                {'IsCorrect__c': False, 'Order__c': 2, 'Text__c': '1804'},
                {'IsCorrect__c': False, 'Order__c': 3, 'Text__c': '1799'}
            ]
        },
        {
            'Level__c': level_id,
            'Difficulty__c': 'Hard',
            'Order__c': 3,
            'Context__c': 'A Declaração influenciou muitos outros documentos de direitos humanos.',
            'Text__c': 'Qual dos seguintes documentos foi influenciado pela Declaração dos Direitos do Homem e do Cidadão?',
            'options': [
                {'IsCorrect__c': False, 'Order__c': 0, 'Text__c': 'Carta Magna'},
                {'IsCorrect__c': True, 'Order__c': 1, 'Text__c': 'Declaração Universal dos Direitos Humanos'},
                {'IsCorrect__c': False, 'Order__c': 2, 'Text__c': 'Constituição dos Estados Unidos'},
                {'IsCorrect__c': False, 'Order__c': 3, 'Text__c': 'Tratado de Versalhes'}
            ]
        },
        {
            'Level__c': level_id,
            'Difficulty__c': 'Hard',
            'Order__c': 4,
            'Context__c': 'A Declaração afirmava que todos os homens eram iguais perante a lei.',
            'Text__c': 'Qual era um dos principais objetivos da Declaração?',
            'options': [
                {'IsCorrect__c': True, 'Order__c': 0, 'Text__c': 'Abolir os privilégios da nobreza.'},
                {'IsCorrect__c': False, 'Order__c': 1, 'Text__c': 'Manter o sistema feudal.'},
                {'IsCorrect__c': False, 'Order__c': 2, 'Text__c': 'Fortalecer o poder da monarquia.'},
                {'IsCorrect__c': False, 'Order__c': 3, 'Text__c': 'Garantir privilégios à igreja.'}
            ]
        }
    ]

    for question_data in questions:
        options = question_data.pop('options')
        question_result = create_question(question_data)
        question_id = question_result['id']
        
        for option in options:
            option['Question__c'] = question_id
            create_question_option(option)

    # Inserir diálogos
    dialogs = [
        {'Order__c': 0, 'Type__c': 'Introduction', 'Text__c': 'Bem-vindo ao nível sobre a Declaração dos Direitos do Homem e do Cidadão! Eu sou o Marquis de Lafayette.', 'Character__c': 'a0U5Y00000xlCDUUA2'},
        {'Order__c': 1, 'Type__c': 'Introduction', 'Text__c': 'A Declaração foi um documento fundamental que estabeleceu princípios de liberdade e igualdade.', 'Character__c': 'a0U5Y00000xlCDUUA2'},
        {'Order__c': 2, 'Type__c': 'Introduction', 'Text__c': 'Ela foi inspirada pelas ideias do Iluminismo e teve grande influência mundial.', 'Character__c': 'a0U5Y00000xlCDUUA2'},
        {'Order__c': 3, 'Type__c': 'Introduction', 'Text__c': 'Vamos começar com algumas perguntas sobre a Declaração.', 'Character__c': 'a0U5Y00000xlCDUUA2'}
    ]

    for dialog in dialogs:
        create_dialog(dialog)

if __name__ == "__main__":
    insert_data()
