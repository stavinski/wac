# Web Auth Checker

The Web Auth Checker security tool will check a supplied list of urls using auth options supplied to see if access is granted or not, 
this can be used to expose security holes where certain urls have not been locked down.

## Examples

```sh
python wac.py -c 'MY_COOKIE_STRING' -r '/auth/login' site_urls.txt
python wac.py -a user:password -s 401 site_urls.txt
python wac.py -c 'MY_COOKIE_STRING' -b 'access denied' site_urls.txt
```
