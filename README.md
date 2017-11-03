# Web Auth Checker

The Web Auth Checker security tool will check a supplied list of urls using auth options supplied to see if access is granted or not, 
this can be used to expose security holes where certain urls have not been locked down.

You would typically compile a list of urls into a file either by using a tool to spider the site or by building it via the directory
structure.

## Options

```
usage: Web Auth Checker [-h] [-v] [-t THREADS] [-c COOKIE] [-a AUTH]                         
                        [-o OUTPUT] [-r REDIRECT] [-s STATUS] [-b BODY]
                        URL_FILE  

positional arguments:   
    URL_FILE              file with urls to check  

optional arguments:   
    -h, --help            show this help message and exit   
    -v, --verbose         extra logging   
    -t THREADS, --threads THREADS                         
                          number of request threads (default 10)   
    -c COOKIE, --cookie COOKIE                         
                          cookie to use for requests   
    -a AUTH, --auth AUTH  authorization to use for requests in format user:pwd   
    -o OUTPUT, --output OUTPUT                         
                          output file (default stdout)   
    -r REDIRECT, --redirect REDIRECT                         
                          check for a redirect using status of 302 and Location                         
                          header   
    -s STATUS, --status STATUS                         
                          check for a specific HTTP status   
    -b BODY, --body BODY  check custom body content returned in response, regex                         
                          is supported
```

## Examples

```
python wac.py -r '/auth/login' site_urls.txt # anonymous test redirect
python wac.py -c 'MY_COOKIE_STRING' -r '/auth/login' site_urls.txt # cookie test redirect
python wac.py -a user:password -s 401 site_urls.txt # basic auth test 401 response
python wac.py -c 'MY_COOKIE_STRING' -b 'access denied' site_urls.txt # cookie test body has string inside
```
