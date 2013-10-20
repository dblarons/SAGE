# -*- coding: utf-8 -*- 
<%inherit file="layout.mako"/>

<div class="col-md-5"> 
  <div class="row">
    <h2> Decryption </h2>
  </div>
  <div class="row">
    % if decrypted_files:
    <ul>
      % for file in decrypted_files:
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
      <form method="get" role="form" action="${request.route_url('remove_files', remove_encrypted=False)}">
        <div class="form-group">
          <button type="submit" class="btn btn-danger">Remove</button>
        </div>
      </form>
    </div>

    <div class="col-md-6">
      <form method="get" role="form" action="${request.route_url('download_files', is_encryption=False)}">
        <div class="form-group">
          <button type="submit" class="btn btn-success">Download!</button>
        </div>
      </form>
    </div>
  </div>
</div>



<div class="col-md-1"></div>

<div class="col-md-6">
  <h2 class="text-center">
    Encryption
  </h2>

  <div class="row">
    % if encrypted_files:
    <ul>
      % for file in encrypted_files:
      <h4><li> ${file} </li> </h4>
      % endfor
    </ul>
    % else:
    <h4> No uploaded files </h4>
    % endif
  </div>

  <div class="row">
    <form role="form" action="${request.route_url('upload_text_file')}" method="post" accept-charset="utf-8" enctype="multipart/form-data">
      <div class="form-group">
        <label for="plain_text">Text File</label>
        <input id="plain_text" class="form-control" name="plain_text" type="file" value="" />
        <p class="help-block">Choose a file to encrypt</p>
        <button type="submit" class="btn btn-primary">Submit</button>
      </div>
    </form>
  </div>

  <div class="row">
    <div class="col-md-6">
      <form method="get" role="form" action="${request.route_url('remove_files', remove_encrypted=True)}">
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