from pyramid.response import Response
from pyramid.view import view_config

from pyramid.httpexceptions import HTTPFound

import os
import uuid

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    )

@view_config(route_name='encryption', renderer='encryption.mako')
def encryption_view(request):
    return {'status': 'ok'}

@view_config(route_name='decryption', renderer='decryption.mako')
def decryption_view(request):
    return {'status': 'ok'}


@view_config(route_name='upload_text_file')
def upload_text_file(request):
    filename = request.POST['plain_text'].filename
    # input_file contains the actual file data
    input_file = request.POST['plain_text'].file

    # TODO: Change this to a more secure path
    here = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(here, 'tmp/%s.txt' % uuid.uuid4()) # '%s.txt' % uuid.uuid4())

    temp_file_path = file_path + '~'
    output_file = open(temp_file_path, 'wb')

    input_file.seek(0)
    data = input_file.read()

    if data:
        print data
        output_file.write(data)
    else:
        output_file.write("No data") # TODO: handle this later

    output_file.close()

    os.rename(temp_file_path, file_path)

    return HTTPFound(location=request.route_url('encryption'))

@view_config(route_name='download_encrypted_file')
def download_encrypted_file(request):
    here = os.path.abspath(os.path.dirname(__file__))

    tmp_files = os.listdir(os.path.join(here, 'tmp'))
    print tmp_files
    if len(tmp_files) > 1:
        return {'status': 'Error: Too many files in tmp directory'}
    
    encrypted_file = tmp_files[0]

    response = Response(content_type='application/force-download')
    response.content_disposition = 'attachment; filename="my_thing.txt"'
    response.app_iter = open(os.path.join(here, 'tmp/%s' % encrypted_file), 'rb')
    print response.content_disposition
    return response
