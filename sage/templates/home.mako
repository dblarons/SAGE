# -*- coding: utf-8 -*- 
<%inherit file="layout.mako"/>

<div class="row">
  <div class="col-md-5">
    <h1> SAGE </h1>
    <h4> Simple Air-Gapped Encryption </h4>
  </div>

  <div class="col-md-3">
    <h3><a href="${request.route_url('encryption', clear_queue=False)}">Encryption</a></h3>
  </div>
  <div class="col-md-4">
    <h3><a href="${request.route_url('decryption', clear_queue=False)}">Decryption</a></h3>
  </div>
</div>