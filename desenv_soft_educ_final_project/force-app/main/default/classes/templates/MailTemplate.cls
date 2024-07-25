public virtual class MailTemplate {

    protected String subject;
    protected String htmlBody;

    public virtual String getSubject() {
        return this.subject;
    }

    public virtual String getHtmlBody(String name) {
        return this.htmlBody;
    }
}