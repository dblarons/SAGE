from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    # session factory
    session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
    # configuration setup
    config = Configurator(settings=settings, session_factory=session_factory)
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('home', '/')
    config.add_route('encryption', '/encryption/{clear_queue}')
    config.add_route('upload_text_file', '/upload_plain_text')
    config.add_route('remove_files', '/delete/{remove_encrypted}')

    config.add_route('download_files', '/download_files/{is_encryption}')

    config.add_route('decryption', '/decryption/{clear_queue}')
    config.add_route('upload_encrypted_file', '/upload_encrypted')
    config.add_route('download_text_file', '/download_plain_text')

    config.add_route('upload_public_key', '/upload_public_key')
    config.add_route('generate_keys', '/generate_keys')
    config.add_route('key_management', '/key_management')
    config.add_route('download_my_public_key', '/download_my_public_key')
    config.scan()
    return config.make_wsgi_app()
