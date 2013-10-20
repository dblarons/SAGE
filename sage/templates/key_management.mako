# -*- coding: utf-8 -*- 
<%inherit file="layout.mako"/>

<div class="row key-management">
  <div class="col-md-5 jumbotron">
    <div class="row">
      <div class="col-md-12">
        <h3>Keychain</h3>
      </div>
    </div>
    <div class="row">
      <div class="col-md-7">
        <h4>Current Public Key: </h4>
      </div>
      <div class="col-md-5">
        <h4 id="public-key"> ${public_key} </h4>
      </div>
    </div>
    <div class="row">
      <div class="col-md-7">
        <h4>My Private Key: </h4>
      </div>
      <div class="col-md-5">
        <h4 id="private-key">${private_key}</h4>
      </div>
    </div>
  </div>

  <div class="col-md-1"></div>

  <div class="col-md-6 jumbotron">
    <div class="row">
      <div class="col-md-12">
        <h3>Upload Public Key</h3>
      </div>
    </div>
    <div class="row">
      <div class="col-md-12">
        <h5>Public key</h5>
        <form role="form" action="${request.route_url('upload_public_key')}" method="post" accept-charset="utf-8" enctype="multipart/form-data">
          <div class="row">
            <div class="col-md-6">
              <input id="public_key" class="form-control" name="public_key" type="file" value="" />
            </div>
            <div class="col-md-6 submit-button">
              <button type="submit" class="btn btn-primary">Upload Key</button>
            </div>
          </div>
          <p class="help-block">Upload the public key of the message receiver</p>
        </form>
      </div>
    </div>

    <h3>Generate Personal Keys</h3>
    <div class="row">
      <div class="col-md-12">
        <form role="form" action="${request.route_url('generate_keys')}" method="get">
          <div class="row">
            <div class="col-md-4">
              <button type="submit" class="btn btn-primary">Generate Keys</button>
            </div>
            <div class="col-md-6">
              <p class="help-block">Generate a private and public key</p>
            </div>
          </div>
        </form>
      </div>
    </div>

    <h3>Download Personal Public Key</h3>
    <div class="row">
      <div class="col-md-12">
        <form role="form" action="${request.route_url('download_my_public_key')}" method="get">
          <div class="row">
            <div class="col-md-4">
              <button type="submit" class="btn btn-primary">Download My Key</button>
            </div>
            <div class="col-md-6">
              <p class="help-block">Download and share your public key</p>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>


</div>