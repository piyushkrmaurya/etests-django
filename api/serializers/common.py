import razorpay
from django.conf import settings
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    StringRelatedField,
    ValidationError,
)

from api.models import TestSeriesTransaction, CreditUse, Payment, Question, Transaction

RAZORPAY_CLIENT = razorpay.Client(
    auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET)
)


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = ("transaction_id", "receipt", "user", "amount", "test_series")

    def validate_test_series(self, test_series):
        if Payment.objects.filter(
            user=self.context.get("request").user, test_series=test_series
        ):
            raise ValidationError("You have already made a payment")
        return test_series

    def validate(self, attrs):
        payment_id = attrs.get("transaction_id")
        amount = attrs.get("test_series").price * 100
        RAZORPAY_CLIENT.payment.capture(payment_id, amount=100)
        payment = RAZORPAY_CLIENT.payment.fetch(payment_id)
        if not payment["error_code"]:
            # send_email(self.context.get("request").user.email, "", "")
            attrs["verified"] = True
            return attrs
        else:
            raise ValidationError("Payment failed")


class PaymentListSerializer(ModelSerializer):
    test_series = SerializerMethodField()

    class Meta:
        model = Payment
        fields = ("test_series", "date_added")

    def get_test_series(self, obj):
        return {"id": obj.test_series.id, "name": obj.test_series.name}


class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class CreditUseSerializer(ModelSerializer):
    test = SerializerMethodField("get_test_name")

    class Meta:
        model = CreditUse
        fields = "__all__"

    def get_test_name(self, obj):
        return obj.test.name


class TestSeriesTransactionSerializer(ModelSerializer):
    test_series = StringRelatedField(many=True)

    class Meta:
        model = TestSeriesTransaction
        fields = "__all__"


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}}