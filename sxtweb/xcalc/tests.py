"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import csv
import math
from io import StringIO
from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth import SESSION_KEY, get_user_model
from django.test import Client, RequestFactory, SimpleTestCase, TestCase
from django.urls import reverse
from django.utils import timezone

from resources.models import CONE, FILTER, MACHINE
from xcalib.models import NOMINALCALIBRATION
from .forms import TreatmentPlanForm
from .plancalc import calcTxPlan
from .views_export import csv_export_page

from protocols.TG61.tests import *

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class CsvExportTests(SimpleTestCase):
    def test_mu_is_exported_with_one_decimal_place(self):
        machine = SimpleNamespace(
            MachineCode='M1',
            OutputControl='MU',
            SerialNumber='SN1',
        )
        filter_model = SimpleNamespace(
            Machine=machine,
            FilterCode='F1',
            HVLUnit='mm Al',
            Energy=100,
            Current=10,
            NominalHVL=1.0,
        )
        plan = SimpleNamespace(
            PatientId='P1',
            Filter=SimpleNamespace(Filter=filter_model),
            TxTime=13.94,
            Cone=SimpleNamespace(
                Breadth=1.0,
                Width=1.0,
                Shape='Circle',
                FSD=100.0,
                ConeCode='C1',
            ),
            CutoutRequired=False,
            CutoutShape='',
            DOB=None,
            LastName='Test',
            FirstName='Patient',
            MiddleName='',
            PlanName='CSV test',
            Fractions=1,
            TotalDose=100.0,
            CutoutWidth=0.0,
            CutoutLength=0.0,
            CutoutThickness=0.0,
            StandOut=0.0,
        )
        request = RequestFactory().get('/plan_export/csv/1')
        request.user = SimpleNamespace(is_authenticated=True)

        with patch('xcalc.views_export.get_object_or_404', return_value=plan):
            response = csv_export_page(request, '1')

        rows = list(csv.reader(StringIO(response.content.decode('utf-8'))))
        self.assertEqual(rows[1][8], '13.9')


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


class ConeGeometryTests(SimpleTestCase):
    def cone(self, shape, breadth, width):
        return CONE(Shape=shape, Breadth=breadth, Width=width)

    def test_max_dimension_uses_the_cone_shape(self):
        self.assertEqual(self.cone('Circle', 5.0, 5.0).getMaxDimension(), 5.0)
        self.assertAlmostEqual(
            self.cone('Square', 5.0, 5.0).getMaxDimension(), math.sqrt(50.0))
        self.assertAlmostEqual(
            self.cone('Rectangle', 4.0, 3.0).getMaxDimension(), 5.0)

    def test_cone_labels_preserve_fractional_dimensions(self):
        self.assertEqual(self.cone('Circle', 7.5, 7.5).getConeShape(), 'Circ 7.5')
        self.assertEqual(self.cone('Square', 7.5, 7.5).getConeShape(), '7.5x7.5')
        self.assertEqual(self.cone('Rectangle', 7.5, 3.25).getConeShape(), '7.5x3.25')

    def test_cutout_containment_uses_circle_geometry(self):
        cone = self.cone('Circle', 10.0, 10.0)
        self.assertTrue(cone.canContainCutout('Oval', 9.0, 8.0))
        self.assertFalse(cone.canContainCutout('Oval', 10.0, 1.0))
        self.assertTrue(cone.canContainCutout('Rectangle', 6.0, 7.0))
        self.assertFalse(cone.canContainCutout('Rectangle', 8.0, 8.0))

    def test_cutout_containment_uses_aligned_square_and_rectangle_axes(self):
        square = self.cone('Square', 10.0, 10.0)
        self.assertTrue(square.canContainCutout('Rectangle', 9.0, 9.0))
        self.assertFalse(square.canContainCutout('Rectangle', 10.0, 5.0))

        rectangle = self.cone('Rectangle', 10.0, 6.0)
        self.assertTrue(rectangle.canContainCutout('Rectangle', 5.0, 9.0))
        self.assertFalse(rectangle.canContainCutout('Rectangle', 9.0, 7.0))

    def test_cutout_containment_rejects_invalid_dimensions_and_shapes(self):
        cone = self.cone('Rectangle', 10.0, 6.0)
        self.assertFalse(cone.canContainCutout('Rectangle', 0.0, 1.0))
        self.assertFalse(cone.canContainCutout('Triangle', 1.0, 1.0))
        self.assertFalse(self.cone('Rectangle', 10.0, 0.0).canContainCutout(
            'Rectangle', 1.0, 1.0))


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

    def test_circle_rejects_rectangular_cutout_that_exceeds_its_diameter(self):
        form = TreatmentPlanForm(data=self.form_data(
            CutoutShape='Rectangle', CutoutLength='8.0', CutoutWidth='8.0'))

        form.is_valid()

        self.assertIn('CutoutLength', form.errors)
        self.assertIn('CutoutWidth', form.errors)

    def test_rectangle_rejects_cutout_that_exceeds_one_axis(self):
        self.cone.Shape = 'Rectangle'
        self.cone.Breadth = 10.0
        self.cone.Width = 6.0
        self.cone.save(update_fields=('Shape', 'Breadth', 'Width'))
        form = TreatmentPlanForm(data=self.form_data(
            CutoutShape='Rectangle', CutoutLength='9.0', CutoutWidth='7.0'))

        form.is_valid()

        self.assertIn('CutoutLength', form.errors)
        self.assertIn('CutoutWidth', form.errors)

    def test_square_accepts_aligned_cutout_that_fits_each_axis(self):
        self.cone.Shape = 'Square'
        self.cone.Breadth = 10.0
        self.cone.Width = 10.0
        self.cone.save(update_fields=('Shape', 'Breadth', 'Width'))
        form = TreatmentPlanForm(data=self.form_data(
            CutoutShape='Rectangle', CutoutLength='9.0', CutoutWidth='9.0'))

        form.is_valid()

        self.assertNotIn('CutoutLength', form.errors)
        self.assertNotIn('CutoutWidth', form.errors)

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

