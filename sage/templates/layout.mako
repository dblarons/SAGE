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
  <link rel='stylesheet' href="http://fonts.googleapis.com/css?family=Quicksand:300,400" type='text/css'>
  <link rel="stylesheet/less" href="${request.static_url('sage:static/stylesheets/less/styles.less')}" type="text/css">
  <link rel="stylesheet/less" href="${request.static_url('sage:static/stylesheets/css/main.css')}" type="text/css">

  <!--[if lte IE 6]>
  <link rel="stylesheet" href="${request.static_url('sage:static/ie6.css')}" type="text/css" media="screen" charset="utf-8" />
  <![endif]-->
</head>
<body>
  
  <div id="wrap">
    <div class="container">
      ${next.body()}
    </div>

  </div>

  <div id="footer">
    <div class="container">&copy; Intelligence Iterated</div>
  </div>

  <script src="${request.static_url('sage:static/vendor/bootstrap-3.0.0/js/bootstrap.min.js')}"></script>
</body>
</html>
