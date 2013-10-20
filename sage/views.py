from pyramid.response import Response
from pyramid.view import view_config
import zipfile

from pyramid.httpexceptions import HTTPFound

import os

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    )

@view_config(route_name='home', renderer='home.mako')
def home(request):
    return {'status': 'ok'}

####################
# Encryption Views #
####################

@view_config(route_name='encryption', renderer='encryption.mako')
def encryption_view(request):
    if request.matchdict.get('clear_queue') is True:
        request.session['uploaded_files'] = []
    if not request.session.get('uploaded_files'):
        request.session['uploaded_files'] = []

    return {'uploaded_files': request.session['uploaded_files']}


@view_config(route_name='upload_text_file')
def upload_text_file(request):
    if request.POST.get('plain_text') == "":
        request.session.flash('Please select a file for upload')
        return HTTPFound(location=request.route_url('encryption', clear_queue="False"))

    filename = request.POST['plain_text'].filename

    if filename in request.session['uploaded_files']:
        request.session.flash('A file with that name has already been uploaded')
        return HTTPFound(location=request.route_url('encryption', clear_queue=False))

    request.session['uploaded_files'].append(filename)

    # input_file contains the actual file data
    input_file = request.POST['plain_text'].file

    # TODO: Change this to a more secure path
    here = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(here, 'tmp/%s' % filename)

    temp_file_path = file_path + '~'
    output_file = open(temp_file_path, 'wb')

    input_file.seek(0)
    data = input_file.read()

    if data:
        output_file.write(data)
    else:
        output_file.write("No data") # TODO: handle this later

    output_file.close()

    os.rename(temp_file_path, file_path)

    temp_encryption_method(here, filename)

    return HTTPFound(location=request.route_url('encryption', clear_queue=False))

def remove_files(request, here):
    tmp_files = os.listdir(os.path.join(here, 'tmp'))
    encrypted_files = os.listdir(os.path.join(here, 'encrypted_files'))
    download_files = os.listdir(os.path.join(here, 'download'))
    decrypted_files = os.listdir(os.path.join(here, 'decrypted_files'))

    for tmp_file in tmp_files:
        os.remove(os.path.join(here, 'tmp/', tmp_file))

    for encrypted_file in encrypted_files:
        os.remove(os.path.join(here, 'encrypted_files/', encrypted_file))

    for download_file in download_files:
        os.remove(os.path.join(here, 'download/', download_file))

    for decrypted_file in decrypted_files:
        os.remove(os.path.join(here, 'decrypted_files/', decrypted_file))

    request.session['uploaded_files'] = []

@view_config(route_name='remove_files_encryption_page')
def remove_files_encryption_page(request):
    here = os.path.abspath(os.path.dirname(__file__))
    
    remove_files(request, here)

    return HTTPFound(location=request.route_url('encryption', clear_queue=False))


@view_config(route_name='download_files')
def download_files(request):
    is_encryption = request.matchdict.get('is_encryption')
    if is_encryption == 'True':
        folder = 'encrypted_files/'
        package = 'encrypted_package.zip'
        return_url = 'encryption'
    elif is_encryption == 'False':
        folder = 'decrypted_files/'
        package = 'decrypted_package.zip'
        return_url = 'decryption'

    here = os.path.abspath(os.path.dirname(__file__))

    files_to_download = os.listdir(os.path.join(here, folder[:-1]))

    if not files_to_download:
        request.session.flash('No files have been uploaded')
        return HTTPFound(location=request.route_url(return_url, clear_queue=False))

    if len(files_to_download) == 1:
        response = download(os.path.join(here, folder, files_to_download[0]), files_to_download[0])
    # Make zip in /download folder and download the zip
    else:
        zip = zipfile.ZipFile(os.path.join(here, 'download', package), 'w')
        for encrypted_file in files_to_download:
            zip.write(os.path.join(here, folder, encrypted_file), encrypted_file)
        zip.close

        response = download(os.path.join(here, 'download', package), package)

    return response


def download(file, filename):
    response = Response(content_type='application/force-download')
    response.content_disposition = 'attachment; filename="%s"' % filename
    response.app_iter = open(file, 'rb')
    return response

def temp_encryption_method(here, plain_file):
    old_path = os.path.join(here, 'tmp/', plain_file)
    new_path = os.path.join(here, 'encrypted_files/', plain_file)
    os.rename(old_path, new_path)

def temp_decryption_method(here, plain_file):
    old_path = os.path.join(here, 'tmp/', plain_file)
    new_path = os.path.join(here, 'decrypted_files/', plain_file)
    os.rename(old_path, new_path)



####################
# Decryption Views #
####################


@view_config(route_name='decryption', renderer='decryption.mako')
def decryption_view(request):
    if request.matchdict.get('clear_queue') == 'True':
        here = os.path.abspath(os.path.dirname(__file__))
        remove_files(request, here)
        request.session['uploaded_files'] = []
    if not request.session.get('uploaded_files'):
        request.session['uploaded_files'] = []

    return {'uploaded_files': request.session['uploaded_files']}


@view_config(route_name='upload_encrypted_file')
def upload_encrypted_file(request):
    if request.POST.get('plain_text') == "":
        request.session.flash('Please select a file for upload')
        return HTTPFound(location=request.route_url('decryption', clear_queue=False))

    filename = request.POST['plain_text'].filename

    if filename in request.session['uploaded_files']:
        request.session.flash('A file with that name has already been uploaded')
        return HTTPFound(location=request.route_url('decryption', clear_queue=False))

    request.session['uploaded_files'].append(filename)

    # input_file contains the actual file data
    input_file = request.POST['plain_text'].file

    # TODO: Change this to a more secure path
    here = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(here, 'tmp/%s' % filename)

    temp_file_path = file_path + '~'
    output_file = open(temp_file_path, 'wb')

    input_file.seek(0)
    data = input_file.read()

    if data:
        output_file.write(data)
    else:
        output_file.write("No data") # TODO: handle this later

    output_file.close()

    os.rename(temp_file_path, file_path)

    temp_decryption_method(here, filename)

    return HTTPFound(location=request.route_url('decryption', clear_queue=False))

@view_config(route_name='remove_files_decryption_page')
def remove_files_decryption_page(request):
    here = os.path.abspath(os.path.dirname(__file__))
    
    remove_files(request, here)

    return HTTPFound(location=request.route_url('decryption', clear_queue=False))

