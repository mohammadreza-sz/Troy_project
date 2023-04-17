from djoser import email
class CustomizeActivationEmail(email.ActivationEmail):
    template_name = "account/activation.html"


class CustomizeConfirmationEmail(email.ConfirmationEmail):
    template_name = "account/confirmation.html"


class CustomizePasswordResetEmail(email.PasswordResetEmail):
    template_name = "account/password_reset.html"


class CustomizePasswordChangedConfirmationEmail(email.PasswordChangedConfirmationEmail):
    template_name = "account/password_changed_confirmation"
