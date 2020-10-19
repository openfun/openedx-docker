# Richie Configuration

## Enable TLS

If you want to use this repo with [Richie](https://github.com/openfun/richie),
[you need to enable TLS](https://richie.education/docs/quick-start#purpose)
on your development environment. Following instructions suppose that your development domain
is `edx.local.dev` and you edited your `etc/hosts` accordingly.

### How to

#### 1. Install mkcert ans its Certificate Authority

First you will need to install mkcert and its Certificate Authority.
[mkcert](https://mkcert.org/) is a little util to ease local certificate generation.

##### a. Install `mkcert` on your local machine

- [Read the doc](https://github.com/FiloSottile/mkcert)
- Linux users who do not want to use linuxbrew : [read this article](https://www.prado.lt/how-to-create-locally-trusted-ssl-certificates-in-local-development-environment-on-linux-with-mkcert).

##### b. Install Mkcert Certificate Authority

`mkcert -install`

> If you do not want to use mkcert, you can generate [CA and certificate with openssl](https://www.freecodecamp.org/news/how-to-get-https-working-on-your-local-development-environment-in-5-minutes-7af615770eec/).
> You will have to put your certificate and its key in the `docker/files/etc/nginx/ssl` directory
> and name them `edx.local.dev.pem` and `edx.local.dev.key`.

#### 2. Configure Nginx

To generate the certificate with mkcert and update Nginx configuration, run:
`bin/setup-ssl`

> If you do not want to use mkcert, read instructions above to generate OpenEdx certificate then
> run `bin/setup-ssl --no-cert` instead.

#### 3. Enable Mobile Rest API (Only for Dogwood & Eucalyptus)
If you want to use OpenEdx Dogwood or Eucalyptus releases, you have to enable
the mobile rest API to work with Richie.

`FEATURES['ENABLE_MOBILE_REST_API'] = True`

#### 4. Start OpenEdx over SSL

Finally start apps over SSL with `make run-ssl`.
You can still run apps without SSL using `make run`.
