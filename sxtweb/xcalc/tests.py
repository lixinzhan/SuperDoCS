"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import math
from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth import SESSION_KEY, get_user_model
from django.test import Client, SimpleTestCase, TestCase
from django.urls import reverse
from django.utils import timezone

from resources.models import CONE, FILTER, MACHINE
from xcalib.models import NOMINALCALIBRATION
from .forms import TreatmentPlanForm
from .plancalc import calcTxPlan

from protocols.TG61.tests import *

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class TreatmentTimeCalculationTests(SimpleTestCase):
    def test_missing_calibration_does_not_produce_infinite_time(self):
        filter_data = SimpleNamespace(id=1, HVL=1.0, HVLUnit='mmAl', EndEffect=0.0)
        calibration_cone = SimpleNamespace(id=1, FSD=50.0)
        plan_filter = SimpleNamespace(
            id=1,
            Cone=calibration_cone,
            Filter=filter_data,
            LastModifiedDateTime=timezone.now(),
        )
        plan = SimpleNamespace(
            Filter=plan_filter,
            Cone=SimpleNamespace(
                id=2, FSD=100.0, ConeEnd='Open',
                getEquivDiameter=lambda: 5.0,
            ),
            CutoutRequired=False,
            CutoutThickness=0.0,
            StandOut=0.0,
            SpecifyROF=False,
            TargetTissue='Air',
            TotalDose=100.0,
            Fractions=1,
            TxTime=0.0,
        )
        errors = []

        with patch('xcalc.plancalc.NOMINALCALIBRATION.objects.get',
                   return_value=SimpleNamespace(DR_Air=1.0)):
            with patch('xcalc.plancalc.CALIBRATION.objects.get',
                       side_effect=LookupError):
                with patch('xcalc.plancalc.BSF_Wat.getValue', return_value=1.0):
                    with patch('xcalc.plancalc.Mu_WatAir_air.getValue', return_value=1.0):
                        calcTxPlan(plan, errors)

        self.assertTrue(errors)
        self.assertEqual(plan.TxTime, 0.0)
        self.assertTrue(math.isfinite(plan.TxTime))


class TreatmentPlanCutoutValidationTests(TestCase):
    def setUp(self):
        self.machine = MACHINE.objects.create(
            MachineCode='T1',
            MachineName='Cutout test machine',
            MachineModel='Test',
            SerialNumber='CUTOUT-TEST',
            OutputControl='min',
        )
        filter_model = FILTER.objects.create(
            FilterCode='T1',
            FilterName='Cutout test filter',
            Machine=self.machine,
            Energy=100,
            Current=10,
            NominalHVL=1,
            HVL=1,
            LastModifiedByUser='test',
        )
        self.cone = CONE.objects.create(
            ConeCode='T1',
            ConeName='Cutout test cone',
            Machine=self.machine,
            Shape='Circle',
            Breadth=10,
            Width=10,
            FSD=100,
        )
        self.calibration = NOMINALCALIBRATION.objects.create(
            NCalibName='Cutout test calibration',
            Filter=filter_model,
            Cone=self.cone,
            LastModifiedByUser='test',
        )

    def form_data(self, **overrides):
        data = {
            'Filter': str(self.calibration.pk),
            'Cone': str(self.cone.pk),
            'CutoutRequired': 'on',
            'CutoutShape': 'Oval',
            'CutoutLength': '2.0',
            'CutoutWidth': '2.0',
            'CutoutThickness': '0.2',
        }
        data.update(overrides)
        return data

    def test_invalid_cutout_dimensions_report_field_errors(self):
        for field, value in (
            ('CutoutLength', 'not-a-number'),
            ('CutoutWidth', ''),
            ('CutoutThickness', 'not-a-number'),
        ):
            with self.subTest(field=field):
                form = TreatmentPlanForm(data=self.form_data(**{field: value}))

                self.assertFalse(form.is_valid())
                self.assertIn(field, form.errors)

    def test_valid_cutout_dimensions_pass_cross_field_validation(self):
        form = TreatmentPlanForm(data=self.form_data())

        form.is_valid()

        for field in ('CutoutLength', 'CutoutWidth', 'CutoutThickness'):
            self.assertNotIn(field, form.errors)

class LogoutPageTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_superuser(
            username='logout-test-user',
            email='logout-test@example.com',
            password='test-password',
        )
        self.client = Client(enforce_csrf_checks=True)
        self.client.force_login(self.user)

    def assert_logout_form(self, response):
        self.assertContains(response, 'method="post"')
        self.assertContains(response, 'action="/logout/"')
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        self.assertContains(response, '<button type="submit"')
        self.assertIn('csrftoken', self.client.cookies)
        return self.client.cookies['csrftoken'].value

    def test_get_does_not_log_out(self):
        response = self.client.get(reverse('logout_page'))

        self.assertEqual(response.status_code, 405)
        self.assertIn(SESSION_KEY, self.client.session)

    def test_post_without_csrf_does_not_log_out(self):
        response = self.client.post(reverse('logout_page'))

        self.assertEqual(response.status_code, 403)
        self.assertIn(SESSION_KEY, self.client.session)

    def test_application_logout_form_logs_out(self):
        page = self.client.get('/help/')
        csrf_token = self.assert_logout_form(page)

        response = self.client.post(
            reverse('logout_page'),
            HTTP_X_CSRFTOKEN=csrf_token,
        )

        self.assertRedirects(response, '/')
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_admin_logout_form_logs_out(self):
        page = self.client.get(reverse('admin:index'))
        csrf_token = self.assert_logout_form(page)

        response = self.client.post(
            reverse('logout_page'),
            HTTP_X_CSRFTOKEN=csrf_token,
        )

        self.assertRedirects(response, '/')
        self.assertNotIn(SESSION_KEY, self.client.session)

