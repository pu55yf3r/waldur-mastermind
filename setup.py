#!/usr/bin/env python
from setuptools import setup, find_packages

# apache-libcloud is required by AWS plugin
# defusedxml is required by djangosaml2
# jira is required by JIRA plugin
# lxml is required by waldur-auth-valimo
# passlib is required by Ansible plugin
# paypalrestsdk is required by PayPal plugin
# python-digitalocean is required by DigitalOcean plugin
# python-freeipa is required by FreeIPA plugin
install_requires = [
    'ansible-waldur-module>=0.8.2',
    'apache-libcloud>=1.1.0,<2.3.0',
    'azure-mgmt-compute==5.0.0',
    'azure-mgmt-network==2.0.0',
    'azure-mgmt-rdbms==1.2.0',
    'azure-mgmt-resource==2.0.0',
    'azure-mgmt-storage==2.0.0',
    'Babel!=2.4.0,>=2.3.4',
    'Celery>=4.3.0',
    'croniter>=0.3.4',
    'defusedxml>=0.4.1',
    # 'django-admin-tools==0.8.2',  # Not published yet thus installing from GIT commit via pip
    'django-auth-ldap>=2.0.0',
    'django-defender>=0.6.2',
    'django-filter==2.2',
    'django-fluent-dashboard==1.0.1',
    'django-fsm==2.6.1',
    'django-jsoneditor>=0.0.7',
    'django-model-utils==3.2.0',
    'django-redis-cache>=2.0.0',
    'django-rest-swagger==2.1.2',
    'django-reversion==2.0.8',
    'django-taggit>=1.1.0',
    'Django>=2.2.7,<3.0',
    'djangorestframework>=3.10.2,<3.11.0',
    'djangosaml2==0.17.2',
    'docker>=4.1',
    'hiredis>=0.2.0',
    'influxdb>=4.1.0',
    'iptools>=0.6.1',
    'jira>=2.0.0',
    'lxml>=3.2.0',
    'passlib>=1.7.0',
    'paypalrestsdk>=1.10.0,<2.0',
    'pbr!=2.1.0',
    'pdfkit>=0.6.1',
    'Pillow>=6.2.0',
    'PrettyTable<0.8,>=0.7.1',
    'psycopg2-binary>=2.8.4',  # https://docs.djangoproject.com/en/2.2/ref/databases/#postgresql-notes
    'pycountry>=1.20,<2.0',
    'python-cinderclient>=3.1.0',
    'python-digitalocean>=1.5',
    'python-freeipa>=0.2.2',
    'python-glanceclient>=2.8.0',
    'python-keystoneclient>=3.13.0',
    'python-neutronclient>=6.5.0',
    'python-novaclient>=9.1.0',
    'pyvat>=1.3.1,<2.0',
    'pyvmomi>=6.7.1',
    'PyYAML>=5.1',
    'pyzabbix>=0.7.2',
    'redis>=3.2.1,<3.3',
    'requests>=2.20.0',
    'sqlparse>=0.1.11',
    'pyjwt>=1.5.3',
    'sentry-sdk>=0.9.0',
]

test_requires = [
    'ddt>=1.0.0,<1.1.0',
    'docker',
    'factory_boy==2.4.1',
    'freezegun==0.3.7',
    'mock-django==0.6.9',
    'sqlalchemy>=1.3.0',
    'responses',
]

setup(
    name='waldur-mastermind',
    version='4.3.5',
    author='OpenNode Team',
    author_email='info@opennodecloud.com',
    url='http://waldur.com',
    description='Waldur MasterMind is a hybrid cloud orchestrator.',
    license='MIT',
    long_description=open('README.rst').read(),
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),
    install_requires=install_requires,
    extras_require={
        'test': test_requires,
    },
    zip_safe=False,
    entry_points={
        'console_scripts': (
            'waldur = waldur_core.server.manage:main',
        ),
        'waldur_extensions': (
            'waldur_analytics = waldur_mastermind.analytics.extension:AnalyticsExtension',
            'waldur_ansible_estimator = waldur_mastermind.ansible_estimator.extension:AnsibleEstimatorExtension',
            'waldur_auth_bcc = waldur_auth_bcc.extension:AuthBCCExtension',
            'waldur_auth_saml2 = waldur_auth_saml2.extension:SAML2Extension',
            'waldur_auth_social = waldur_auth_social.extension:AuthSocialExtension',
            'waldur_auth_valimo = waldur_auth_valimo.extension:AuthValimoExtension',
            'waldur_aws = waldur_aws.extension:AWSExtension',
            'waldur_azure = waldur_azure.extension:AzureExtension',
            'waldur_billing = waldur_mastermind.billing.extension:BillingExtension',
            'waldur_booking = waldur_mastermind.booking.extension:BookingExtension',
            'waldur_common = waldur_ansible.common.extension:AnsibleCommonExtension',
            'waldur_cost_planning = waldur_cost_planning.extension:CostPlanningExtension',
            'waldur_digitalocean = waldur_digitalocean.extension:DigitalOceanExtension',
            'waldur_freeipa = waldur_freeipa.extension:FreeIPAExtension',
            'waldur_geo_ip = waldur_geo_ip.extension:GeoIPExtension',
            'waldur_invoices = waldur_mastermind.invoices.extension:InvoicesExtension',
            'waldur_jira = waldur_jira.extension:JiraExtension',
            'waldur_marketplace = waldur_mastermind.marketplace.extension:MarketplaceExtension',
            'waldur_marketplace_azure = waldur_mastermind.marketplace_azure.extension:MarketplaceAzureExtension',
            'waldur_marketplace_checklist = waldur_mastermind.marketplace_checklist.extension:MarketplaceChecklistExtension',
            'waldur_marketplace_openstack = waldur_mastermind.marketplace_openstack.extension:MarketplaceOpenStackExtension',
            'waldur_marketplace_rancher = waldur_mastermind.marketplace_rancher.extension:MarketplaceRancherExtension',
            'waldur_marketplace_script = waldur_mastermind.marketplace_script.extension:MarketplaceScriptExtension',
            'waldur_marketplace_slurm = waldur_mastermind.marketplace_slurm.extension:MarketplaceSlurmExtension',
            'waldur_marketplace_support = waldur_mastermind.marketplace_support.extension:MarketplaceSupportExtension',
            'waldur_marketplace_vmware = waldur_mastermind.marketplace_vmware.extension:MarketplaceVMwareExtension',
            'waldur_openstack = waldur_openstack.openstack.extension:OpenStackExtension',
            'waldur_openstack_tenant = waldur_openstack.openstack_tenant.extension:OpenStackTenantExtension',
            'waldur_packages = waldur_mastermind.packages.extension:PackagesExtension',
            'waldur_paypal = waldur_paypal.extension:PayPalExtension',
            'waldur_playbook_jobs = waldur_ansible.playbook_jobs.extension:PlaybookJobsExtension',
            'waldur_rancher = waldur_rancher.extension:RancherExtension',
            'waldur_rancher_invoices = waldur_mastermind.rancher_invoices.extension:RancherInvoicesExtension',
            'waldur_rijkscloud = waldur_rijkscloud.extension:RijkscloudExtension',
            'waldur_slurm = waldur_slurm.extension:SlurmExtension',
            'waldur_slurm_invoices = waldur_mastermind.slurm_invoices.extension:SlurmInvoicesExtension',
            'waldur_support = waldur_mastermind.support.extension:SupportExtension',
            'waldur_support_invoices = waldur_mastermind.support_invoices.extension:SupportInvoicesExtension',
            'waldur_vmware = waldur_vmware.extension:VMwareExtension',
            'waldur_zabbix = waldur_zabbix.extension:ZabbixExtension',
            'waldur_zabbix_openstack = waldur_mastermind.zabbix_openstack.extension:ZabbixOpenStackExtension',
        ),
    },
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
)
