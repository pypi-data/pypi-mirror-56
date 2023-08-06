# -*- coding: utf-8 -*-


import json
import mimetypes

from Qt import Qt, QtCore, QtNetwork, QtWidgets, pyqtSignal

#from img import Ico

TIMEOUT = 5000  # 30000
ATTR_TAG = QtNetwork.QNetworkRequest.User + 10
DEBUG_TAG = QtNetwork.QNetworkRequest.User + 20


class Reply:

    def __init__(self):

        self.debug = True
        self.busy = False

        self.origin = None
        self.url = None
        self.operation = None
        self.http_code = None

        self.error = None
        self.content = None
        self.data = None
        self.tag = None

    def is_origin(self, other):
        return self.origin == other

    @property
    def get(self):
        return self.operation == QtNetwork.QNetworkAccessManager.GetOperation

    @property
    def post(self):
        return self.operation == QtNetwork.QNetworkAccessManager.PostOperation

    @property
    def status(self):
        return "BUSY" if self.busy else "IDLE"

    @property
    def method(self):
        if self.get:
            return "GET"
        if self.post:
            return "POST"
        return "?method?"

    def callback(self, s=" ??"):
        # print(" << callback " ,s,  self.origin)
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
            print(", ".join(sorted(self.data.keys())))

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
            self.status, self.http_code, self.method, self.url, self.origin.__class__.__name__, self.error, d)


class ServerConn(QtCore.QObject):
    """
    HTTP Client for ajax queries
    """
    TIMEOUT = 3000  # 30000

    def __init__(self, parent, server=None):
        super(ServerConn, self).__init__(parent)

        self.netManager = QtNetwork.QNetworkAccessManager(self)

        ## The cookie jar only lasts for session
        # with pyqt we are using settings to persists (ATMO)
        self._cookieJar = QtNetwork.QNetworkCookieJar()
        self.netManager.setCookieJar(self._cookieJar)

        self.netManager.finished.connect(self.on_REQUEST_FINISHED)

        self.progressDialog = None
        if False:
            self.progressDialog = QtWidgets.QProgressDialog()
            self.progressDialog.setMinimumWidth(300)
            self.progressDialog.setWindowTitle("Server")
            self.progressDialog.setWindowIcon(Ico.icon(Ico.Busy))
            self.progressDialog.setRange(0, 5)
            self.progressDialog.setCancelButton(None)
            self.progressDialog.setModal(True)
            self.progressDialog.setWindowModality(Qt.WindowModal);
            self.progressDialog.hide()

    def make_request_obj(self, origin, url_str, tag=None, debug=None):

        srv = G.settings.current_server()
        if srv == None:
            return None, None, "No Server set"

        qurl = QtCore.QUrl("%s%s" % (srv, url_str))

        request = QtNetwork.QNetworkRequest()
        request.setOriginatingObject(origin)
        request.setPriority(QtNetwork.QNetworkRequest.HighPriority)
        if tag != None:
            request.setAttribute(ATTR_TAG, tag)
        if debug != None:
            request.setAttribute(DEBUG_TAG, debug)

        self.set_raw_header(request, "Host", qurl.host())

        return request, qurl, None

    # ==================================================================================
    ## Send GET to server
    def get(self, origin, url=None, params=None, tag=None, debug=False):

        request, qurl, err = self.make_request_obj(origin, url, tag=tag, debug=debug)
        if err:
            return err

        q = QtCore.QUrlQuery()
        if params:
            for k, v in params.items():
                q.addQueryItem(str(k), str(v))
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

        self.netManager.get(request)

    # ==================================================================================
    ## Send POST to the server
    def post(self, origin, url, data=None, cb=None, widget=None, debug=False,
             tag=None, form=False):  # , form=True, debug=False, progress=True, html=None, custom_url=False ):

        request, qurl, err = self._make_request_obj(origin, url, tag=tag, debug=debug)

        bites = QtCore.QByteArray()
        if form:
            postData = QtCore.QUrlQuery()
            for k in data:
                postData.addQueryItem(k, str(data[k]))

            bites.append(postData.toString(QtCore.QUrl.FullyEncoded))


        else:
            data_str = json.dumps(data)
            bites.append(data_str)
            self.set_raw_header(request, "Content-Type", "application/json")
            self.set_raw_header(request, "Content-Length", str(len(data_str)))

        request.setUrl(qurl)
        # self._set_raw_header(request, "Content-Type", "application/x-www-form-urlencoded")

        reply = Reply()
        reply.busy = True
        reply.debug = debug
        reply.origin = origin
        reply.operation = QtNetwork.QNetworkAccessManager.PostOperation
        reply.callback("post()")

        self.progress_start(url)
        if debug:
            reply.print()

        self.netManager.post(request, bites)

    def progress_start(self, url=None):
        self.progressDialog = QtWidgets.QProgressDialog()
        self.progressDialog.setMinimumWidth(300)
        self.progressDialog.setWindowTitle("POST: server")
        if url:
            self.progressDialog.setLabelText(url)
        # self.progressDialog.setWindowIcon(Ico.icon(Ico.busy))
        self.progressDialog.setRange(0, 0)
        # self.progressDialog.setCancelButton(True)
        # progressDialog.setModal(True)
        self.progressDialog.setWindowModality(Qt.WindowModal)
        self.progressDialog.forceShow()

    def progress_stop(self):
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

    ###################################################################################
    ## Server Request Finished
    ###################################################################################
    def on_REQUEST_FINISHED(self, qreply):

        """Server Request has finished, so parse and check for errors"""

        reply = Reply()
        reply.busy = False

        reply.url = qreply.request().url().toString()
        reply.origin = qreply.request().originatingObject()
        reply.http_code = qreply.attribute(QtNetwork.QNetworkRequest.HttpStatusCodeAttribute)
        reply.operation = qreply.operation()

        reply.tag = qreply.request().attribute(ATTR_TAG)
        reply.debug = qreply.request().attribute(DEBUG_TAG)

        turl = qreply.request().url()
        reply.url = turl.path() + "?" + turl.query()

        # reply.content = str(qreply.readAll().data(), encoding="ascii")

        self.progress_stop()

        if reply.http_code != 200:  # Not ok!

            if reply.http_code == 301:
                reply.error = "Permissions error"
            else:
                reply.error = "ERROR: %s" % reply.http_code
            reply.callback("server.err")
            qreply.deleteLater()
            return


        ##==============================
        ## Decode and handle json reply
        try:
            contents = str(qreply.readAll().data(), encoding="ascii")

            reply.data = json.loads(contents)

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
            return

        ## Probably some server error type string - didnt happen in JSON
        except ValueError as e:

            reply.error = str(e)
            reply.callback("error.json")
            qreply.deleteLater()
            return

        ## Json Decoding was not correct ?
        except TypeError as e:

            reply.error = str(e)
            reply.callback("error.json")
            qreply.deleteLater()
            return

        except Exception as e:
            reply.error = str(e)
            reply.callback("error")
            qreply.deleteLater()
            return

        qreply.deleteLater()

    ##########################################################################
    ##  UploadBinary Or Text File (probably fixed as binary
    ##########################################################################

    def upload_files(self, target_url, params, files_list, xWidget=None, debugMode=False):

        # self.widget = xWidget

        # self.set_widget(xWidget)
        # self.start_timer()

        # print "======================= UPLOAD    =============="
        files = {}
        for f in files_list:
            fileInfo = QtCore.QFileInfo(f)
            if not fileInfo.exists():
                # print "'%s' not exist" % f
                return None
            else:
                files[f] = fileInfo.fileName()

        params['file_count'] = len(files)

        # xx = QtCore.QDateTime().currentDateTime().toString("hh_mm_ss_")
        # file_name =  xx + fileInfo.fileName() # QtCore.QDateTime().currentDateTime().toString("hh_mm_ss") + ".xls"

        # fileObj = QtCore.QFile(file_path)
        # fileObj.open(QtCore.QIODevice.ReadOnly)
        # fileObj = open(file_path, 'rb')
        # print fileObj.read_all()
        ### Constants
        CRLF = "\r\n"
        BOUNDARY = "-----------------------------7d935033608e2"  # any string to mark boundaries
        START_DELIM = "--" + BOUNDARY + CRLF  # delimiter for start of content "block"
        CONTENT_DISPOSITION = 'Content-Disposition: form-data; '

        ## Byte array to append to
        requestContent = QtCore.QByteArray()

        ## Add the paramaters as form-data eg {'foo': 'bar', 'bar': 'beer'}

        for p_key in params:
            st = QtCore.QString(START_DELIM + ('Content-Disposition: form-data; name="%s"' % p_key) + CRLF + CRLF)
            st.append("%s%s" % (params[p_key], CRLF))
            requestContent.append(st)

        ## Append the file - binary
        count = 0
        for file_path in files:
            fileObj = QtCore.QFile(file_path)
            fileObj.open(QtCore.QIODevice.ReadOnly)

            st = QtCore.QString(START_DELIM + 'Content-Disposition: form-data; name="file_%s"; filename="%s";%s' % (
            count, files[file_path], CRLF))

            mime_type, encoding = mimetypes.guess_type(file_path)
            content_type = "Content-Type: %s" % mime_type
            st.append(content_type + CRLF + CRLF)

            requestContent.append(st)
            requestContent.append(fileObj.readAll())

            term = QtCore.QString(CRLF + "--" + BOUNDARY + "--" + CRLF)
            requestContent.append(term)
            count += 1

        # dataToSend = QtCore.QString(data).toAscii()
        self.emit(QtCore.SIGNAL("payload_size"), requestContent.size())  # , payload

        ## Constuct Request

        # self.url = QtCore.QUrl( "%s/rpc%s" % ( self.srv_url, action_url ) )
        self.url = QtCore.QUrl("http://%s/%s" % (self.srv.ip, target_url))

        request = QtNetwork.QNetworkRequest()
        request.setUrl(self.url)
        request.setRawHeader("Content-Type", 'multipart/form-data; boundary="%s"' % BOUNDARY)
        request.setRawHeader("Host", self.srv.host)
        request.setHeader(QtNetwork.QNetworkRequest.ContentLengthHeader, QtCore.QVariant(requestContent.size()))
        self.load_cookies()

        ## Post to server
        # self.update_status( SERVER_STATUS.BUSY )
        # self.errorFlag = False
        # self.abort_flag = False

        # self.timeoutTimer.setInterval( self.TIMEOUT * 100 ) # Huge file
        # self.timeoutTimer.start()
        # self.POST = False

        # self.reply = self.netMan.post( self.request, requestContent )
        # self.connect( self.reply, QtCore.SIGNAL( "uploadProgress(qint64,qint64)" ), self.file_upload_progress )
        # self.connect( self.reply, QtCore.SIGNAL( 'error(QNetworkReply::NetworkError)' ), self.on_network_error )
        # self.connect( self.reply, QtCore.SIGNAL( 'readyRead()' ), self._on_server_ready_read )
        # self.connect( self.reply, QtCore.SIGNAL( 'finished()' ), self._on_server_read_finished )

    def file_upload_progress(self, progress, size):
        self.emit(QtCore.SIGNAL("uploadProgress"), progress, size)


