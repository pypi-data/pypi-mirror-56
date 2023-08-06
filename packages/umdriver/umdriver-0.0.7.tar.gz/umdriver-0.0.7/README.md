# UM Driver

An extension of the selenium webdriver bindings for python with U-M weblogin baked in.


## Usage

Use UMDriver as you would a normal Selenium webdriver. UMDriver provides the login method to help facilitate logging into authenticated resources. If you have two-factor authentication enabled, the login method will wait for you to authorize the login before proceeding to the next lines of code.

``` python
with UMDriver() as driver:
    driver.login(username='uniqname', password='secret')
    driver.get('https://url.for.protected.resource')
```

If you are logging into any test environments and need to authenticate with the test identity provider, you can add an optional `env` parameter to your login call:

``` python
driver.login(username, password, env='test')
```
