from freezegun import freeze_time
from rest_framework import status, test

from waldur_core.structure.tests import fixtures as structure_fixtures
from waldur_mastermind.common.mixins import UnitPriceMixin
from waldur_mastermind.common.utils import parse_date
from waldur_mastermind.invoices import tasks as invoices_tasks
from waldur_mastermind.marketplace_openstack import PACKAGE_TYPE

from .. import models, tasks
from . import factories, helpers


class StatsBaseTest(test.APITransactionTestCase):
    def setUp(self):
        self.fixture = structure_fixtures.ProjectFixture()
        self.customer = self.fixture.customer
        self.project = self.fixture.project

        self.category = factories.CategoryFactory()
        self.category_component = factories.CategoryComponentFactory(
            category=self.category
        )

        self.offering = factories.OfferingFactory(
            category=self.category,
            type=PACKAGE_TYPE,
            state=models.Offering.States.ACTIVE,
        )
        self.offering_component = factories.OfferingComponentFactory(
            offering=self.offering, parent=self.category_component
        )


@freeze_time('2019-01-22')
class StatsTest(StatsBaseTest):
    def setUp(self):
        super(StatsTest, self).setUp()

        self.date = parse_date('2019-01-01')

        self.plan = factories.PlanFactory(offering=self.offering)
        self.plan_component = factories.PlanComponentFactory(
            plan=self.plan, component=self.offering_component, amount=10
        )

        self.resource = factories.ResourceFactory(
            project=self.project, offering=self.offering, plan=self.plan
        )

    def test_reported_usage_is_aggregated_for_project_and_customer(self):
        # Arrange
        plan_period = models.ResourcePlanPeriod.objects.create(
            start=parse_date('2019-01-01'), resource=self.resource, plan=self.plan,
        )

        models.ComponentUsage.objects.create(
            resource=self.resource,
            component=self.offering_component,
            date=parse_date('2019-01-10'),
            billing_period=parse_date('2019-01-01'),
            plan_period=plan_period,
            usage=100,
        )

        self.new_resource = factories.ResourceFactory(
            project=self.project, offering=self.offering, plan=self.plan
        )

        new_plan_period = models.ResourcePlanPeriod.objects.create(
            start=parse_date('2019-01-01'), resource=self.new_resource, plan=self.plan,
        )

        models.ComponentUsage.objects.create(
            resource=self.resource,
            component=self.offering_component,
            date=parse_date('2019-01-20'),
            billing_period=parse_date('2019-01-01'),
            plan_period=new_plan_period,
            usage=200,
        )

        # Act
        tasks.calculate_usage_for_current_month()

        # Assert
        project_usage = (
            models.CategoryComponentUsage.objects.filter(
                scope=self.project, component=self.category_component, date=self.date
            )
            .get()
            .reported_usage
        )
        customer_usage = (
            models.CategoryComponentUsage.objects.filter(
                scope=self.customer, component=self.category_component, date=self.date
            )
            .get()
            .reported_usage
        )

        self.assertEqual(project_usage, 300)
        self.assertEqual(customer_usage, 300)

    def test_fixed_usage_is_aggregated_for_project_and_customer(self):
        # Arrange
        models.ResourcePlanPeriod.objects.create(
            resource=self.resource,
            plan=self.plan,
            start=parse_date('2019-01-10'),
            end=parse_date('2019-01-20'),
        )

        # Act
        tasks.calculate_usage_for_current_month()

        # Assert
        project_usage = (
            models.CategoryComponentUsage.objects.filter(
                scope=self.project, component=self.category_component, date=self.date,
            )
            .get()
            .fixed_usage
        )
        customer_usage = (
            models.CategoryComponentUsage.objects.filter(
                scope=self.customer, component=self.category_component, date=self.date
            )
            .get()
            .fixed_usage
        )

        self.assertEqual(project_usage, self.plan_component.amount)
        self.assertEqual(customer_usage, self.plan_component.amount)

    def test_offering_customers_stats(self):
        url = factories.OfferingFactory.get_url(self.offering, action='customers')
        self.client.force_authenticate(self.fixture.staff)
        result = self.client.get(url)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(len(result.data), 1)
        self.assertEqual(
            result.data[0]['uuid'], self.resource.project.customer.uuid.hex
        )


@freeze_time('2020-01-01')
class CostsStatsTest(StatsBaseTest):
    def setUp(self):
        super(CostsStatsTest, self).setUp()
        self.url = factories.OfferingFactory.get_url(self.offering, action='costs')

        self.plan = factories.PlanFactory(
            offering=self.offering, unit=UnitPriceMixin.Units.PER_DAY,
        )
        self.plan_component = factories.PlanComponentFactory(
            plan=self.plan, component=self.offering_component, amount=10
        )

        self.resource = factories.ResourceFactory(
            offering=self.offering,
            state=models.Resource.States.OK,
            plan=self.plan,
            limits={'cpu': 1},
        )
        invoices_tasks.create_monthly_invoices()

    def test_offering_costs_stats(self):
        with freeze_time('2020-03-01'):
            self._check_stats()

    def test_period_filter(self):
        self.client.force_authenticate(self.fixture.staff)

        result = self.client.get(self.url, {'other_param': ''})
        self.assertEqual(result.status_code, status.HTTP_200_OK)

        result = self.client.get(self.url, {'start': '2020-01'})
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_offering_costs_stats_if_resource_has_been_failed(self):
        with freeze_time('2020-03-01'):
            self.resource.state = models.Resource.States.ERRED
            self.resource.save()
            self._check_stats()

    def _check_stats(self):
        self.client.force_authenticate(self.fixture.staff)
        result = self.client.get(self.url, {'start': '2020-01', 'end': '2020-02'})
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(len(result.data), 2)
        self.assertEqual(
            result.data[0],
            {
                'tax': 0,
                'total': self.plan_component.price * 31,
                'price': self.plan_component.price * 31,
                'price_current': self.plan_component.price * 31,
                'period': '2020-01',
            },
        )

    @helpers.override_marketplace_settings(ANONYMOUS_USER_CAN_VIEW_OFFERINGS=True)
    def test_stat_methods_are_not_available_for_anonymous_users(self):
        offering_url = factories.OfferingFactory.get_url(self.offering)

        result = self.client.get(offering_url)
        self.assertEqual(result.status_code, status.HTTP_200_OK)

        offering_list_url = factories.OfferingFactory.get_list_url()
        result = self.client.get(offering_list_url)
        self.assertEqual(result.status_code, status.HTTP_200_OK)

        result = self.client.get(self.url)
        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)

        customers_url = factories.OfferingFactory.get_url(
            self.offering, action='customers'
        )
        result = self.client.get(customers_url)
        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)
