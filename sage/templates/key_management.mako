# -*- coding: utf-8 -*- 
<%inherit file="layout.mako"/>

<div class="row">
  <div class="col-md-5">
    <h2> Simple Air-Gapped Encryption </h2>
    <br>
    <h4>Current Public Key: ${public_key}</h4>
    <br>
    <h4>My Private Key: ${private_key}</h4>
  </div>

  <div class="col-md-6">
    <h2 class="text-center">
      Upload Public Key
    </h2>
    <div class="row">
      <form role="form" action="${request.route_url('upload_public_key')}" method="post" accept-charset="utf-8" enctype="multipart/form-data">
        <div class="form-group">
          <label for="public_key">Public key</label>
          <input id="public_key" class="form-control" name="public_key" type="file" value="" />
          <p class="help-block">Upload the public key of the message receiver</p>
          <button type="submit" class="btn btn-primary">Upload Key</button>
        </div>
      </form>
    </div>

    <h2 class="text-center">
      Generate Personal Keys
    </h2>
    <div class="row">
      <form role="form" action="${request.route_url('generate_keys')}" method="get">
        <button type="submit" class="btn btn-primary">Generate Keys</button>
        <p class="help-block">Generate a private and public key</p>
      </form>
    </div>

    <h2 class="text-center">
      Download Personal Public Key
    </h2>
    <div class="row">
      <form role="form" action="${request.route_url('download_my_public_key')}" method="get">
        <button type="submit" class="btn btn-primary">Download My Key</button>
        <p class="help-block">Download and share your public key</p>
      </form>
    </div>
  </div>


</div>