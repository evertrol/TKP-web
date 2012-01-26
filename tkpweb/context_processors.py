from tkp.config import config


def dblogin(request):
    return {'dblogin': request.session.get('dblogin', config['database'])}
