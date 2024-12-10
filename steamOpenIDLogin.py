from pysteamauth.auth import Steam
import http.client

#OpenID Url Like This : https://steamcommunity.com/openid/login?openid.ns=http://specs.openid.net/auth/2.0&openid.mode=checkid_setup&openid.return_to...
#Username steam_username
#Password steam_password


async def openid_login(username,password,openid_url):

    steam = Steam(
        login=username, 
        password=password,
    )
    
    await steam.login_to_steam()
    
    steam_cookies = steam._storage.cookies[username]['steamcommunity.com']
    
    boundary = "50817086733764508952000487392"
    headers = {
    'Cookie': f"sessionid={steam_cookies['sessionid']}; steamCountry={steam_cookies['steamCountry']}; timezoneOffset=10800,0; steamLoginSecure={steam_cookies['steamLoginSecure']}",

}
   
    a = http.client.HTTPSConnection("steamcommunity.com",443)
    
    a.request("GET",openid_url,headers=headers)
    nonce_resp = a.getresponse().read().decode("utf-8")
    nonce = str(nonce_resp).split('nonce"')[1].split('"')[1]
    openidparams = str(nonce_resp).split('openidparams"')[1].split('"')[1]

    headers = {
    'Content-Type': f"multipart/form-data; boundary=---------------------------{boundary}",
    'Cookie': f"sessionid={steam_cookies['sessionid']}; steamCountry={steam_cookies['steamCountry']}; timezoneOffset=10800,0; steamLoginSecure={steam_cookies['steamLoginSecure']}; sessionidSecureOpenIDNonce={nonce}",

}

    payload = (
    f'-----------------------------{boundary}\r\n'
    f'Content-Disposition: form-data; name="action"\n\n'
    "steam_openid_login\n"
    f'-----------------------------{boundary}\r\n'
    f'Content-Disposition: form-data; name="openid.mode"\n\n'
    "checkid_setup\n"
    f'-----------------------------{boundary}\r\n'
    f'Content-Disposition: form-data; name="openidparams"\n\n'
    f'{openidparams}\n'
    f'-----------------------------{boundary}\r\n'
    f'Content-Disposition: form-data; name="nonce"\n\n'
    f'{nonce}\n'
    f'-----------------------------{boundary}--\r\n'
)

    
    a = http.client.HTTPSConnection("steamcommunity.com",443)
    a.request("POST","/openid/login",body=payload,headers=headers)
    resp = a.getresponse()
    location = resp.headers.get("Location")
    return location
