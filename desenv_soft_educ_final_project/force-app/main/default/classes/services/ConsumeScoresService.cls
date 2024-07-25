public with sharing class ConsumeScoresService {

    private static Decimal getAvailable(Score__c score) {
        return (score.Total__c - score.Available__c);
    }

    public static void consume(fflib_SObjectUnitOfWork uow, Player__c player, Decimal value) {
        Decimal transactionsScores = 0;

        List<Score__c> scores = [SELECT Id, Total__c, Used__c, Available__c FROM Score__c WHERE Player__c =: player.Id ORDER BY CreatedDate];

        for(Score__c score : scores) {
            Decimal available = getAvailable(score);

            if(available == 0) {
                continue;
            }

            if(value == 0) {
                break;
            }

            if(available <= value) {
                value = value - available; 
                score.Used__c = score.Used__c + available;
            } else {
                score.Used__c = score.Used__c + value;
                value = 0;
            }

            uow.registerDirty(score);
        }
    }
}