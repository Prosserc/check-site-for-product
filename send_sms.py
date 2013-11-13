#!/usr/bin/python
# using http://www.txtlocal.co.uk

import urllib, urllib2

def main(msg, numbers, user, sender_name):
    """ numbers recieved as string, comma separated"""

    # https://control.txtlocal.co.uk/docs/
    hash = '6fe96c4e98a1bca5a1b11a4790ef06487079d6dc'
    test_flag = 0 # 0 for live 1 for test

    values = {'test'    : test_flag,
              'uname'   : user,
              'hash'    : hash,
              'message' : msg,
              'from'    : sender_name,
              'selectednums' : numbers }

    url = 'http://www.txtlocal.com/sendsmspost.php'

    postdata = urllib.urlencode(values)
    req = urllib2.Request(url, postdata)

    print 'Attempt to send SMS ...'

    try:
        response = urllib2.urlopen(req)
        response_url = response.geturl()
        if response_url==url:
            print 'SMS sent!\n', msg
    except urllib2.URLError, e:
        print 'Send failed!'
        print e.reason

if __name__ == '__main__':
    main()
