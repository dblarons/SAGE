# -*- coding: utf-8 -*- 
<%inherit file="layout.mako"/>

<div class="col-md-5 jumbotron"> 
  <div class="row">
    <div class="col-md-12">
      <h2> Decryption </h2>
    </div>
  </div>
  <div class="row">
    <div class="col-md-12">
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
  </div>

  <div class="row">
    <form role="form" action="${request.route_url('upload_encrypted_file')}" method="post" accept-charset="utf-8" enctype="multipart/form-data">
      <div class="col-md-12">
        <div class="row">
          <div class="col-md-12">
            <h6>Encrypted File</h6>
          </div>
        </div>
        <div class="row">
          <div class="col-md-8">
              <input id="plain_text" class="form-control" name="plain_text" type="file" value="" />
              <p class="help-block">Choose a file to decrypt</p>
          </div>
          <div class="col-md-4 submit-button">
            <button type="submit" class="btn btn-primary">Submit</button>
          </div>
        </div>
      </div>
    </form>
  </div>

  <div class="row">
    <div class="col-md-3">
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

<div class="col-md-5 jumbotron">
  <div class="row">
    <div class="col-md-12">
      <h2>Encryption</h2>
    </div>
  </div>

  <div class="row">
    <div class="col-md-12">
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
  </div>

  <div class="row">
    <form role="form" action="${request.route_url('upload_text_file')}" method="post" accept-charset="utf-8" enctype="multipart/form-data">
      <div class="col-md-12">
        <div class="row">
          <div class="col-md-12">
            <h6>Text File</h6>
          </div>
        </div>
        <div class="row">
          <div class="col-md-8">
            <input id="plain_text" class="form-control" name="plain_text" type="file" value="" />
            <p class="help-block">Choose a file to encrypt</p>
          </div>
          <div class="col-md-4 submit-button">
            <button type="submit" class="btn btn-primary">Submit</button>
          </div>
        </div>
      </div>
    </form>
  </div>

  <div class="row">
    <div class="col-md-3">
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