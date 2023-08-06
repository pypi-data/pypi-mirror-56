# -*- coding: utf-8 -*-
# author: ethosa
from ..utils import *
requests.packages.urllib3.disable_warnings()
from .vkaudio import *
import traceback
import datetime
import asyncio
import random
import time
import sys

class Vk:
    '''
    docstring for Vk

    Get vk access token here:
    https://vkhost.github.io/ (choose the Kate mobile.)

    used:
    vk = Vk(token=Access_Token) # if you want auth to user
    vk = Vk(token=Group_Access_Token) # if you want auth to group

    use param version_api for change verison api. Default value is 5.103
    use param debug=True for debugging!
    use param lang='en' for set debug language! # en, ru, de, fr, ja

    for handling new messages:
    In the official VK API documentation, the event of a new message is called "message_new", so use:

    @vk.on_message_new
    def getMessage(obj):
        printf(obj)
        printf('text message:', obj.text) # see https://vk.com/dev/objects/message for more info
        printf(obj.obj)
        printf(obj.peer_id)

    use any vk api method:
    vk.method(method='messages.send', message='message', peer_id=1234567890)

    use messages methods:
    vk.messages.send(message='message', peer_id=1234567890)
    '''

    def __init__(self, token="", debug=0, version_api="5.103",
            group_id="", lang="en", login="", password=""):
        """initialization method
        
        Required for authorization in VK via token
        
        Arguments:
            token {str} -- VK token
            debug {bool} -- an option to enable debugging
            version_api {float or str} -- the version of VK API
            group_id {str or int} -- ID groups (if you authorize through the group)
            lang {str} -- language for debuging (can be "en", "ru", "de", "fr", "ja")
        """
        if login and password:
            session = requests.Session()
            def auth(session):
                location = str("https://login.vk.com/?act=grant_access&client_id=2685278&settings=1040183263"
                                "&redirect_uri=https%3A%2F%2Foauth.vk.com%2Fblank.html&response_type=token"
                                "&group_ids=&token_type=0&v=&state=&display=page&ip_h=0ce35355c94dac1278"
                                "&hash=1574456300_200c5d0e2c43de5377&https=1")
                return session.get(location)
            url = 'https://vk.com'
            session.headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language':'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
                        'Accept-Encoding':'gzip, deflate',
                        'Connection':'keep-alive',
                        'DNT':'1'
                    }
            data = session.get(url).text
            start = re.search("<form.+name=\"login.+", data).start()
            end = re.search("<input type=\"submit\" class=\"submit\" />", data).start()
            data = data[start:end]
            lg_h = re.findall("<input.+lg_h.+", data)[0]
            lg_h = lg_h.split("value=\"", 1)[1].split("\"", 1)[0].strip()
            ip_h = re.findall("<input.+ip_h.+", data)[0]
            ip_h = ip_h.split("value=\"", 1)[1].split("\"", 1)[0].strip()
            form = {'act' : 'login', 'role' : 'al_frame', 'expire' : '',
                    'recaptcha' : '', 'captcha_sid' : '', 'captcha_key' : '',
                    '_origin': 'https://vk.com', 'ip_h': ip_h,
                    'lg_h': lg_h, 'ul': '',
                    'email': login, 'pass': password}
            response = session.post("https://login.vk.com/", data=form)
            if not ('onLoginDone' in response.text):
                raise VkError("Auth error.")

            url1 = "https://oauth.vk.com/authorize?client_id=2685278&scope=1073737727&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token"
            text = session.get(url1).text
            location = re.findall(r'location.href = "(\S+)"\+addr;', text)
            if location:
                token = re.findall(r"token=([^&]+)", session.get(location[0]).url)
                if debug:
                    print(token)
                token = token[0]
        self.token_vk = token
        self.debug = debug 
        self.version_api = version_api
        self.group_id = group_id
        self.lang = lang
        self.errors_parsed = 0.0

        # Initialize methods
        self.longpoll = LongPoll(vk=self)
        self.method = Method(vk=self).use
        self.fastMethod = Method(vk=self).fuse
        self.execute = lambda code: self.fastMethod("execute", {"code" : code})

        self.help = Help

        # Other variables:
        self.translate = TranslatorDebug().translate
        self.vk_api_url = "https://api.vk.com/method/"

        if self.token_vk:
            if self.debug: sys.stdout.write(self.translate('Токен установлен. Проверяем его валидность ...', self.lang))
            test = ''.join(requests.get('%smessages.getLongPollServer?access_token=%s&v=%s%s' % (self.vk_api_url, self.token_vk, self.version_api, "&group_id=%s" % (self.group_id) if self.group_id else "")).json().keys())
            if self.debug: sys.stdout.write(self.translate("Ошибка" if test == "error" else 'Успешно!', self.lang))
        else:
            if self.debug: sys.stdout.write(self.translate("Ошибка", self.lang))

        self.uploader = Uploader(vk=self)


    # Handlers:
    # use handlers:
    # @vk.*name function*
    # def function(obj):
    #     pass
    #
    # Example:
    # @vk.on_wall_post_new
    # def get_message(obj):
    #     print("post text is", obj.text)
    #
    # Hander longpolls errors:
    # return object with variables:
    # object.message, object.line, object.code
    def onError(self, function):
        """call function when find error
        
        Arguments:
            function {callable object} -- [function or class]
        """
        self.errors_parsed = 1.0
        def parseError():
            while True:
                for error in self.longpoll.errors:
                    function(error)
                    self.longpoll.errors.remove(error)
        Thread_VK(parseError).start()

    def getUserHandlers(self):
        # return ALL user handlers
        return ["on_%s" % i for i in users_event]


    # Handler wrapper
    # Use it:
    # def a(func): vk.listenWrapper('message_new', Obj, func)
    # @a
    # def get_mess(obj):
    #   print(obj.text)
    def listenWrapper(self, type_value, classWrapper, function, e="type"):
        def listen(e=e):
            if type(type_value) == int: e = 0
            for event in self.longpoll.listen():
                if event.update[e] == type_value:
                    if self.errors_parsed:
                        try: function(classWrapper(event.update))
                        except Exception as error_msg:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            line = traceback.extract_tb(exc_tb)[-1][1]
                            self.longpoll.errors.append(Error(line=line, message=str(error_msg), code=type(error_msg).__name__))
                    else:
                        function(classWrapper(event.update))
        if "%s" % type(function) == "<class 'function'>" or "%s" % type(function) == "<class 'method'>":
            Thread_VK(listen).start()
        else:
            classWrapper = function
            return lambda function: self.listenWrapper(type_value, classWrapper, function)

    def getRandomId(self): return random.randint(-2_000_000, 2_000_000)

    def createExampleScript(self, name="testScript"):
        with open("%s.py" % name, "w") as f:
            f.write("""from social_ethosa import * # import library ..
TOKEN = "your token here"
GROUP_ID = "id of your group"

vk = Vk(token=TOKEN, group_id=GROUP_ID, debug=1, lang="en") # auth in

@vk.on_message_new # get all new messages
def newMessage(obj):
    print(obj.peer_id)
    vk.messages.send(message="Hello world", peer_id=peer_id,
                    random_id=vk.getRandomId())
""")
        sys.stdout.write(self.translate("В директории с текущим скриптом создан скрипт-пример использования библиотеки", self.lang))

    def __getattr__(self, method):
        if method.startswith("on_"):
            method = method[3:]
            if method not in users_event.keys():
                return lambda function: self.listenWrapper(method, Obj, function)
            else:
                return lambda function: self.listenWrapper(users_event[method][0], Obj, function)
        else: return Method(vk=self, method=method)

    def __str__(self):
        return "<Vk %s object at 0x%0x (group_id=%s)>" % (self.version_api, self.__hash__(), self.group_id)


class VkError(Exception):
    def __init__(self, message): self.message = message


class LongPoll:
    '''
    docstring for LongPoll

    usage:
    longpoll = LongPoll(access_token='your_access_token123')
    for event in longpoll.listen():
        print(event)
    '''
    def __init__(self, vk=None):
        if vk:
            self.group_id = vk.group_id
            self.access_token = vk.token_vk
            self.version_api = vk.version_api
        self.vk_api_url = 'https://api.vk.com/method/'
        self.ts = "0"
        self.errors = []
        self.session = requests.Session()
        self.session.headers = {
            "Content-Type" : "application/json"
        }

    def listen(self):
        """listening to longpoll
        
        Yields:
            [Event] -- event
        """
        if self.group_id:
            response = self.session.get("%sgroups.getLongPollServer?access_token=%s&v=%s&group_id=%s" %
                                (self.vk_api_url, self.access_token, self.version_api, self.group_id)).json()
            try:
                response = response['response']
            except Exception as e:
                raise VkError("auth error, %s. response: <%s>" % (e, response))
            self.ts = response['ts']
            self.key = response['key']
            self.server = response['server']
            emptyUpdates = []

            while 1.0:
                response = self.session.get('%s?act=a_check&key=%s&ts=%s&wait=25' % (self.server, self.key, self.ts)).json()
                self.ts = getValue(response, 'ts', self.ts)
                updates = getValue(response, 'updates')

                if updates:
                    for update in updates: yield Event(update)
                else:
                    emptyUpdates.append(0)
                if len(emptyUpdates) > 100:
                    break
            for e in self.listen():
                yield e
        else:
            response = self.session.get("%smessages.getLongPollServer?access_token=%s&v=%s" %
                                (self.vk_api_url, self.access_token, self.version_api)).json()
            try:
                response = response['response']
            except Exception as e:
                raise VkError("auth error, %s. response: <%s>" % (e, response))
            self.ts = response["ts"]
            self.key = response["key"]
            self.server = response["server"]
            emptyUpdates = []

            while 1.0:
                response = self.session.get('https://%s?act=a_check&key=%s&ts=%s&wait=25&mode=202&version=3' % (self.server,
                                            self.key, self.ts)).json()
                self.ts = getValue(response, 'ts', self.ts)
                updates = getValue(response, 'updates')

                if updates:
                    for update in updates: yield Event(update)
                else:
                    emptyUpdates.append(0)
                if len(emptyUpdates) > 100:
                    break
            for e in self.listen():
                yield e


# Class for use anything vk api method
# Usage:
# response = vk.method(method='wall.post', message='Hello, world!')
class Method:
    def __init__(self, vk=None, method=""):
        if vk:
            self.group_id = vk.group_id
            self.access_token = vk.token_vk
            self.version_api = vk.version_api
            self.getRandomId = vk.getRandomId
        self.method = method
        self.fuse = lambda method, kwargs: asyncio.run(self.Fuse(method, kwargs))
        self.use = lambda method, **kwargs: asyncio.run(self.Use(method, **kwargs))

    async def Use(self, method, **kwargs):
        url = "https://api.vk.com/method/%s" % method
        kwargs['access_token'] = self.access_token
        kwargs['v'] = self.version_api
        response = requests.post(url, data=kwargs).json()
        if "error" in response:
            raise VkError("error in method call <%s>" % response)
        return response

    async def Fuse(self, method, kwargs):
        url = "https://api.vk.com/method/%s" % method
        kwargs['access_token'] = self.access_token
        kwargs['v'] = self.version_api
        response = requests.post(url, data=kwargs).json()
        if "error" in response:
            raise VkError("error in method call <%s>" % response)
        return response

    def __getattr__(self, method):
        method = "%s.%s" % (self.method, method)
        def send(**kwargs):
            if method == "messages.send":
                kwargs["random_id"] = self.getRandomId()
            if "attachment" in kwargs:
                if isinstance(kwargs["attachment"], list) or isinstance(kwargs["attachment"], tuple):
                    kwargs["attachment"] = ",".join(kwargs["attachment"])
            elif "attachments" in kwargs:
                if isinstance(kwargs["attachments"], list) or isinstance(kwargs["attachments"], tuple):
                    kwargs["attachments"] = ",".join(kwargs["attachments"])
            return self.fuse(method, kwargs)
        return lambda **kwargs: send(**kwargs)

from .uploader import *

class Keyboard:
    """
    docstring for Keyboard

    use it for add keyboard in message

    keyboard = Keyboard()
    keyboard.addButton(Button(type='text', label='lol'))
    keyboard.addLine()
    keyboard.addButton(Button(type='text', label='hello', color=ButtonColor.POSITIVE))
    keyboard.addButton(Button(type='text', label='world', color=ButtonColor.NEGATIVE))
    # types "location", "vkpay", "vkapps" can't got colors. also this types places on all width line.
    keyboard.addButton(Button(type='location''))
    keyboard.addButton(Button(type='vkapps'', label='hello, world!'))
    keyboard.addButton(Button(type='vkpay''))
    """
    def __init__(self, **kwargs):
        self.keyboard = {
            "one_time" : getValue(kwargs, "one_time", True),
            "buttons" : getValue(kwargs, "buttons", [[]]),
            "inline" : getValue(kwargs, "inline", False)
        }
        if self.keyboard["inline"]:
            self.maxSize = (3, 3)
            del self.keyboard["one_time"]
        else:
            self.maxSize = (4, 10)

    def addLine(self):
        if len(self.keyboard['buttons']) < self.maxSize[1]:
            self.keyboard['buttons'].append([])

    def addButton(self, button):
        if len(self.keyboard['buttons'][::-1][0]) < self.maxSize[0]:
            if button['action']['type'] != 'text' and len(self.keyboard['buttons'][-1]) >= 1:
                self.addLine()
            if len(self.keyboard['buttons']) < self.maxSize[1]+1:
                self.keyboard['buttons'][::-1][0].append(button)
        else:
            self.addLine()
            if len(self.keyboard['buttons']) < self.maxSize[1]+1:
                self.addButton(button)

    def compile(self): return json.dumps(self.keyboard)

    def clear(self):
        self.keyboard["buttons"] = [[]]

    def createAndPlaceButton(self, *args, **kwargs):
        self.addButton(Button(*args, **kwargs))

    def visualize(self):
        for line in self.keyboard["buttons"]:
            sys.stdout.write("%s\n" % " ".join(["[%s]" % button["action"]["label"]
                                                if "label" in button["action"] else "[%s button]" % button["action"]["type"]
                                                for button in line]))


class Button:
    """
    docstring for Button

    Button use for Keyboard.
    Usage:
    red_button = Button(label='hello!', color=ButtonColor.NEGATIVE)

    and use red button:
    keyboard.add_button(red_button) # easy and helpfull!
    """
    PRIMARY = "primary"
    SECONDARY = "secondary"
    NEGATIVE = "negative"
    POSITIVE = "positive"
    def __init__(self, type="text", label="бан", payload="",
            hash="action=transfer-to-group&group_id=1&aid=10", owner_id="-181108510",
            app_id="6979588", color="primary"):
        self.type = type

        actions = {
            "text" : {
                "type" : "text",
                "label" : label,
                "payload" : payload
            },
            "location" : {
                "type" : "location",
                "payload" : payload
            },
            "vkpay" : {
                "type" : "vkpay",
                "payload" : payload,
                "hash" : hash
            },
            "vkapps" : {
                "type" : "open_app",
                "payload" : payload,
                "hash" : hash,
                "label" : label,
                "owner_id" : owner_id,
                "app_id" : app_id
            }
        }

        self.action = getValue(actions, self.type, actions['text'])
        self.color = color

    def setText(self, text):
        if "label" in self.action:
            self.action["label"] = text

    def setColor(self, color): self.color = color

    def getButton(self):
        kb = {'action' : self.action, 'color' : self.color}
        if kb['action']['type'] != 'text':
            del kb['color']
        return kb

    def __new__(self, type="text", label="бан", payload="",
                hash="action=transfer-to-group&group_id=1&aid=10", owner_id="-181108510",
                app_id="6979588", color="primary"):
        self.__init__(self, type, label, payload, hash, owner_id, app_id, color)
        return self.getButton(self)


class Error:
    def __init__(self, **kwargs):
        self.code = kwargs["code"]
        self.message = kwargs["message"]
        self.line = kwargs["line"]
    def __str__(self):
        return "%s, Line %s:\n%s" % (self.code, self.line, self.message)


class Help:
    """
    docstring for Help

    usage:
    vk.help() - return list of all methods

    vk.help('messages') - return list of all messages methods

    vk.help('messages.send') - return list of all params method
    """
    def __new__(self, *args, **kwargs):
        if not args:
            resp = requests.get('https://vk.com/dev/methods').text
            response = resp.split('<div id="dev_mlist_submenu_methods" style="">')[1].split('</div>')[0].split('<a')
            return [i.split('>')[1].split('</a')[0].lower() for i in response if len(i.split('>')) > 1 and i.split('>')[1].split('</a')[0] != '']
        else:
            return self.__getattr__(self, args[0])
    def __getattr__(self, method):
        if '.' not in method:
            resp = requests.get('https://vk.com/dev/%s' % method).text
            response = resp.split('<span class="dev_methods_list_span">')
            response = [i.split('</span>', 1)[0] for i in response if len(i.split('</span>', 1)[0]) <= 35]
            return response
        else:
            response = requests.get('https://vk.com/dev/%s' % method).text.split('<table class="dev_params_table">')[1].split('</table>')[0]

            params = {
                i.split('<td')[1].split('>')[1].split('</td')[0] : i.split('<td')[2].split('>', 1)[1].split('</td')[0]
                for i in response.split('<tr') if len(i) > 2 }

            for i in params.keys():
                params[i] = params[i].replace('\n', ' ').replace('&lt;', '{').replace('&gt;', '}')
                while '<' in params[i]:
                    pos = [params[i].find('<'), params[i].find('>')]
                    params[i] = "%s%s" % (params[i][:pos[0]], params[i][pos[1]+1:])
            return params