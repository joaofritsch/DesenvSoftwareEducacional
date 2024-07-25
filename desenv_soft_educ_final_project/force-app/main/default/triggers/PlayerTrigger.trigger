trigger PlayerTrigger on Player__c (after insert) {
    fflib_SObjectDomain.triggerHandler(Players.class);
}