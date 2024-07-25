from simple_salesforce import Salesforce
import json
from config import Config

sf = Salesforce(username=Config.SF_USERNAME, password=Config.SF_PASSWORD,
                security_token=Config.SF_SECURITY_TOKEN, domain=Config.SF_DOMAIN)

character_id = "a0U5Y00000xlCDKUA2"

# JSON com os diálogos
dialogs_data = [
    {
        "Order__c": 0,
        "Type__c": "Introduction",
        "Text__c": "Olá, meu nome é Jacques Necker, e fui Ministro das Finanças da França. Estou aqui para falar sobre as causas que levaram à Revolução Francesa.",
        "Character__c": character_id
    },
    {
        "Order__c": 1,
        "Type__c": "Introduction",
        "Text__c": "Antes da Revolução, a França enfrentava uma grave crise econômica. As despesas excessivas com guerras e a má administração levaram o país a uma dívida insustentável.",
        "Character__c": character_id
    },
    {
        "Order__c": 2,
        "Type__c": "Introduction",
        "Text__c": "A sociedade francesa era dividida em três estados: o clero, a nobreza e o terceiro estado. O terceiro estado, composto por camponeses, trabalhadores e a burguesia, suportava a maior parte dos impostos.",
        "Character__c": character_id
    },
    {
        "Order__c": 3,
        "Type__c": "Introduction",
        "Text__c": "Além disso, o aumento dos impostos e o custo de vida elevado geraram grande insatisfação entre o povo, especialmente entre os camponeses que enfrentavam uma enorme carga tributária.",
        "Character__c": character_id
    },
    {
        "Order__c": 4,
        "Type__c": "Conclusion",
        "Text__c": "Esses fatores criaram um ambiente de descontentamento e revolta que culminou na Revolução Francesa. Agora, vamos explorar mais sobre esses eventos respondendo a algumas perguntas.",
        "Character__c": character_id
    }
]

# Inserir diálogos no Salesforce
for dialog in dialogs_data:
    sf.Dialog__c.create(dialog)
    print(f"Dialog created: {dialog}")

print("All dialogs have been inserted successfully.")
