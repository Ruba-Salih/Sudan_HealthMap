from django.apps import apps

def create_hospital_account(supervisor, name, state, username, password):
    Hospital = apps.get_model('hospital.Hospital')
    Hospital.objects.create(
        supervisor=supervisor,
        name=name,
        state=state,
        username=username,
        password=password
    )
