public with sharing class WelcomeEmailTemplate extends MailTemplate {

    public WelcomeEmailTemplate() {
        this.subject = 'Bem-vindo(a) ao Guardiões do Tempo';
        this.htmlBody = '<html>' +
                      '<head><title>Bem-vindo(a) ao Guardiões do Tempo</title></head>' +
                      '<body>' +
                      '<div style="width: 100%; max-width: 600px; margin: 0 auto; background-color: #fff; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); overflow: hidden;">' +
                      '<div style="background-color: #8b0000; color: #fff; padding: 20px; text-align: center;">' +
                      '<img src="URL_DA_IMAGEM_DO_JOGO" alt="Guardiões do Tempo" style="max-width: 100px; margin-bottom: 10px;">' +
                      '<h1 style="margin: 0; font-family: \'DragonFableFont\', serif;">Guardiões do Tempo</h1>' +
                      '</div>' +
                      '<div style="padding: 20px;">' +
                      '<h2 style="font-family: \'DragonFableFont\', serif; color: #8b0000;">Bem-vindo(a)!</h2>' +
                      '<p>Olá, <strong>' + '{{name}}' + '</strong>!</p>' +
                      '<p>Seja bem-vindo(a) ao Guardiões do Tempo: A Missão da Revolução Francesa. Estamos entusiasmados em tê-lo(a) conosco nesta jornada épica através da história.</p>' +
                      '<p>Nossa missão é tornar o aprendizado sobre a Revolução Francesa envolvente e interativo. Prepare-se para viajar no tempo, enfrentar desafios e aprender de uma forma totalmente nova!</p>' +
                      '<p>Se precisar de ajuda ou tiver alguma dúvida, não hesite em nos contatar.</p>' +
                      '<p>Atenciosamente,<br>Equipe Guardiões do Tempo</p>' +
                      '</div>' +
                      '<div style="background-color: #8b0000; color: #fff; text-align: center; padding: 10px;">' +
                      '<p>&copy; 2024 Guardiões do Tempo. Todos os direitos reservados.</p>' +
                      '</div>' +
                      '</div>' +
                      '</body>' +
                      '</html>';
    }

    public override String getSubject() {
        return this.subject;
    }

    public override String getHtmlBody(String name) {
        return this.htmlBody.replace('{{name}}', name);
    }
}