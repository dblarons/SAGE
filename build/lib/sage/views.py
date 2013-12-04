from pyramid.response import Response
from pyramid.view import view_config
import zipfile

from scripts.encryption_algorithm import PrivateKey, PublicKey, DecryptMessage, EncryptMessage

from pyramid.httpexceptions import HTTPFound

import os

from .models import (
    DBSession
    )

@view_config(route_name='home', renderer='home.mako')
def home(request):
    here = os.path.abspath(os.path.dirname(__file__))
    public_keys = os.listdir(os.path.join(here, 'public_keys'))
    if not public_keys:
        keys = {'public_key': 'No keys'}
    elif len(public_keys) == 1:
        keys = {'public_key': public_keys[0]}
    else:
        keys = {'public_key': 'Too many keys!'}

    private_keys = os.listdir(os.path.join(here, 'my_keys/private_keys'))
    if not private_keys:
        keys['private_key'] = 'No keys'
    elif len(private_keys) == 1:
        keys['private_key'] = private_keys[0]
    else:
        keys['private_key'] = 'Too many keys!'

    return keys

####################
# Encryption Views #
####################

@view_config(route_name='encryption', renderer='encryption.mako')
def encryption_view(request):
    here = os.path.abspath(os.path.dirname(__file__))

    if not request.session.get('encrypted_files'):
        request.session['encrypted_files'] = []
        
    if not request.session.get('decrypted_files'):
        request.session['decrypted_files'] = []

    if request.matchdict.get('clear_queue') is True:
        request.session['encrypted_files'] = []
        request.session['decrypted_files'] = []
        clear_all_files(request, here)

    return {'decrypted_files': request.session['decrypted_files'],
            'encrypted_files': request.session['encrypted_files']}


@view_config(route_name='upload_text_file')
def upload_text_file(request):
    if request.POST.get('plain_text') == "":
        request.session.flash('Please select a file for upload')
        return HTTPFound(location=request.route_url('encryption', clear_queue=False))

    filename = request.POST['plain_text'].filename

    if filename in request.session['encrypted_files']:
        request.session.flash('A file with that name has already been uploaded')
        return HTTPFound(location=request.route_url('encryption', clear_queue=False))

    request.session['encrypted_files'].append(filename)

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

    encrypt_uploaded_file(here, filename)

    return HTTPFound(location=request.route_url('encryption', clear_queue=False))


@view_config(route_name='download_files')
def download_files(request):
    is_encryption = request.matchdict.get('is_encryption')
    if is_encryption == 'True':
        folder = 'encrypted_files/'
        package = 'encrypted_package.zip'
    elif is_encryption == 'False':
        folder = 'decrypted_files/'
        package = 'decrypted_package.zip'

    here = os.path.abspath(os.path.dirname(__file__))

    files_to_download = os.listdir(os.path.join(here, folder[:-1]))

    if not files_to_download:
        request.session.flash('No files have been uploaded')
        return HTTPFound(location=request.route_url('encryption', clear_queue=False))

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

def encrypt_uploaded_file(here, plain_file):
    old_path = os.path.join(here, 'tmp/', plain_file)
    new_path = os.path.join(here, 'encrypted_files/', plain_file)
    public_key = get_public_key()

    encrypted_message = EncryptMessage(public_key.n, public_key.e, old_path)
    encrypted_message.write(new_path)

def decrypt_uploaded_file(here, plain_file):
    old_path = os.path.join(here, 'tmp/', plain_file)
    new_path = os.path.join(here, 'decrypted_files/', plain_file)
    private_key = get_private_key()
    public_key = get_public_key()
    
    decrypted_message = DecryptMessage(private_key.p, private_key.q, public_key.e, old_path)
    decrypted_message.write(new_path)



####################
# Decryption Views #
####################


@view_config(route_name='decryption', renderer='decryption.mako')
def decryption_view(request):
    if request.matchdict.get('clear_queue') == 'True':
        here = os.path.abspath(os.path.dirname(__file__))
        clear_all_files(request, here)
        request.session['decrypted_files'] = []
    if not request.session.get('decrypted_files'):
        request.session['decrypted_files'] = []

    return {'decrypted_files': request.session['decrypted_files']}


@view_config(route_name='upload_encrypted_file')
def upload_encrypted_file(request):
    if request.POST.get('plain_text') == "":
        request.session.flash('Please select a file for upload')
        return HTTPFound(location=request.route_url('encryption', clear_queue=False))

    filename = request.POST['plain_text'].filename

    if filename in request.session['decrypted_files']:
        request.session.flash('A file with that name has already been uploaded')
        return HTTPFound(location=request.route_url('encryption', clear_queue=False))

    request.session['decrypted_files'].append(filename)

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

    decrypt_uploaded_file(here, filename)

    return HTTPFound(location=request.route_url('encryption', clear_queue=False))

def remove_encrypted_files(request, here):
    encrypted_files = os.listdir(os.path.join(here, 'encrypted_files'))

    for encrypted_file in encrypted_files:
        os.remove(os.path.join(here, 'encrypted_files/', encrypted_file))

def remove_decrypted_files(request, here):
    decrypted_files = os.listdir(os.path.join(here, 'decrypted_files'))

    for decrypted_file in decrypted_files:
        os.remove(os.path.join(here, 'decrypted_files/', decrypted_file))

def clear_all_files(request, here):
    tmp_files = os.listdir(os.path.join(here, 'tmp'))
    download_files = os.listdir(os.path.join(here, 'download'))

    for tmp_file in tmp_files:
        os.remove(os.path.join(here, 'tmp/', tmp_file))

    for download_file in download_files:
        os.remove(os.path.join(here, 'download/', download_file))

    remove_encrypted_files(request, here)
    remove_decrypted_files(request, here)


@view_config(route_name='remove_files')
def remove_files(request):
    here = os.path.abspath(os.path.dirname(__file__))

    if request.matchdict['remove_encrypted'] == 'True':
        remove_encrypted_files(request, here)
        request.session['encrypted_files'] = []
    elif request.matchdict['remove_encrypted'] == 'False':
        remove_decrypted_files(request, here)
        request.session['decrypted_files'] = []
    
    return HTTPFound(location=request.route_url('encryption', clear_queue=False))


@view_config(route_name='upload_public_key')
def upload_public_key(request):
    here = os.path.abspath(os.path.dirname(__file__))

    if request.POST.get('public_key') == "":
        request.session.flash('Please select a file for upload')
        return HTTPFound(location=request.route_url('key_management'))

    here = os.path.abspath(os.path.dirname(__file__))
    public_keys = os.listdir(os.path.join(here, 'public_keys'))
    if len(public_keys) > 0:
        for public_key in public_keys:
            os.remove(os.path.join(here, 'public_keys/', public_key))

    filename = request.POST['public_key'].filename

    # input_file contains the actual file data
    input_file = request.POST['public_key'].file

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

    keys_path = os.path.join(here, 'public_keys/', filename)

    os.rename(temp_file_path, keys_path)

    public_key = PublicKey()
    public_key.retrieve_stored_key(keys_path)

    return HTTPFound(location=request.route_url('key_management'))


@view_config(route_name='generate_keys')
def generate_keys(request):
    here = os.path.abspath(os.path.dirname(__file__))

    private_key_path = os.path.join(here, 'my_keys/private_keys/private_key.txt')
    public_key_path = os.path.join(here, 'my_keys/public_keys/public_key.txt')

    private_key = PrivateKey()
    private_key.new_private_key_pair()
    private_key.store_private_key(private_key_path)

    public_key = PublicKey()
    public_key.new_public_key_pair(private_key.p, private_key.q)
    public_key.store_public_key(public_key_path)

    return HTTPFound(location=request.route_url('key_management'))


# Key generation page
@view_config(route_name='key_management', renderer='key_management.mako')
def key_management(request):
    here = os.path.abspath(os.path.dirname(__file__))
    public_keys = os.listdir(os.path.join(here, 'my_keys/public_keys'))
    if not public_keys:
        keys = {'public_key': 'No keys'}
    elif len(public_keys) == 1:
        keys = {'public_key': public_keys[0]}
    else:
        keys = {'public_key': 'Too many keys!'}

    private_keys = os.listdir(os.path.join(here, 'my_keys/private_keys'))
    if not private_keys:
        keys['private_key'] = 'No keys'
    elif len(private_keys) == 1:
        keys['private_key'] = private_keys[0]
    else:
        keys['private_key'] = 'Too many keys!'

    return keys

@view_config(route_name='download_my_public_key')
def download_my_public_key(request):
    here = os.path.abspath(os.path.dirname(__file__))

    public_key_folder = os.path.join(here, 'my_keys/public_keys')

    public_keys = os.listdir(os.path.join(here, public_key_folder))

    if not public_keys:
        request.session.flash('A public key has not been generated')
        return HTTPFound(location=request.route_url('key_management'))

    response = download(os.path.join(here, public_key_folder, public_keys[0]), public_keys[0])

    return response


''' Helper methods '''

def get_public_key():
    here = os.path.abspath(os.path.dirname(__file__))
    public_keys = os.listdir(os.path.join(here, 'my_keys/public_keys'))

    if not public_keys:
        return 0
    if len(public_keys) == 1:
        public_key = PublicKey()
        public_key.retrieve_stored_key(os.path.join(here, 'my_keys/public_keys/', public_keys[0]))
        return public_key

def get_private_key():
    here = os.path.abspath(os.path.dirname(__file__))
    private_keys = os.listdir(os.path.join(here, 'my_keys/private_keys'))

    if not private_keys:
        return 0
    if len(private_keys) == 1:
        private_key = PrivateKey()
        private_key.retrieve_stored_key(os.path.join(here, 'my_keys/private_keys/', private_keys[0]))
        return private_key