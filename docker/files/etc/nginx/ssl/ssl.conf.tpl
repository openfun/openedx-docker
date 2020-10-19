  ssl_certificate     /etc/nginx/conf.d/edx.local.dev.pem;
  ssl_certificate_key /etc/nginx/conf.d/edx.local.dev.key;
  error_page 497 https://$host:$server_port$request_uri;

