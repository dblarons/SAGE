# -*- coding: utf-8 -*- 
<%inherit file="layout.mako"/>

<div class="col-md-3"> </div>

<div class="col-md-6">
  <h2 class="text-center">
    <a href="${request.route_url('encryption', clear_queue=True)}">Encrypt</a> | Decrypt 
  </h2>
  % if request.session.peek_flash():
    <div class="flash">
      <% flash = request.session.pop_flash() %>
      % for message in flash:
        ${message}<br>
      % endfor
    </div>
  % endif

  <div class="row">
    % if uploaded_files:
    <ul>
      % for file in uploaded_files:
      <h4><li> ${file} </li> </h4>
      % endfor
    </ul>
    % else:
    <h4> No uploaded files </h4>
    % endif
  </div>

  <div class="row">
    <form role="form" action="${request.route_url('upload_encrypted_file')}" method="post" accept-charset="utf-8" enctype="multipart/form-data">
      <div class="form-group">
        <label for="plain_text">Encrypted File</label>
        <input id="plain_text" class="form-control" name="plain_text" type="file" value="" />
        <p class="help-block">Choose a file to decrypt</p>
        <button type="submit" class="btn btn-primary">Submit</button>
      </div>
    </form>
  </div>

  <div class="row">
    <div class="col-md-6">
      <form method="get" role="form" action="${request.route_url('remove_files_decryption_page')}">
        <div class="form-group">
          <button type="submit" class="btn btn-danger">Remove</button>
        </div>
      </form>
    </div>

    <div class="col-md-6">
      <form method="get" role="form" action="${request.route_url('download_files', is_encryption=True)}">
        <div class="form-group">
          <button type="submit" class="btn btn-success">Download!</button>
        </div>
      </form>
    </div>
  </div>

</div>