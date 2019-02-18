import multiprocessing

bind = '0.0.0.0:8000'
workers = multiprocessing.cpu_count() * 2 + 1
accesslog = '/var/log/gunicorn-access.log'
errlog = '/var/log/gunicorn-error.log'
capture_output = True
daemon = True
loglevel = 'debug'
