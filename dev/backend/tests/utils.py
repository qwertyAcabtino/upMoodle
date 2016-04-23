from django.core.management import call_command


def load_fixture(fixture_name):
    call_command("loaddata", "ddbb/"+fixture_name+".json", verbosity=0)
