#!/usr/bin/python

import os, sys, urllib, time, re, json 
from interface import log, send_update, send_msg 

# globals
config_file_path  = 'link_config.json'
log_file_path = 'chk_link_log.csv'
program = os.path.split(sys.argv[0])[1]

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        url, end_quote = None, 0
    else:
        start_quote = page.find('"', start_link)
        end_quote = page.find('"', start_quote+1)
        url = page[start_quote+1:end_quote]
    return url, end_quote

def get_links(page, source_url):
    link_url, start_from, links = 'initialised', 0, []
    base_url = source_url[:source_url.find('/',source_url.find('//')+2)]
    while link_url:
        page = page[start_from:]
        link_url, start_from = get_next_target(page)
        if link_url and len(link_url) > 3:
            if link_url[0] == '/':
                link_url = base_url+link_url
            links.append(link_url)
    return links

def check(product, url, check_string, sms_params):
    html = urllib.urlopen(url).read()
    all_links, matching_links = get_links(html, url), []
    for link in all_links:
        if re.search(check_string, link.lower()):
            matching_links.append(link)
    if len(matching_links) > 0:
        msg = ', '.join([l for l in matching_links])
        send_msg(log_file_path, program, html, msg, product, sms_params)
        return True
    else:
        log(log_file_path, program, product, 'Not available yet')
        return False

def get_config():
    config = json.load(open(config_file_path))
    delay = float(config['mins_delay'])*60
    email_params = config['email_params']
    sms_params = config['sms_params']
    products = config['products']
    return delay, email_params, sms_params, products
                                                         
def main():
    finished, loops = False, 0
    while not finished:
        loops += 1
        delay, email_params, sms_params, products = get_config()
        update_interval = 86400 / delay
        for prod_name in products.keys():
            finished = check(prod_name, 
                             products[prod_name]['url'],
                             products[prod_name]['check_string'],
                             sms_params)
            if finished: break
        if loops == 1: 
            send_update(log_file_path, program, email_params) 
        elif loops >= update_interval: 
            loops = 0
        time.sleep(delay)

if __name__ == '__main__':
    main()
