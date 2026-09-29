from django.db import migrations


STATUS_TABLE = 'jobs_work24fetchstatus'


def _table_names(schema_editor):
    return schema_editor.connection.introspection.table_names()


def remove_default_fetch_status(apps, schema_editor):
    if schema_editor.connection.alias != 'default' or STATUS_TABLE not in _table_names(schema_editor):
        return
    schema_editor.delete_model(apps.get_model('jobs', 'Work24FetchStatus'))


def restore_default_fetch_status(apps, schema_editor):
    if schema_editor.connection.alias != 'default' or STATUS_TABLE in _table_names(schema_editor):
        return
    schema_editor.create_model(apps.get_model('jobs', 'Work24FetchStatus'))


def create_community_fetch_status(apps, schema_editor):
    if schema_editor.connection.alias != 'community' or STATUS_TABLE in _table_names(schema_editor):
        return
    schema_editor.create_model(apps.get_model('jobs', 'Work24FetchStatus'))


def remove_community_fetch_status(apps, schema_editor):
    if schema_editor.connection.alias != 'community' or STATUS_TABLE not in _table_names(schema_editor):
        return
    schema_editor.delete_model(apps.get_model('jobs', 'Work24FetchStatus'))


class Migration(migrations.Migration):
    dependencies = [('jobs', '0002_work24fetchstatus_externaljobposting')]

    operations = [
        migrations.DeleteModel(name='Application'),
        migrations.DeleteModel(name='JobPosting'),
        migrations.DeleteModel(name='PhoneIdentity'),
        migrations.DeleteModel(name='CenterContact'),
        migrations.RunPython(remove_default_fetch_status, restore_default_fetch_status),
        migrations.RunPython(
            create_community_fetch_status,
            remove_community_fetch_status,
            hints={'model_name': 'work24fetchstatus'},
        ),
    ]
