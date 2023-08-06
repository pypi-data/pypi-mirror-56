from abc import ABC, abstractmethod

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class BaseProcessor(ABC):
    display_name = None
    accepted_currencies = None
    logo_url = None
    slug = None  # for friendly urls
    method = "GET"
    template_name = None

    def __init__(self, payment):
        self.payment = payment
        self.path = payment.backend
        self.context = {}  # can be used by Payment's customized methods.
        if self.slug is None:
            self.slug = payment.backend  # no more Mr. Friendly :P
        self.config = getattr(settings, "GETPAID_BACKEND_SETTINGS", {}).get(
            self.path, {}
        )

    def get_form(self, post_data):
        """
        Only used if the payment processor requires POST requests.
        Generates a form only containing hidden input fields.
        """
        from . import forms

        return forms.PaymentHiddenInputsPostForm(items=post_data)

    def handle_callback(self, request, *args, **kwargs):
        """
        This method handles the callback from payment broker for the purpose
        of updating the payment status.
        :return: HttpResponse instance
        """
        raise NotImplementedError

    @classmethod
    def get_display_name(cls):
        return cls.display_name

    @classmethod
    def get_accepted_currencies(cls):
        """
        Used to generate list of accepted currencies. By default returns
        ``accepted_currencies`` attribute.
        :return: List of accepted currencies, e.g. ["EUR", "USD"]
        """
        return cls.accepted_currencies

    @classmethod
    def get_logo_url(cls):
        """
        By default returns ``logo_url`` attribute.
        :return: String with url to broker's logo.
        """
        return cls.logo_url

    def fetch_status(self):
        """
        Logic for checking payment status with broker.

        Should return dict with either "amount" or "status" keys.
        If "status" key is used, it should be one of getpaid.models.PAYMENT_STATUS_CHOICES
        If both keys are present, "status" takes precedence.
        """
        raise NotImplementedError

    @abstractmethod
    def get_redirect_params(self):
        """
        Must return a dictionary containing all the data required by
        backend to process the payment in appropriate format.

        Refer to your broker's API documentation for info what keys the API
        expects and what types should the values be in.

        The Payment instance is here: self.payment
        """
        return {}

    def get_redirect_method(self):
        return self.method

    @abstractmethod
    def get_redirect_url(self):
        """
        Returns URL where the user will be redirected to complete the payment.
        This URL should be provided in your broker's documentation.
        """
        return

    def get_template_names(self, view=None):
        """
        Return a list of template names to be used for the request. Must return
        a list.
        """
        template_name = self.get_setting("POST_TEMPLATE")
        if template_name is None:
            template_name = getattr(settings, "GETPAID_POST_TEMPLATE", None)
        if template_name is None:
            template_name = self.template_name
        if template_name is None and hasattr(view, "get_template_names"):
            return view.get_template_names()
        if template_name is None:
            raise ImproperlyConfigured("Couldn't determine template name!")
        return [template_name]

    def get_setting(self, name, default=None):
        return self.config.get(name, default)
