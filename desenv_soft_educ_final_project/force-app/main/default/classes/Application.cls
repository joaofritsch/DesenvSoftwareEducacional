public with sharing class Application {

    public static final fflib_Application.UnitOfWorkFactory unitOfWork = new fflib_Application.UnitOfWorkFactory(
        new List<SObjectType> {
            Player__c.sObjectType,
            Level__c.sObjectType,
            PlayerLevel__c.sObjectType,
            PlayerItem__c.sObjectType,
            Score__c.sObjectType
        }
    ); 
}