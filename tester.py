import os

log_directory = '/home/sohfix/logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_file = os.path.join(log_directory, 'application.log')
