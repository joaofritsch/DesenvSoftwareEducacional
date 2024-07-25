public with sharing class BuyService {

    public class Purchase {
        public Id playerId;
        public Id itemPurchasedId;
        public String itemObject;
        
        public Purchase(Id playerId, Id itemPurchasedId, String itemObject) {
            this.playerId = playerId;
            this.itemPurchasedId = itemPurchasedId;
            this.itemObject = itemObject;
        }
    }

    private static void purchaseItem(fflib_SObjectUnitOfWork uow, Player__c player, Purchase purchase) {
        Item__c item = [SELECT Id, Price__c FROM Item__c WHERE Id =: purchase.itemPurchasedId LIMIT 1];

        ConsumeScoresService.consume(uow, player, item.Price__c);

        PlayerItem__c playerItem = new PlayerItem__c();
        uow.registerRelationship(playerItem, PlayerItem__c.Item__c, item);
        uow.registerRelationship(playerItem, PlayerItem__c.Player__c, player);
        uow.registerNew(playerItem);
    }

    private static void purchaseLevel(fflib_SObjectUnitOfWork uow, Player__c player, Purchase purchase) {
        Level__c level = [SELECT Id, UnlockScore__c FROM Level__c WHERE Id =: purchase.itemPurchasedId LIMIT 1];

        ConsumeScoresService.consume(uow, player, level.UnlockScore__c);

        PlayerLevel__c playerLevel = new PlayerLevel__c();
        uow.registerRelationship(playerLevel, PlayerLevel__c.Level__c, level);
        uow.registerRelationship(playerLevel, PlayerLevel__c.Player__c, player);
        uow.registerNew(playerLevel);
    }

    public static void purchase(Purchase purchase) {
        Player__c player = [SELECT Id, TotalScore__c FROM Player__c WHERE Id =: purchase.playerId LIMIT 1];
        fflib_SObjectUnitOfWork uow = (fflib_SObjectUnitOfWork)Application.unitOfWork.newInstance();
        
        if(purchase.itemObject == 'Item__c') purchaseItem(uow, player, purchase);
        if(purchase.itemObject == 'Level__c') purchaseLevel(uow, player, purchase);
        
        uow.commitWork();
    }
}