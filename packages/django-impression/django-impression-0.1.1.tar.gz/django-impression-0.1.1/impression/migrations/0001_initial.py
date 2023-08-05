# Generated by Django 2.2.4 on 2019-10-20 02:32

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [("auth", "0011_update_proxy_permissions")]

    operations = [
        migrations.CreateModel(
            name="Distribution",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
                (
                    "distributions",
                    models.ManyToManyField(blank=True, to="impression.Distribution"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EmailAddress",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email_address", models.EmailField(max_length=254, unique=True)),
                (
                    "unsubscribed",
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        help_text="Email is unsubscribed from everything.",
                    ),
                ),
            ],
            options={"verbose_name_plural": "Email addresses"},
        ),
        migrations.CreateModel(
            name="Template",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=255,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[A-Za-z _-]+$",
                                code="invalid_name_format",
                                message="Name must only consist of letters, spaces, dashes, and underscores",
                            )
                        ],
                    ),
                ),
                ("subject", models.CharField(blank=True, max_length=255)),
                ("body", models.TextField(blank=True)),
                (
                    "extends",
                    models.ForeignKey(
                        blank=True,
                        help_text="Use this in place of the '{% extends %}' template tag.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="impression.Template",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Service",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Name must only contain lowercase letters, numbers, and underscores",
                        max_length=255,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[a-z0-9_]+$",
                                code="invalid_name_format",
                                message="Name must only consist of lowercase letters, numbers, and underscores",
                            )
                        ],
                        verbose_name="(URL Safe) Name",
                    ),
                ),
                ("is_active", models.BooleanField(db_index=True, default=True)),
                (
                    "allow_override_email_from",
                    models.BooleanField(
                        default=False,
                        help_text="Whether users of the service are allowed to override the FROM email address of the service.",
                        verbose_name="Allow override of email FROM header",
                    ),
                ),
                (
                    "allow_extra_target_email_addresses",
                    models.BooleanField(
                        default=False,
                        help_text="Whether we should accept extra email addresses in the TO/CC/BCC headers of the email message, or if we should ignore them and just use the service email configuration.",
                    ),
                ),
                (
                    "allow_json_body",
                    models.BooleanField(
                        default=True,
                        help_text="Try to decode the message body as a JSON and load into template context.",
                        verbose_name="Allow JSON body",
                    ),
                ),
                (
                    "allowed_groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Defines the groups who have access to the service.",
                        to="auth.Group",
                    ),
                ),
                (
                    "bcc_distributions",
                    models.ManyToManyField(
                        blank=True,
                        related_name="service_distribution_bcc_set",
                        to="impression.Distribution",
                        verbose_name="BCC (distribution)",
                    ),
                ),
                (
                    "bcc_email_addresses",
                    models.ManyToManyField(
                        blank=True,
                        related_name="service_email_address_bcc_set",
                        to="impression.EmailAddress",
                        verbose_name="BCC",
                    ),
                ),
                (
                    "cc_distributions",
                    models.ManyToManyField(
                        blank=True,
                        related_name="service_distribution_cc_set",
                        to="impression.Distribution",
                        verbose_name="CC (distribution)",
                    ),
                ),
                (
                    "cc_email_addresses",
                    models.ManyToManyField(
                        blank=True,
                        related_name="service_email_address_cc_set",
                        to="impression.EmailAddress",
                        verbose_name="CC",
                    ),
                ),
                (
                    "from_email_address",
                    models.ForeignKey(
                        blank=True,
                        help_text="If blank, the 'DEFAULT_FROM_EMAIL' setting will be used.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="service_email_from_set",
                        to="impression.EmailAddress",
                        verbose_name="From",
                    ),
                ),
                (
                    "template",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="impression.Template",
                    ),
                ),
                (
                    "to_distributions",
                    models.ManyToManyField(
                        blank=True,
                        related_name="service_distribution_to_set",
                        to="impression.Distribution",
                        verbose_name="To (distribution)",
                    ),
                ),
                (
                    "to_email_addresses",
                    models.ManyToManyField(
                        blank=True,
                        related_name="service_email_address_to_set",
                        to="impression.EmailAddress",
                        verbose_name="To",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("subject", models.CharField(blank=True, max_length=255)),
                (
                    "body",
                    models.TextField(
                        blank=True,
                        help_text="This can be either a single string, or an encoded JSON to pass arguments to the service.",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("ready_to_send", models.BooleanField(default=False)),
                ("sent", models.DateTimeField(blank=True, default=None, null=True)),
                (
                    "last_attempt",
                    models.DateTimeField(blank=True, default=None, null=True),
                ),
                (
                    "extra_bcc_email_addresses",
                    models.ManyToManyField(
                        blank=True,
                        related_name="message_extra_bcc_set",
                        to="impression.EmailAddress",
                        verbose_name="Extra BCC",
                    ),
                ),
                (
                    "extra_cc_email_addresses",
                    models.ManyToManyField(
                        blank=True,
                        related_name="message_extra_cc_set",
                        to="impression.EmailAddress",
                        verbose_name="Extra CC",
                    ),
                ),
                (
                    "extra_to_email_addresses",
                    models.ManyToManyField(
                        blank=True,
                        related_name="message_extra_to_set",
                        to="impression.EmailAddress",
                        verbose_name="Extra To",
                    ),
                ),
                (
                    "override_from_email_address",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="message_from_set",
                        to="impression.EmailAddress",
                        verbose_name="From (Override)",
                    ),
                ),
                (
                    "service",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="impression.Service",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="emailaddress",
            name="service_unsubscriptions",
            field=models.ManyToManyField(blank=True, to="impression.Service"),
        ),
        migrations.AddField(
            model_name="distribution",
            name="email_addresses",
            field=models.ManyToManyField(blank=True, to="impression.EmailAddress"),
        ),
    ]
