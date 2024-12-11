# steamOpenIDLogin
Simple function which returns auth url on 'sign in through steam' sites.

Little improved version of [pysteamauth](https://github.com/sometastycake/pysteamauth) with openid login using the returned steam cookies.

## Usage

Pip install pysteamauth.

Give username,password and url params. Openid_url ,is the url you get when clicking on "sign in through steam", should look like below.

Using the returned url from func, you can simply paste to browser or get the url with python requests which usually gives back jwt token to login the site.

```python
   from steamOpenIDLogin.py import openid_login

   async def main():
       username = "steamusername"
       password = "steampassword"
       openid_url =  "https://steamcommunity.com/openid/login?openid.ns=http://specs.openid.net/auth/2.0&openid.mode=checkid_setup&openid.return_to.."
       result = await openid_login(username,password,openid_url)
       print(result)
   asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
   asyncio.run(main()) 
```

or

```python
   from steamOpenIDLogin.py import openid_login

   username = "steamusername"
   password = "steampassword"
   openid_url =  "https://steamcommunity.com/openid/login?openid.ns=http://specs.openid.net/auth/2.0&openid.mode=checkid_setup&openid.return_to.."
   loop = asyncio.get_event_loop()
   result = loop.run_until_complete(openid_login(username,password,openid_url))  
   print(result)
       
       
```





