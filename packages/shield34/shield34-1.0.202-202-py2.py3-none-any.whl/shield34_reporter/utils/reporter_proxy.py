import time

import json
import os
import pickle
import platform
import stat
import sys
import tempfile

from browsermobproxy import Server

from shield34_reporter.auth.sdk_authentication import SdkAuthentication
from shield34_reporter.exceptions import Shield34LoginFailedException
from shield34_reporter.listeners.shield34_listener import Shield34Listener
from shield34_reporter.utils.network_utils import NetworkUtils
import urllib
import socket

class ReporterProxy():

    local_ip = None

    @staticmethod
    def get_ip():
        if ReporterProxy.local_ip is None:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                # doesn't even have to be reachable
                s.connect(('10.255.255.255', 1))
                IP = s.getsockname()[0]
            except:
                try:
                    IP = socket.gethostbyname(socket.gethostname())
                except:
                    IP = '127.0.0.1'
            finally:
                s.close()
            ReporterProxy.local_ip = IP
        return ReporterProxy.local_ip

    @staticmethod
    def browser_mob_proxy_is_listening(browser_mob_server,retry_count=60):
        count = 0
        while not browser_mob_server._is_listening():
            time.sleep(0.5)
            count += 1
            if count == retry_count:
                return False
        return True

    @staticmethod
    def create_proxy():
        if SdkAuthentication.is_authorized():
            from shield34_reporter.container.run_report_container import RunReportContainer
            block_run_report_container = RunReportContainer.get_current_block_run_holder()
            if block_run_report_container.proxyServer is None:
                browser_mob_server = None
                ReporterProxy.add_browsermob_to_path()
                proxy_data_filepath = ReporterProxy.get_shield34_proxy_data_filename()
                brwoser_mob_server_config = {}

                ReporterProxy.wait_for_lock_create_proxy_to_be_released(timeout=10)

                ReporterProxy.lock_create_proxy()
                if os.path.exists(proxy_data_filepath):
                    try:
                        brwoser_mob_server_config = ReporterProxy.read_json_from_file(proxy_data_filepath)
                        Shield34Listener.logger.console(
                            "Using Shield34 Proxy Server on port {}".format(brwoser_mob_server_config['port']))
                        browser_mob_server = Server('browsermob-proxy',
                                                    options={'port': brwoser_mob_server_config['port']})
                        browser_mob_server.host = ReporterProxy.get_ip()
                        browser_mob_server.command += ['--address=' + ReporterProxy.get_ip(),"--ttl=3600"]

                        browser_mob_server.pid = brwoser_mob_server_config['pid']
                    except Exception as e:
                        browser_mob_server = None

                if browser_mob_server is None or not ReporterProxy.browser_mob_proxy_is_listening(browser_mob_server,retry_count=10):
                    proxy_server_port = NetworkUtils.get_random_port(ReporterProxy.get_ip())
                    Shield34Listener.logger.console("Running Shield34 Proxy Server on port {}".format(proxy_server_port))
                    browser_mob_server = Server('browsermob-proxy',
                                                    options={'port': proxy_server_port})
                    browser_mob_server.host = ReporterProxy.get_ip()
                    browser_mob_server.command += ['--address='+ReporterProxy.get_ip(),"--ttl=3600"]

                    browser_mob_server.start()
                    brwoser_mob_server_config['port'] = proxy_server_port
                    brwoser_mob_server_config['pid'] = browser_mob_server.process.pid
                    browser_mob_server.pid = browser_mob_server.process.pid
                    try:
                        ReporterProxy.write_json_to_file(proxy_data_filepath, brwoser_mob_server_config)
                    except Exception as e:
                        pass

                ReporterProxy.release_lock_create_proxy()


                chained_proxy = ReporterProxy.get_os_proxies()
                sub_instance_port = NetworkUtils.get_random_port(ReporterProxy.get_ip())
                if chained_proxy is not None:
                    proxy = browser_mob_server.create_proxy(
                        params={"trustAllServers": "true", "port": sub_instance_port,
                                "bindAddress": ReporterProxy.get_ip(), 'httpProxy': chained_proxy})
                    Shield34Listener.logger.console("Creating Shield34 Proxy sub-instance on port {} through system proxy {}".format(sub_instance_port,chained_proxy))
                else:
                    proxy = browser_mob_server.create_proxy(
                        params={"trustAllServers": "true", "port": sub_instance_port,
                                "bindAddress": ReporterProxy.get_ip()})
                    Shield34Listener.logger.console("Creating Shield34 Proxy sub-instance on port {}".format(sub_instance_port))
                proxy.base_server = browser_mob_server
                block_run_report_container.proxyServer = proxy

                return True
            else :
                # proxy already exists. !
                return True
        return False



    @staticmethod
    def write_object_to_file(file_path, obj):
        pickle_out = open(file_path, "wb")
        pickle.dump(obj, pickle_out)
        pickle_out.close()

    @staticmethod
    def load_object_from_file(file_path):
        pickle_in = open(file_path, "rb")
        return pickle.load(pickle_in)

    @staticmethod
    def lock_create_proxy():
        ReporterProxy.write_lock_file(ReporterProxy.get_shield34_proxy_lock_filename())

    @staticmethod
    def release_lock_create_proxy():
        file =ReporterProxy.get_shield34_proxy_lock_filename()
        if os.path.exists(file):
            os.remove(file)

    @staticmethod
    def wait_for_lock_create_proxy_to_be_released(timeout=10):
        counter = 0
        while os.path.exists(ReporterProxy.get_shield34_proxy_lock_filename()):
            time.sleep(1)
            counter = counter + 1
            if counter > timeout:
                ReporterProxy.release_lock_create_proxy()
                break



    @staticmethod
    def get_shield34_proxy_lock_filename():
        temp_dir = tempfile.gettempdir()
        filepath = os.path.join(temp_dir, 'shield34_proxy.lck')
        return filepath

    @staticmethod
    def get_shield34_proxy_data_filename():
        temp_dir = tempfile.gettempdir()
        filepath = os.path.join(temp_dir, 'shield34_proxy.dat')
        return filepath

    @staticmethod
    def write_json_to_file(file_path, dictjson):
        with open(file_path, 'w') as file:
            file.write(json.dumps(dictjson))
        file.close()

    @staticmethod
    def write_lock_file(file_path):
        with open(file_path, 'w') as file:
            file.write("")
        file.close()

    @staticmethod
    def read_json_from_file(file_path):
        with open(file_path, 'r') as file:
            dictjsonstr = file.read()
        file.close()
        return json.loads(dictjsonstr)

    # @staticmethod
    # def close_proxy_if_idle():
    #     from shield34_reporter.container.run_report_container import RunReportContainer
    #     block_run_report_container = RunReportContainer.get_current_block_run_holder()
    #     proxy_ports = block_run_report_container.proxyServer.proxy_ports()
    #     if len(proxy_ports) == 1:
    #         port = proxy_ports[0]
    #         if port == block_run_report_container.proxyServer.port:
    #             try:
    #                 import psutil
    #                 p = psutil.Process(block_run_report_container.proxyServer.base_server.pid)
    #                 p.kill()
    #             except NoSuchProcess as e:
    #                 pass

    @staticmethod
    def get_os_proxies():
        if sys.version_info > (3, 0):
            proxies = urllib.request.getproxies()
        else:
            proxies = urllib.getproxies()

        if 'https' in proxies:
            proxy = proxies['https']
            proxy = proxy.replace("https://", "")
            proxy = proxy.replace("www.", "")
            return proxy
        elif 'http' in proxies:
            proxy = proxies['http']
            proxy = proxy.replace("http://", "")
            proxy = proxy.replace("www.", "")
            return proxy
        else:
            return None

    @staticmethod
    def add_browsermob_to_path():
        ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(ROOT_DIR, 'proxy', 'browsermob-proxy-2.1.4', 'bin')
        os.environ["PATH"] += os.pathsep + path
        #Shield34Listener.logger.console("added '{}' to the system environment path".format(path))
        try:
            if platform.system() != 'Windows':
                file = os.path.join(path, "browsermob-proxy")
                st = os.stat(file)
                os.chmod(file, st.st_mode | stat.S_IEXEC)
        except Exception as e:
            pass

