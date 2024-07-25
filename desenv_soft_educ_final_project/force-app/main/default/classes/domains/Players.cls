public with sharing class Players extends fflib_SObjectDomain {

    public Players(List<Player__c> records) {
        super(records);
    }

    public class Constructor implements fflib_SObjectDomain.IConstructable {
        public fflib_SObjectDomain construct(List<SObject> records) {
            return new Players(records);
        }
    }

    public override void onAfterInsert() {
        sendWelcomeEmail();

        fflib_SObjectUnitOfWork uow = (fflib_SObjectUnitOfWork)Application.unitOfWork.newInstance();

        createFreePlayerLevels(uow);

        uow.commitWork();
    }

    private void sendWelcomeEmail() {
        List<EmailService.EmailWrapper> emailWrappers = new List<EmailService.EmailWrapper>();

        for(Player__c player : (List<Player__c>)this.records) {
            emailWrappers.add(new EmailService.EmailWrapper(player.Email__c, player.Name));
        }

        EmailService.sendEmails(emailWrappers, 'WelcomeEmail');
    }

    private void createFreePlayerLevels(fflib_SObjectUnitOfWork uow) {
        for(Level__c level : new LevelsSelector().selectByUnlockScore(0)) {
            for(Player__c player : (List<Player__c>)this.records) {
                PlayerLevel__c playerLevel = new PlayerLevel__c();
                uow.registerRelationship(playerLevel, PlayerLevel__c.Level__c, level);
                uow.registerRelationship(playerLevel, PlayerLevel__c.Player__c, player);
                uow.registerNew(playerLevel);
            }
        }
    }
}