import sys
import os
import traceback
import win32serviceutil
import win32service

KEY_PATH = os.path.join(os.environ.get('SYSTEMROOT', r'c:\windows'), 'system32', 'easycluster_service.key')

class EasyClusterService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'EasyCluster'
    _svc_display_name_ = 'EasyCluster remote execution service'

    server = None
        
    def SvcDoRun(self):
        '''Start and run the service.'''
        try:
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            import easycluster.server
            import servicemanager
            servicemanager.LogInfoMsg('%s - Starting (%r)' % (self._svc_name_, sys.executable))
            easycluster.server.server_main(['-S', '-k', KEY_PATH])
        except Exception:
            import servicemanager
            servicemanager.LogErrorMsg(traceback.format_exc())

    def SvcStop(self):
        '''Stop the service.'''

        import easycluster.server
        import servicemanager
        servicemanager.LogInfoMsg('%s - Shutting down' % self._svc_name_)
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        easycluster.server.stop_server()

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(EasyClusterService)
