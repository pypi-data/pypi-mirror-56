#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Attribution: Hijacked from tracservice.py by Florent Xicluna <laxyf@yahoo.fr>
# http://trac-hacks.org/wiki/WindowsServiceScript
# then further hacked by Vernon Cole
#
# To use this class, users must do the following:
# 1. Edit the constants section with the proper information.
# 2. Open a command prompt with administrator rights and navigate to the directory
#    where this file is located.  Use one of the following commands to
#    install/start/stop/remove the service:
#    > adodbapi_service.py install
#    > adodbapi_service.py start
#    > adodbapi_service.py stop
#    > adodbapi_service.py remove
#    Additionally, typing "adodbapi_service.py" will present the user with all of the
#    available options.
#
# Once installed, the service will be accessible through the Services
# management console just like any other Windows Service.  All service 
# startup exceptions encountered by the AdodbapiWindowsService class will be 
# viewable in the Windows event viewer (this is useful for debugging
# service startup errors); all application specific output or exceptions should
# appear in the stdout/stderr logs.
#

import sys
import os
import datetime

from distutils import sysconfig

import win32serviceutil
import win32service

# ==  Editable CONSTANTS SECTION  ============================================

x_ADODBAPI_PROJECT = '%HOME%\\Documents\\adodbapi_projects\\myProject'

x_OPTS = {
    'hostname': 'myComputer.myDomain.com',
    'port': '80',
}

# ==  End of CONSTANTS SECTION  ==============================================

# Other constants
PYTHONDIR = sysconfig.get_python_lib()  # gets site-packages folder
PYTHONSERVICE_EXE = os.path.join(PYTHONDIR, 'win32', 'pythonservice.exe')
SERVER_PY = os.path.join(PYTHONDIR, 'adodbapi', 'service', 'run_server.py')
X_FILE = __file__
#x_LOG_DIR = os.path.join(ADODBAPI_PROJECT, 'log')
#x_SETTINGS = os.path.basename(ADODBAPI_PROJECT) + '.' + 'settings'

# Adodbapi Project
ARGS = [SERVER_PY]

class AdodbapiWindowsService(win32serviceutil.ServiceFramework):
    """Adodbapi Windows Service helper class.

    The AdodbapiWindowsService class contains all the functionality required
    for running Adodbapi application as a Windows Service.

    For information on installing the application, please refer to the
    documentation at the end of this module or navigate to the directory
    where this module is located and type "adodbapi_service.py" from the command
    prompt.
    """

    _svc_name_ = 'Adodbapi_%s' % str(hash(SERVER_PY))
    _svc_display_name_ = 'Adodbapi project at %s' % SERVER_PY
    _exe_name_ = PYTHONSERVICE_EXE

    def SvcDoRun(self):
        """ Called when the Windows Service runs. """

        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        self.x_httpd = self.adodbapi_init()
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        try:
            self.x_httpd.serve_forever()
        except OSError:
            sys.exit(1)

    def SvcStop(self):
        """Called when Windows receives a service stop request."""

        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        if self.x_httpd:
            self.x_httpd.server_close()
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def adodbapi_init(self):
        """ Checks for the required data and initializes the application. """

        def Klass(x=NotImplemented):
            # klass.inner_run(*args, **options)
            import errno
            import socket
            klass = NotImplemented
            httpd = NotImplemented

            quit_command = 'CTRL-BREAK' if sys.platform == 'win32' else 'CONTROL-C'

            klass.stdout.write("Validating models...\n\n")
            klass.validate(display_num_errors=True)
            klass.stdout.write((
                "%(started_at)s\n"
                "Adodbapi version %(version)s, using settings %(settings)r\n"
                "Starting development server at http://%(addr)s:%(port)s/\n"
                "Quit the server with %(quit_command)s.\n"
            ) % {
                "started_at": datetime.datetime.now().strftime('%B %d, %Y - %X'),
                "version": klass.get_version(),

                "addr": '[%s]' % klass.addr if klass._raw_ipv6 else klass.addr,
                "port": klass.port,
                "quit_command": quit_command,
            })


            try:
                handler = NotImplemented # .get_handler(*args, **options)
                # run(addr=klass.addr, port=int(klass.port), wsgi_handler=handler,
                #     ipv6=klass.use_ipv6, threading=threading)
                server_address = (klass.addr, int(klass.port))
                httpd = NotImplemented # (server_address, WSGIRequestHandler, ipv6=klass.use_ipv6)
                httpd.set_app(handler)
                
            except socket.error as e:
                # Use helpful error messages instead of ugly tracebacks.
                ERRORS = {
                    errno.EACCES: "You don't have permission to access that port.",
                    errno.EADDRINUSE: "That port is already in use.",
                    errno.EADDRNOTAVAIL: "That IP address can't be assigned-to.",
                }
                try:
                    error_text = ERRORS[e.errno]
                except KeyError:
                    error_text = str(e)
                klass.stderr.write("Error: %s" % error_text)
                # Need to use an OS exit because sys.exit doesn't work in a thread
                os._exit(1)

            return httpd


if __name__ == '__main__':
    # The following are the most common command-line arguments that are used
    # with this module:
    #  adodbapi_service.py install (Installs the service with manual startup)
    #  adodbapi_service.py --startup auto install (Installs the service with auto startup)
    #  adodbapi_service.py start (Starts the service)
    #  adodbapi_service.py stop (Stops the service)
    #  adodbapi_service.py remove (Removes the service)
    #
    # For a full list of arguments, simply type "adodbapi_service.py".
    win32serviceutil.HandleCommandLine(AdodbapiWindowsService)
