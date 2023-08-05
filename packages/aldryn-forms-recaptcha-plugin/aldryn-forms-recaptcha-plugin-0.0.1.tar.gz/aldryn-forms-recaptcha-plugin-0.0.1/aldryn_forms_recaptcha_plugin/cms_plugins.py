from django.utils.translation import ugettext_lazy as _
from cms.plugin_pool import plugin_pool
from django.conf import settings
from aldryn_forms.cms_plugins import Field
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3


class ReCaptchaFieldPlugin(Field):
    name = _("Invisible ReCaptcha Field")
    render_template = True
    allow_children = False
    form_field = ReCaptchaField
    form_field_widget = ReCaptchaV3

    form_field_enabled_options = [
        'error_messages',
    ]
    fieldset_general_fields = []
    fieldset_advanced_fields = []

    def get_form_field_widget_attrs(self, instance):
        return {
            'required_score': getattr(settings, 'RECAPTCHA_REQUIRED_SCORE', 0.85),
        }

    def get_error_messages(self, instance):
        return {'required': "There was a problem with ReCaptcha V3. Please contact support if this problem persists."}


plugin_pool.register_plugin(ReCaptchaFieldPlugin)
