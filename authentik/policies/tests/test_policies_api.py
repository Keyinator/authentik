"""Test policies API"""
from json import loads

from django.urls import reverse
from rest_framework.test import APITestCase

from authentik.core.tests.utils import create_test_admin_user
from authentik.policies.dummy.models import DummyPolicy


class TestPoliciesAPI(APITestCase):
    """Test policies API"""

    def setUp(self) -> None:
        super().setUp()
        self.policy = DummyPolicy.objects.create(name="dummy", result=True)
        self.user = create_test_admin_user()
        self.client.force_login(self.user)

    def test_test_call(self):
        """Test Policy's test endpoint"""
        response = self.client.post(
            reverse("authentik_api:policy-test", kwargs={"pk": self.policy.pk}),
            data={
                "user": self.user.pk,
            },
        )
        body = loads(response.content.decode())
        self.assertEqual(body["passing"], True)
        self.assertEqual(body["messages"], ["dummy"])
        self.assertEqual(body["log_messages"][0]["event"], ["Policy waiting"])

    def test_types(self):
        """Test Policy's types endpoint"""
        response = self.client.get(
            reverse("authentik_api:policy-types"),
        )
        self.assertEqual(response.status_code, 200)
