import os, datetime as dt, send_sms, send_mail, traceback

def log(log_file_path,
        program,
        param, 
        progress, 
        exit=False):
    log_file = open(log_file_path, 'a')
    info = ', '.join((program, dt.datetime.now().strftime("%Y-%m-%d"),
                      dt.datetime.now().strftime("%H:%M:%S"),
                      param, progress, '\n'))
    log_file.write(info)
    if exit:
        sys.exit(progress)
    log_file.close()

def send_update(log_file_path,
                program,
                email_params):
    try:
        subject = 'Daily ' + program + ' update'
        sender = email_params['sender']
        enc_pwd = email_params['enc_pwd']
        recipient = email_params['recipient']
        f = open(log_file_path, 'rb')
        data = [line for line in f]
        body = str(len(data)) + \
               ' lines of data in log, here are the last 10 lines:<br/>'
        body += '<br/>'.join([line for line in data[-10:]])
        f.close()
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        body = 'Error getting email body... ' + \
               ''.join('!! ' + line for line in lines)
    try:
        send_mail.mail(sender, enc_pwd, recipient, subject, body)
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        err = 'Error sending update email!: '  + \
              ''.join('!! ' + line for line in lines)
        log(log_file_path, program, subject, err, True)

def send_msg(log_file_path,
             program,
             html, 
             links, 
             product,
             sms_params):
    try:
        sms_account = sms_params["sms_account"]
        sms_sender = sms_params["sms_sender"]
        mobile_nos = sms_params["mobile_nos"] # comma separated list, no spaces
        msg = product + ' may be available now, check on ' + links
        send_sms.main(msg, mobile_nos, sms_account, sms_sender)
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        err = 'Error sending sms: ' + ''.join('!! ' + line for line in lines)
        log(log_file_path, program, product, err, True)
    else:
        log(log_file_path, program, product, 'Link Available! SMS sent.')
        try:
            f = open('link_available.html', 'wb')
            f.write(html)
        except:
            pass
