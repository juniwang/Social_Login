# Integrate Microsoft service with Social Login

This demo is to show how to intergrate social network account(like QQ account and weibo account) with the Misrosoft Service(like Azure Active Directory and Office 365 Service).

  - Use social network account to login in.
  - Store the relationship between social account and AAD account.


## How to deploy
> Python2 and MySQL are in need.

```sh
$ mysql -u root -p
$ create database social_login;
$ create User 'social_login'@'localhost' IDENTIFIED by 'social_login';
$ GRANT ALL on social_login.* TO 'social_login'@'localhost';
```
```sh
$ pip install -r requirement.txt
$ cd src/social_login
$ python setup_db.py
```
Then run the website.
```sh
$ python run.py
```

## Sample
* Add *open-hackathon-dev.chinacloudapp.cn* as *127.0.0.1* in file "hosts"
* Input *http://open-hackathon-dev.chinacloudapp.cn/?redirect_url=http://test.com* 
* Choose a identity provider like QQ, enter username and password.
* And it will redirect to http://b.com/?identity_provider=qq&social_access_token=XXX&aad_access_token=XXX
* Using social_access_token to get user resource from QQ and using aad_access_token to access to Microsoft Service like Office365.
