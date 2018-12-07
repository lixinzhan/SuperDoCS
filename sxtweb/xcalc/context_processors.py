from django.conf import settings

def sxt_version(context):
    return {'VERSION': settings.VERSION,
            'REVISION': settings.REVISION,
            'DB_SCHEMA': settings.DB_SCHEMA}

def sxt_copyright(context):
    return {'COPYRIGHT': settings.COPYRIGHT}

def sxt_admin(context):
    return {'ADMIN': settings.ADMINS[0][0], 'ADMINEMAIL':settings.ADMINS[0][1]}
