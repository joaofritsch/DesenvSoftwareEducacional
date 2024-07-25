from simple_salesforce import Salesforce
from config import Config

class SalesforceService:
    def __init__(self):
        self.sf = self.connect_salesforce()

    def connect_salesforce(self):
        return Salesforce(
            username=Config.SF_USERNAME,
            password=Config.SF_PASSWORD,
            security_token=Config.SF_SECURITY_TOKEN,
            domain=Config.SF_DOMAIN
        )

    def refresh_connection(self):
        self.sf = self.connect_salesforce()

    def get_player_by_username(self, username):
        self.refresh_connection()
        query = f"SELECT Id, Username__c, Password__c FROM Player__c WHERE Username__c = '{username}'"
        return self.sf.query(query)['records']

    def get_player_by_id(self, player_id):
        self.refresh_connection()
        query = f"SELECT Id, TotalScore__c FROM Player__c WHERE Id = '{player_id}'"
        return self.sf.query(query)['records']

    def get_levels(self):
        self.refresh_connection()
        query = "SELECT Id, Name, UnlockScore__c, Description__c, Character__r.Name, Difficulty__c FROM Level__c"
        return self.sf.query(query)['records']

    def get_player_level(self, player_id, level_id):
        self.refresh_connection()
        query = f"SELECT Id FROM PlayerLevel__c WHERE Player__c = '{player_id}' AND Level__c = '{level_id}'"
        return self.sf.query(query)['records']

    def get_level_details(self, level_id):
        self.refresh_connection()
        query = f"SELECT Id, Name, ImageURL__c, UnlockScore__c, Description__c, Character__c, Character__r.Name, Character__r.ImageURL__c, Difficulty__c FROM Level__c WHERE Id = '{level_id}'"
        return self.sf.query(query)['records']

    def get_character_dialogs(self, character_id):
        self.refresh_connection()
        query = f"SELECT Id, Order__c, Type__c, Text__c FROM Dialog__c WHERE Character__c = '{character_id}' ORDER BY Order__c ASC"
        return self.sf.query(query)['records']

    def get_questions(self, level_id):
        self.refresh_connection()
        query = f"SELECT Id, Text__c, Difficulty__c, Order__c FROM Question__c WHERE Level__c = '{level_id}' ORDER BY Order__c ASC"
        questions = self.sf.query(query)['records']
        for question in questions:
            question['options'] = self.get_question_options(question['Id'])
        return questions

    def get_question_options(self, question_id):
        self.refresh_connection()
        query = f"SELECT Id, Text__c, IsCorrect__c, Order__c FROM QuestionOption__c WHERE Question__c = '{question_id}' ORDER BY Order__c ASC"
        return self.sf.query(query)['records']

    def create_question_answer(self, data):
        self.refresh_connection()
        return self.sf.QuestionAnswer__c.create(data)

    def get_time_setting(self, difficulty):
        self.refresh_connection()
        query = f"SELECT Time__c FROM TimeSetting__mdt WHERE Difficulty__c = '{difficulty}' AND Type__c = 'Level'"
        return self.sf.query(query)['records']

    def get_level_setting(self, difficulty):
        self.refresh_connection()
        query = f"SELECT RightQuestions__c FROM LevelSetting__mdt WHERE Difficulty__c = '{difficulty}'"
        return self.sf.query(query)['records']

    def get_score_setting(self, difficulty, type):
        self.refresh_connection()
        query = f"SELECT Score__c FROM ScoreSetting__mdt WHERE Difficulty__c = '{difficulty}' AND Type__c = '{type}'"
        return self.sf.query(query)['records']

    def mark_level_completed(self, player_level_id):
        self.refresh_connection()
        return self.sf.PlayerLevel__c.update(player_level_id, {'Completed__c': True})

    def create_score_record(self, data):
        self.refresh_connection()
        return self.sf.Score__c.create(data)

    def create_record(self, sobject, data):
        self.refresh_connection()
        return self.sf.__getattr__(sobject).create(data)

    def update_record(self, sobject, record_id, data):
        self.refresh_connection()
        return self.sf.__getattr__(sobject).update(record_id, data)

    def query_salesforce(self, query):
        self.refresh_connection()
        return self.sf.query(query)['records']
    
    def get_customization_items(self):
        query = "SELECT Id, Name, Price__c, ImageURL__c FROM Item__c WHERE RecordType.DeveloperName = 'Customization'"
        return self.sf.query(query)['records']

    def get_player_inventory(self, player_id):
        query = f"SELECT Id, Item__r.Name, Item__r.ImageURL__c FROM PlayerItem__c WHERE Player__c = '{player_id}'"
        return self.sf.query(query)['records']

salesforce_service = SalesforceService()
