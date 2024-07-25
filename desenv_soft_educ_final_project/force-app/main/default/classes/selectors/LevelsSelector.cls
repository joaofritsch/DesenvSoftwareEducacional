public with sharing class LevelsSelector extends fflib_SObjectSelector {
 
    public Schema.SObjectType getSObjectType() {
       return Level__c.sObjectType;
    }
  
    public List<Schema.SObjectField> getSObjectFieldList() {
        return new List<Schema.SObjectField> {
            Level__c.Id,
            Level__c.UnlockScore__c
        };
    }

    public List<Level__c> selectByUnlockScore(Integer unlockScore) {
        fflib_QueryFactory query = newQueryFactory();
        query.setCondition('UnlockScore__c =: unlockScore');

        return (List<Level__c>) Database.query( query.toSOQL() );
    }
}