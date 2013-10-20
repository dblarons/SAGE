# -*- coding: utf-8 -*-
<!DOCTYPE html>
<html>
<head>

  <meta charset="utf-8">
  <title>Decryption Page</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="shortcut icon" href="${request.static_url('sage:static/favicon.ico')}" />
  <link rel="stylesheet" href="${request.static_url('sage:static/vendor/bootstrap-3.0.0/css/bootstrap.min.css')}" type="text/css" media="screen" charset="utf-8" />
  <link rel="stylesheet" href="${request.static_url('sage:static/vendor/bootstrap-3.0.0/css/bootstrap-theme.min.css')}" type="text/css" media="screen" charset="utf-8" />
  <link rel="stylesheet" href="${request.static_url('sage:static/vendor/Quicksand/Quicksand-Light.ttf')}" type="text/css">
  <link rel="stylesheet" href="${request.static_url('sage:static/vendor/Quicksand/Quicksand-Regular.ttf')}" type="text/css">
  <link rel="stylesheet" href="${request.static_url('sage:static/vendor/Quicksand/Quicksand-Bold.ttf')}" type="text/css">
  <link rel="stylesheet" href="${request.static_url('sage:static/stylesheets/css/main.css')}" type="text/css">


  <!--[if lte IE 6]>
  <link rel="stylesheet" href="${request.static_url('sage:static/ie6.css')}" type="text/css" media="screen" charset="utf-8" />
  <![endif]-->
</head>
<body>

  <nav class="navbar navbar-inverse" role="navigation">
  <!-- Brand and toggle get grouped for better mobile display -->
  <div class="navbar-header">
    <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-ex1-collapse">
      <span class="sr-only">Toggle navigation</span>
      <span class="icon-bar"></span>
      <span class="icon-bar"></span>
      <span class="icon-bar"></span>
    </button>
    <a class="navbar-brand" href="${request.route_url('home')}">SAGE</a>
  </div>

  <!-- Collect the nav links, forms, and other content for toggling -->
  <div class="collapse navbar-collapse navbar-ex1-collapse">
    <ul class="nav navbar-nav">
      <li><a href="${request.route_url('encryption', clear_queue=False)}">Encryption</a></li>
      <li><a href="${request.route_url('key_management')}">Key Management</a></li>
    </ul>
    <ul class="nav navbar-nav navbar-right">
      <li><a href="#">&copy; Intelligence Iterated</a></li>
    </ul>
  </div><!-- /.navbar-collapse -->
</nav>
  
  <div id="wrap">
    <div class="container">
      % if request.session.peek_flash():
        <div class="flash">
          <% flash = request.session.pop_flash() %>
          % for message in flash:
            ${message}<br>
          % endfor
        </div>
      % endif
      ${next.body()}
    </div>

  </div>

  <script src="//code.jquery.com/jquery.js"></script>
  <script src="${request.static_url('sage:static/vendor/bootstrap-3.0.0/js/bootstrap.min.js')}"></script>
</body>
</html>
