public with sharing class EmailService {

    private static Map<String, Type> emailTemplatesByName = new Map<String, Type> {
        'WelcomeEmail' => WelcomeEmailTemplate.class
    };

    private static String ORG_WIDE_EMAIL_ADDRESS = 'fritschjoao@hotmail.com';

    public class EmailWrapper {
        public String email;
        public String name;

        public EmailWrapper(String email, String name) {
            this.email = email;
            this.name = name;
        }
    }

    private static OrgWideEmailAddress getOrgWideEmailAddress() {
        return [SELECT Id FROM OrgWideEmailAddress WHERE Address =: ORG_WIDE_EMAIL_ADDRESS LIMIT 1];
    }

    private static MailTemplate getEmailTemplate(String templateName) {
        if(emailTemplatesByName.containsKey(templateName)) {
            Type emailTemplate = emailTemplatesByName.get(templateName);
            return (MailTemplate)emailTemplate.newInstance();
        } else {
            throw new IllegalArgumentException('Template não encontrado: ' + templateName);
        }
    }

    public static void sendEmails(List<EmailWrapper> emailWrappers, String templateName) {
        List<Messaging.SingleEmailMessage> mails = new List<Messaging.SingleEmailMessage>();
        OrgWideEmailAddress orgWideEmailAddress = getOrgWideEmailAddress();
        MailTemplate emailTemplate = getEmailTemplate(templateName);

        for (EmailWrapper emailWrapper : emailWrappers) {
            Messaging.SingleEmailMessage mail = new Messaging.SingleEmailMessage();
            mail.setSubject(emailTemplate.getSubject());
            mail.setHtmlBody(emailTemplate.getHtmlBody(emailWrapper.name));
            mail.setToAddresses(new String[] { emailWrapper.email });
            mail.setOrgWideEmailAddressId(orgWideEmailAddress.Id);
            mails.add(mail);
        }
        
        Messaging.sendEmail(mails);
    }
}