<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" xmlns:tal="http://xml.zope.org/namespaces/tal">
<head>
  <title>Encryption Page</title>
  <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
  <meta name="keywords" content="python web application" />
  <meta name="description" content="pyramid web application" />
  <link rel="shortcut icon" href="${request.static_url('sage:static/favicon.ico')}" />
  <link rel="stylesheet" href="${request.static_url('sage:static/pylons.css')}" type="text/css" media="screen" charset="utf-8" />
  <link rel="stylesheet" href="http://static.pylonsproject.org/fonts/nobile/stylesheet.css" media="screen" />
  <link rel="stylesheet" href="http://static.pylonsproject.org/fonts/neuton/stylesheet.css" media="screen" />
  <!--[if lte IE 6]>
  <link rel="stylesheet" href="${request.static_url('sage:static/ie6.css')}" type="text/css" media="screen" charset="utf-8" />
  <![endif]-->
</head>
<body>
  <div id="wrap">
    <form action="${request.route_url('upload_text_file')}" method="post" accept-charset="utf-8" enctype="multipart/form-data">

        <label for="plain_text">Text File</label>
        <input id="plain_text" name="plain_text" type="file" value="" />

        <input type="submit" value="submit" />
    </form>

    <form method="get" action="${request.route_url('download_encrypted_file')}">
      <button type="submit">Download!</button>
    </form>
  </div>
  <div id="footer">
    <div class="footer">&copy; Intelligence Iterated</div>
  </div>
</body>
</html>
