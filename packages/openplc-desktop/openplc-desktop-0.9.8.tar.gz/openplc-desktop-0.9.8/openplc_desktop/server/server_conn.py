# -*- coding: utf-8 -*-
# @author: Peter Morgan <pete@daffodil.uk.com>


import json
import mimetypes
import datetime

import paramiko
import websocket
from Qt import  Qt, QtCore, QtNetwork, QtWidgets, pyqtSignal


import G
from img import Ico


TIMEOUT = 5000 #30000
ATTR_TAG = QtNetwork.QNetworkRequest.User + 10
DEBUG_TAG = QtNetwork.QNetworkRequest.User + 20


class Reply:
    """A Reply is emitted by the Server Connection"""
    def __init__(self):

        self.debug = False
        self.busy = False
        self.url = None
        self.operation = None

        self.http_code = None

        self.error = None
        self.content = None
        self.data = None
        self.tag = None

    @property
    def get(self):
        """True if a GET operation"""
        return self.operation == QtNetwork.QNetworkAccessManager.GetOperation

    @property
    def post(self):
        """True if a POST operation"""
        return self.operation == QtNetwork.QNetworkAccessManager.PostOperation

    @property
    def status(self):
        return "BUSY" if self.busy else "IDLE"

    @property
    def method(self):
        """str with the request method eg `GET` """
        if self.get:
            return "GET"
        if self.post:
            return "POST"
        return "?method?"

    def callback(self, s=" ??"):
        """The callback function to call """
        #print(" << callback " ,s,  self.origin)
        if self.origin == None:
            # TODO make cancel
            print("####### origin disappeared. .CANCEL ME TODO...", self)
            return
        self.origin.on_server_reply(self)

    def print(self):
        if self.busy:
            print(">>------------------------->>")
        else:
            print("<<-------------------------<<")
        print("%s %s %s" % (self.status, self.method, self.url))
        if self.tag:
            print("tag=", self.tag)
        if self.data == None:
            print(" ## NO DATA ##")
            return

        if self.debug:
            print(self.data)
        else:
            print(", ".join( sorted(self.data.keys()) ))


    def __repr__(self):
        d = None
        if self.data:
            if isinstance(self.data, dict):
                d = sorted(self.data.keys())
            elif isinstance(self.data, list):
                d = self.data
            else:
                d = self.data.kkkcrash()

        return "<Reply %s %s %s:%s, ori=%s, err=%s \n  data=%s>" % (
            self.status, self.http_code, self.method, self.url, self.origin.__class__.__name__,  self.error, d)



class WebsocketClient(QtCore.QThread):

    sigWsMessage = pyqtSignal(object)

    def __init__(self, parent=None):
        super(WebsocketClient, self).__init__(parent)

        self.debug = True
        websocket.enableTrace(True)

        self.WS = websocket.WebSocketApp("ws://localhost:8080/ws",
                                    on_message = self.on_message,
                                    on_error = self.on_error,
                                    on_ping=self.on_ping,
                                    on_pong=self.on_pong,
                                    on_open = self.on_open,
                                    on_close = self.on_close)

    def on_message(self, message):#
        recs = json.loads(message)
        self.sigWsMessage.emit(recs)

        if self.debug:
            print("on_message", message)

    def on_error(self, *args):
        if self.debug:
            print("error", args)

    def on_close(self, *args):
        if self.debug:
            print("### closed ###", args)


    def on_pong(self, ws):
        #if self.debug:
        #    print("on_pong", ws)
        pass

    def on_ping(self, ws):
        #if self.debug:
        #    print("on_ping", ws)
        pass



    def on_open(self):
        if self.debug:
            print("on_open")

    def on_close(self):
        if self.debug:
            print("on_close")

    def run(self):
        self.WS.run_forever(ping_interval=3)

    def close_all(self):

        self.WS.close()
        self.WS = None
        self.exit()


class RuntimeMessage:

    def __init__(self, message=None, error=None, connected=None):

        self.message = message
        self.error = error
        self.connected = connected

class ServerConn( QtCore.QObject ):
    """
    HTTP Client for REST queries
    """
    TIMEOUT = 3000 #30000

    sigWsMessage = pyqtSignal(object)
    sigRuntimeMessage = pyqtSignal(object)
    sigSSHMessage = pyqtSignal(object, object)

    def __init__( self, parent, server_address=None ):
        super(ServerConn, self).__init__(parent)

        self.netManager = QtNetwork.QNetworkAccessManager( self )

        self.server_address = server_address

        ## The cookie jar only lasts for session
        # with pyqt we are using settings to persists (ATMO)
        self.cookieJar = QtNetwork.QNetworkCookieJar()
        self.netManager.setCookieJar( self.cookieJar )

        self.netManager.finished.connect(self.on_REQUEST_FINISHED)

        self.progressDialog = None


        ## Websocket
        self.webSock = WebsocketClient(self)
        self.webSock.sigWsMessage.connect(self.on_ws_message)


        ## Runtime
        self.runtimeSock = QtNetwork.QTcpSocket(self)
        self.runtimeSock.connected.connect(self.on_runtime_connected)
        self.runtimeSock.disconnected.connect(self.on_runtime_disconnected)
        self.runtimeSock.readyRead.connect(self.on_runtime_socket_ready_read)
        self.runtimeSock.error.connect(self.on_runtime_socket_error)

        self.sshClient = paramiko.SSHClient()
        self.sshClient.load_system_host_keys()
        self.sshClient.set_missing_host_key_policy(paramiko.WarningPolicy)

    def connect_ssh(self, host, port, username, password):
        #print("on_ssh")
        self.sshClient.connect(host, port=port, username=username, password=password)
        self.send_ssh("uname -a")
        self.send_ssh("whoami")


    def send_ssh(self, cmd):
        stdin, stdout, stderr = self.sshClient.exec_command(cmd)
        # print( stdout.read(), )
        sout = str(stdout.read(), encoding="ascii")
        serr = str(stderr.read(), encoding="ascii")
        #print(s)
        self.sigSSHMessage.emit(sout, serr)

    def send_runtime(self, cmd):
        cmdd = cmd + "\n"
        #print("send_runtime", cmdd)
        bites = QtCore.QByteArray()
        bites.append(cmdd)
        self.runtimeSock.write(bites)

    def connect_runtime(self):
        url = QtCore.QUrl(self.server_address)
        #print("connect_runtime", url.host())
        self.runtimeSock.connectToHost(url.host(), 43628)

    def on_runtime_connected(self):
        #print("on_runtime_connected")
        m = RuntimeMessage(connected=True)
        self.sigRuntimeMessage.emit(m)
        self.send_runtime("runtime_logs()")

    def on_runtime_disconnected(self):
        #print("on_runtime_disconnected")
        m = RuntimeMessage(connected=False)
        self.sigRuntimeMessage.emit(m)

    def on_runtime_socket_ready_read(self):
        #print("on_runtime_socket_ready_read")
        bites = self.runtimeSock.readAll()
        s = str(bites, encoding="ascii")
        m = RuntimeMessage(connected=True, message=s)
        self.sigRuntimeMessage.emit(m)

    def on_runtime_socket_error(self, err):
        #print("on_runtime_socket_error", err)
        m = RuntimeMessage(connected=False, error=err)
        self.sigRuntimeMessage.emit(m)


    def close_all(self):
        self.webSock.close_all()
        self.runtimeSock.close()

    ## ======================================
    def connect_websocket(self):
        print("connext")

        self.webSock.start()
        return
        addr = "ws://localhost:8080/ws" # % self.server_address

    def on_ws_message(self, mess):
        self.sigWsMessage.emit(mess)



    @property
    def base_url(self):
        if self.server_address == None:
            return ""
        return self.server_address + "/ajax"



    def _make_request_obj(self, origin, url_str, tag=None, debug=None):

        qurl = QtCore.QUrl("%s%s" % (self.base_url, url_str))

        request = QtNetwork.QNetworkRequest()
        request.setOriginatingObject(origin)
        request.setPriority(QtNetwork.QNetworkRequest.HighPriority)
        if tag != None:
            request.setAttribute(ATTR_TAG, tag)
        if debug != None:
            request.setAttribute(DEBUG_TAG, debug)

        #self.set_raw_header(request, "Host", qurl.host)
        self.set_raw_header(request, "X-OPENPLC-CLIENT", "openplc-desktop")
        self.set_raw_header(request, "X-OPENPLC-VERSION", "0.0.1")

        return request, qurl, None


    #==================================================================
    ## GET to server
    def get( self, origin, url=None, params=None,  tag=None, debug=False):
             #cb=None, widget=None,  debug=False, spinner=True):

        request, qurl, err = self._make_request_obj(origin, url, tag=tag)
        if err:
            return err

        q = QtCore.QUrlQuery()
        if params:
            for k, v in params.items():
                q.addQueryItem( str( k ), str( v ) )
        qurl.setQuery(q)

        request.setUrl(qurl)

        reply = Reply()
        reply.debug = debug
        reply.busy = True


        reply.url = request.url().toString()
        reply.origin = origin
        reply.operation = QtNetwork.QNetworkAccessManager.GetOperation
        reply.callback("get()")

        if debug:
            reply.print()

        self.netManager.get( request )




    #==================================================================
    ## POST to the server
    def post( self, origin, url, data=None, tag=None, form=False, debug=False ):

        request, qurl, err = self._make_request_obj(origin, url, tag=tag)

        bites = QtCore.QByteArray()
        if form:
            postData = QtCore.QUrlQuery()
            for k in data:
                postData.addQueryItem( k, str( data[k] ) )

            bites.append(postData.toString(QtCore.QUrl.FullyEncoded))


        else:

            data_str = json.dumps(data)
            bites.append(data_str)
            self.set_raw_header(request, "Content-Type", "application/json")
            self.set_raw_header(request, "Content-Length", str(len(data_str)))

        request.setUrl(qurl)

        reply = Reply()
        reply.busy = True
        reply.debug = debug
        reply.origin = origin
        reply.operation = QtNetwork.QNetworkAccessManager.PostOperation
        reply.callback("post()")

        self.progress_start(url)
        if debug:
            reply.print()

        self.netManager.post( request, bites)


    def progress_start(self, url=None):
        self.progressDialog = QtWidgets.QProgressDialog()
        self.progressDialog.setMinimumWidth(300)
        self.progressDialog.setWindowTitle("POST: server")
        if url:
            self.progressDialog.setLabelText(url)
        #self.progressDialog.setWindowIcon(Ico.icon(Ico.busy))
        self.progressDialog.setRange(0, 0)
        #self.progressDialog.setCancelButton(True)
        #progressDialog.setModal(True)
        self.progressDialog.setWindowModality(Qt.WindowModal)
        self.progressDialog.forceShow()
        return
        #progressDialog.hide()
        #if origin:
         #   self.progressDialog.setParent(origin)
        self.progressDialog.setRange(0, 0)
        self.progressDialog.forceShow()

    def progress_stop(self):
        #print(">> progress_stop")
        if self.progressDialog == None:
            return
        self.progressDialog.setRange(0, 100)
        self.progressDialog.hide()
        self.progressDialog = None

    @staticmethod
    def set_raw_header(request, ki, vi):

        ha = QtCore.QByteArray()
        ha.append(ki)

        ba = QtCore.QByteArray()
        ba.append(vi)

        request.setRawHeader(ha, ba)





    #==========================================================
    ## Server Request Finished
    def on_REQUEST_FINISHED( self, qreply ):

        """Server Request has finished, so parse and check for errors"""
        #print("< fin", qreply.errorString(), qreply)
        reply = Reply()
        reply.busy = False

        reply.url = qreply.request().url().toString()
        reply.origin = qreply.request().originatingObject()
        #reply.origin.on_server_status(Status.idle)


        reply.http_code = qreply.attribute(QtNetwork.QNetworkRequest.HttpStatusCodeAttribute)
        reply.operation = qreply.operation()

        reply.tag = qreply.request().attribute(ATTR_TAG)
        reply.debug = qreply.request().attribute(DEBUG_TAG)




        turl = qreply.request().url()
        reply.url = turl.path() + "?" + turl.query()


        self.progress_stop()

        if qreply.error():
            reply.error = "%s: %s" % (qreply.error(), qreply.errorString())
            reply.callback("srv.err")
            qreply.deleteLater()
            return

        if reply.http_code != 200: # Not ok!
            print("GOT ERROR", reply.http_code)
            if reply.http_code == 301:
                reply.error = "Permissions error"
            else:
                reply.error = "ERROR: %s" % reply.http_code
            reply.callback("srv.err")
            qreply.deleteLater()
            return



        ##==============================
        ## Decode and handle json reply
        try:
            contents = str(qreply.readAll().data(), encoding="ascii")
            #print("contents=", contents)
            reply.data = json.loads(contents)
            #print("reply.data=", type(reply.data))
            #print("> data", xdate.now())



            # Always expect a dict so throw tantrum otherwise
            if isinstance(reply.data, dict) or isinstance(reply.data, list):


                if "error" in reply.data and reply.data["error"]:
                    reply.error = reply.data["error"]
                reply.callback("data.json")
                qreply.deleteLater()
                if reply.debug:
                    reply.print()
                return


            print("GOT=========", reply.data.keys())
            panic()




        ## Probably some server error type string - didnt happen in JSON
        except ValueError as e:

            reply.error = str(e)
            reply.callback("error.json")
            qreply.deleteLater()
            return

        ########################################
        ## Json Decoding was not correct ?
        except TypeError as e:

            reply.error = str(e)
            reply.callback("error.json")
            qreply.deleteLater()
            return
                #self.xStatusBar.serverButton.setTex
                #self.xStatusBar.serverButton = s
                #self.xStatusBar.serverString = self.srv_str

        ########################################################
        ## json is decoded and works
        else:
            ## json says No Success will always be true
            if 'error' in resp.data and self.json['error']:
                print("App Error")
                self.update_status( SERVER_STATUS.APP_ERROR )


            dddd()
        qreply.deleteLater()





    ##########################################################################
    ##  UploadBinary Or Text File (probably fixed as binary
    ##########################################################################

    def upload_files( self, target_url, params, files_list, xWidget=None, debugMode=False ):


        #print "======================= UPLOAD    =============="
        files = {}
        for f in files_list:
            fileInfo = QtCore.QFileInfo( f )
            if not fileInfo.exists():
                #print "'%s' not exist" % f
                return None
            else:
                files[f] = fileInfo.fileName()

        params['file_count'] = len( files )



        #xx = QtCore.QDateTime().currentDateTime().toString("hh_mm_ss_")
        #file_name =  xx + fileInfo.fileName() # QtCore.QDateTime().currentDateTime().toString("hh_mm_ss") + ".xls"

        #fileObj = QtCore.QFile(file_path)
        #fileObj.open(QtCore.QIODevice.ReadOnly)
        #fileObj = open(file_path, 'rb')
        #print fileObj.read_all()
        ### Constants
        CRLF = "\r\n"
        BOUNDARY = "-----------------------------7d935033608e2" #any string to mark boundaries
        START_DELIM = "--" + BOUNDARY + CRLF # delimiter for start of content "block"
        CONTENT_DISPOSITION = 'Content-Disposition: form-data; '

        ## Byte array to append to
        requestContent = QtCore.QByteArray()

        ## Add the paramaters as form-data eg {'foo': 'bar', 'bar': 'beer'}

        for p_key in params:
            st = QtCore.QString( START_DELIM + ( 'Content-Disposition: form-data; name="%s"' % p_key ) + CRLF + CRLF )
            st.append( "%s%s" % ( params[p_key], CRLF ) )
            requestContent.append( st )

        ## Append the file - binary
        count = 0
        for file_path in files:

            fileObj = QtCore.QFile( file_path )
            fileObj.open( QtCore.QIODevice.ReadOnly )

            st = QtCore.QString( START_DELIM + 'Content-Disposition: form-data; name="file_%s"; filename="%s";%s' % ( count, files[file_path], CRLF ) )

            mime_type, encoding = mimetypes.guess_type( file_path )
            content_type = "Content-Type: %s" % mime_type
            st.append( content_type + CRLF + CRLF )

            requestContent.append( st )
            requestContent.append( fileObj.readAll() )

            term = QtCore.QString( CRLF + "--" + BOUNDARY + "--" + CRLF )
            requestContent.append( term )
            count += 1



        #dataToSend = QtCore.QString(data).toAscii()
        self.emit( QtCore.SIGNAL( "payload_size" ), requestContent.size() ) #, payload

        ## Constuct Request

        #self.url = QtCore.QUrl( "%s/rpc%s" % ( self.srv_url, action_url ) )
        self.url = QtCore.QUrl( "http://%s/%s" % ( self.srv.ip, target_url ) )

        request = QtNetwork.QNetworkRequest()
        request.setUrl( self.url )
        request.setRawHeader( "Content-Type", 'multipart/form-data; boundary="%s"' % BOUNDARY )
        request.setRawHeader("Host", self.srv.host)
        request.setHeader( QtNetwork.QNetworkRequest.ContentLengthHeader, QtCore.QVariant( requestContent.size() ) )
        self.load_cookies()



    def file_upload_progress( self, progress, size ):
        self.emit( QtCore.SIGNAL( "uploadProgress" ), progress, size )


