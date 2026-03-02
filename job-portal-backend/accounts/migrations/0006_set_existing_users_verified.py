from django.db import migrations


def set_existing_users_verified(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    User.objects.all().update(is_verified=True)


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_user_is_verified_otpverification'),
    ]

    operations = [
        migrations.RunPython(set_existing_users_verified, migrations.RunPython.noop),
    ]
