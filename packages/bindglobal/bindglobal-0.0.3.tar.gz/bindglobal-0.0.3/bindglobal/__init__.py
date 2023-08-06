"""
bindglobal v.0.0.3
by segalion at g(oogle) m a i l
Works like
[tkinter bind](https://effbot.org/tkinterbook/tkinter-events-and-bindings.htm)
but globaly.

Based on pynput

TODO:
- bind/un_bind automatically start/stop listeners
- populate event parameters (keycode, )
- quit gracefully

Notes for OSX:
To get permissons for keystrokes:
Just replace com.mizage.divvy with your program.
sudo sqlite3 /Library/Application\ Support/com.apple.TCC/TCC.db "INSERT INTO access VALUES('kTCCServiceAccessibility','com.mizage.divvy',0,1,1,NULL);"
To remove the entry:
sudo sqlite3 /Library/Application\ Support/com.apple.TCC/TCC.db "delete from access where client='com.mizage.divvy';"
"""

from pynput import keyboard, mouse
import datetime, threading, queue, logging

class PynputEvent:
    """Internal class.
    Container for the properties of a event, similar to a normal tkinter.Event.
    An instance of the PynputEvent class has the following attributes:

    widget: The widget which generated this event. This is a valid Tkinter 
            widget instance, not a name. This attribute is set for all events.
    x, y: The current global mouse position, in pixels.
    char: The character code (keyboard events only), as a string.
    keysym: The key symbol (keyboard events only).
    keycode: The key code (keyboard events only).
    num: The button number (mouse button events only).
    type: The event type ('keyboard' or 'mouse')
    time: datetime of last key/mouse that make fires the bind event
    delta: mousewheel points (positve/negative
    state: string showing modifiers keys like alt, control, shift, etc. 
            in a 'alt_l+shift_r+' form 
            (note this is not included in tkinter standar event) 

    Depending on type of Pynput event however, not all attributes may be set.
    """
    (widget,x,y,char,state,keysym,keycode,num) = (None,0,0,"","",0,0,0)
    (time,event,type,keys,delta) = (0,"","","",0)

    def __str__(self):
        return "{!s} (k:{!s} @{!s}x{!s})". format(self.event, self.keys
                                                  , self.x, self.y)

#from enum import Enum
#class TkKey(Enum):
#    for i in [ 'space','BackSpace', 'Tab'
#        #,'Menu','Insert', 'Pause', 'Num_Lock', 'Scroll_Lock'
#        ,'Left','Right', 'Up', 'Down'
#        ]:
#        eval(i + '=' + 'keyboard.Key.' + i.lower())
#for k in TkKey:
#    print(k)

class TkKeys(object):
    tk_keys = {}
    for i in ( 'space','BackSpace', 'Tab'
        , 'Delete', 'End', 'Home', 'Caps_Lock'
        ,'Left','Right', 'Up', 'Down'
        ,'Menu','Insert', 'Pause', 'Num_Lock', 'Scroll_Lock' #Those fails on OSX
        ):
        try:
            tk_keys.update({i: eval("keyboard.Key." + i.lower())})
        except:
            pass
            
    for i in range(1, 12):
        try:
            tk_keys.update({"F"+str(i): eval("keyboard.Key.f" + str(i))})
        except:
            pass
    for i, v in (('Cancel','esc'), ('Return','enter')
            , ('Escape','esc'),  ('less','<')
            , ('Prior','page_up'), ('Next','page_down')
            , ('Print','print_screen') #fails on osx
            ):
        try:
            tk_keys.update({i: eval("keyboard.Key." + v)})
        except:
            pass
    for i in range(1, 5):
        try:
            tk_keys.update({"Key"+str(i): eval(
                "keyboard.Code(char='" + str(i)+"')")})
        except:
            pass

    tk_mods = {}
    tk_mods.update({
        'Control':  keyboard.Key.ctrl
        , 'Control_L':  keyboard.Key.ctrl_l
        , 'Control_R':  keyboard.Key.ctrl_r
        , 'Shift':  keyboard.Key.shift
        , 'Shift_R': keyboard.Key.shift_r
        , 'Shift_L': keyboard.Key.shift_l
        , 'Alt': keyboard.Key.alt
        , 'Alt_R': keyboard.Key.alt_r
        , 'Alt_L': keyboard.Key.alt_l
        , 'Command': keyboard.Key.cmd
        , 'Command_L': keyboard.Key.cmd_l
        , 'Command_R': keyboard.Key.cmd_r
        })

    tk_anykey=['Key', 'KeyPress']
    tk_keyrelease=['KeyRelease']
    tk_mods2=['Any','Extended', 'Lock', 'Option'
        ,'Meta', 'Meta_L', 'Meta_R' #,'M'
        ,'Mod1', 'M1','Mod2', 'M2','Mod3', 'M3','Mod4', 'M4','Mod5', 'M5'
        ]

    tk_mouse = {}
    tk_mouse.update({
        'Button1': "Button.left"
        ,'1': "Button.left"
        ,'Button2': "Button.right"
         ,'2': "Button.right"
        ,'Button3': "Button.middle"
        ,'3': "Button.middle"
        ,'Button4': "Mousewheel"
        ,'4': "Mousewheel"
        ,'Button5': "Mousewheel"
        ,'5': "Mousewheel"
        ,'Mousewheel': "Mousewheel"
        # Mousewheel maps to B4 or B5 in X11 and MouseWheel on Windows and OSX.
        # event.delta  /120 the ticks positive/negative
        ,'Motion': "Motion"
        })

    tl_mouserelease=['ButtonRelease']

    tk_clics=['Double', 'Triple', 'Quadruple']

    @staticmethod
    def replaces(ev):
        ev.strip() #remove spaces after and before
        for i in ['1', '2', '3', '4', '5']:
            ev.replace("Key-" + i, "Key" + i)
            ev.replace("KeyPress-" + i, "Key" + i)
            ev.replace("Button-" + i, "Button" + i)
            ev.replace("B" + i, "Button" + i)
            ev.replace("ButtonRelease-" + i, "ButtonRelease" + i)
            ev.replace("ButtonPress-" + i, "Button" + i)


class BindGlobal(object):

    def __init__(self, widget=None, timeout=200, logger=None):
        
        self._keys = set() # The monitorized keys
        self._current = set() # The monitorized and the currently pressed keys
        self._mods = set() # The currently pressed mods
        self._combs = [] # list of monitorized key/mouse combinations
        self._anykey = 0 # if special "anykey" mode is enabled
        self._last_press = 0 # last key pressed without release (to filter repeated press)
        self.started = False
        self._on_move = False
        self._logger = logger
        t = datetime.datetime.now()
        self._last = [ [0,t], [0,t], [0,t], [0,t] ]
        t = timeout
        self._t= [ datetime.timedelta(milliseconds=t*3)
            , datetime.timedelta(milliseconds=t*2)
            , datetime.timedelta(milliseconds=t*1)
            , datetime.timedelta(milliseconds=0)
            ]

        self._queue = queue.Queue()
        self._event = PynputEvent()
        self._widget = widget
        self._event.widget = widget
        self._thread = 0
        self.cmouse = mouse.Controller()

    def _log(self,msg,*args,**kargs):
        if self._logger:
            self._logger.debug(msg,*args,**kargs)
        
    def _thread_caller_loop(self):
        while True:
            [callback, e] = self._queue.get()
            if callable(callback):
                callback(e)
            if callback is None:
                break
        self._log("_thread_caller_loop exiting")

    def _tk_caller(self, ev):
        """call to callback function inside tkinter thread (main)"""
        [callback, e] = self._queue.get()
        self._log('_tk_caller calling function {}'.format(callback))
        callback(e)
        
    def _call_4_combs(self, key, x=None, y=None, dx=None, dy=None):
        ''' queue every callbak that pressed key (or mouse)
        has make matched mouse/keys combination fire.
        this is running on external keyboard/mouse hooks thread'''
        for comb in self._combs:
            keys, clics, ev, callback = comb
            aclics=abs(clics)
            if aclics>0 and all(k in self._current for k in keys):
                if len(keys)>1 and "any_key" in keys and key in TkKeys.tk_mods.values():
                    continue
                if aclics == self._repeated or "any_key" in keys: #create event and enqueue
                    self._event.time = self._last[-1][1] #last datetime
                    self._event.event = ev
                    self._event.keys = keys
                    s = str(key)
                    ini = s[0:3]
                    self._event.char,self._event.keysym,  self._event.state = ("", "",  "")
                    self._event.num, self._event.delta = (0, 0)
                    if ini =='Key' or len(s)==3: #keyboard
                        self._event.type = "keyboard"
                        self._event.x, self._event.y = self.cmouse.position
                        #self._event.char = key.char #imposible access key internal
                        #self._event.keysym = key.vk
                        if len(s)==3:
                            self._event.char= s[1:2]
                        elif key not in TkKeys.tk_mods.values():
                            self._event.keysym = "<" + s[4:] + ">"
                    else: #mouse
                        self._event.type = "mouse"
                        self._event.x, self._event.y = (x, y)
                        if ini=='But': #clic
                            self._event.num  = s[7:]
                        elif ini=='Mou': #wheel
                            self._event.delta = dy
                    for i in self._mods:
                        self._event.state += (i[4:].split(':')[0] + '+')
                    # print('queueing callback {} for event {}'.format(callback, ev))
                    self._queue.put([callback, self._event])
                    if self._widget is not None:
                        self._widget.event_generate('<<Pynput>>')

    def _start_keyboard(self):
        self._k_listener = keyboard.Listener(
                on_press = self.on_press,
                on_release = self.on_release)
        self._k_listener.start()
        self._log("keyboard started @" + threading.currentThread().getName())

    def _start_mouse(self):
        self._m_listener = mouse.Listener(
                on_move = self.on_move,
                on_click = self.on_click,
                on_scroll = self.on_scroll)
        self._m_listener.start()
        self._log("mouse started @" + threading.currentThread().getName())

    def join(self):
        self._thread.join()
        
    def start(self):
        if self.started:
            return
        if self._widget is None:
            self._log("starting keyboard in threading mode")
            if not isinstance(self._thread,  threading.Thread) or not self._thread.is_alive():
                self._log("starting thread 1")
                self._thread = threading.Thread(target=self._thread_caller_loop)
                self._thread.start()
            self._start_keyboard()
        else:
            self._log("starting keyboard in tkinter mode")
            self._widget.bind('<<Pynput>>', self._tk_caller)
            self._thread = threading.Thread(target=self._start_keyboard).start()
        
        if self._widget is None:
            self._log("starting mouse in threading mode")
            if not isinstance(self._thread,  threading.Thread) or not self._thread.is_alive():
                self._log("starting thread 2")
                self._thread = threading.Thread(target=self._thread_caller_loop)
                self._thread .start()
            self._start_mouse()
        else:
            self._log("starting mouse in tkinter mode")
            self._widget.bind('<<Pynput>>', self._tk_caller)
            self._thread = threading.Thread(target=self._start_mouse).start()
        self.started = True

    def stop(self):
        if not self.started:
            return
        self._k_listener.stop()
        self._log("keyboard listener stoped")
        self._m_listener.stop()
        self._log("mouse listener stoped")
        # self._thread.join()
        if self._widget is None:
            self._queue.put([None, None]) #force exit
        else:
            self._widget.unbind('<<Pynput>>', self._tk_caller)
        self.started = False

    def _create_comb(self, tk_comb):
        comb = set()
        clics, aclic, nclics = 1, 1, 1
        self._log("tk_comb='"+str(tk_comb)+"'")
        TkKeys.replaces(tk_comb)
        if len(tk_comb)==1:
            if tk_comb != " " and tk_comb !="<":
                comb.add(keyboard.KeyCode(char=tk_comb))
        else:
            e=tk_comb[1:-1].split('-')
            for k in e:
                if k in TkKeys.tk_keyrelease:
                    aclic = -1
                elif k in TkKeys.tk_clics:
                    nclics = TkKeys.tk_clics.index(k) + 2
                elif k in TkKeys.tk_anykey:
                    self._anykey += 1
                    comb.add("any_key")
                elif k in TkKeys.tk_keys:
                    comb.add(TkKeys.tk_keys[k])
                elif k in TkKeys.tk_mods:
                    comb.add(TkKeys.tk_mods[k])
                elif k in TkKeys.tk_mouse:
                    comb.add(TkKeys.tk_mouse[k])
                elif len(k)==1:
                    comb.add(keyboard.KeyCode(char=k))
                elif k.isnumeric(): # numeric keycodes (i.e. in linux Alt-Gr is 65027
                    comb.add(keyboard.KeyCode(int(k)))
                else:
                    clics=0
                    self._log("clics=0")
            clics = clics*aclic*nclics
        return [comb,clics, tk_comb]

    def gbind(self, event, callback=None,  add=''):
        """ Equivalent tkinter bind command, but for global enviroment
        (not only tkinter app).
        if callback is ommited, return list of actual binding combinations.
        """
        [keys, clics, tk_comb] = self._create_comb(event)
        self._log("global bind for {}: keys={}({})".format(tk_comb, keys, clics))
        combs=[]
        if add != '+': # replace existing bind callback
            for i,c in enumerate(self._combs):
                if c[0]==keys and c[2]==clics:
                    if callback is None:
                        combs.append(c)
                    elif callable(callback):
                        for k in keys:
                            self._keys.add(k)
                        self._combs[i] = [keys, clics, tk_comb, callback]
                        return callback
        # add new
        if callback is None:
            return combs
        elif callable(callback):
            for k in keys:
                self._keys.add(k)
            self._combs.append([keys, clics, tk_comb, callback])
            if not self.started:
                self.start()
            self._log("OK: bind_global started={}: keys={}".format(self.started, self._keys))
            return callback
        return None

    def gunbind(self, event, callback=None):
        self._keys.clear()
        [keys, clics, tk_comb] = self._create_comb(event)
        self._log("global unbind for {}: keys={}({})".format(tk_comb, keys, clics))
        for i,c in enumerate(self._combs):
            if c[0]==keys and c[1]==clics and (callback==c[3] or callback==None):
                self._combs.pop(i)
                if  "any_key" in keys:
                    self._anykey -= 1
            else:
                for k in keys:
                    self._keys.add(k)
        if self._combs==[]:
            self.stop()

    def _multi_clic(self, key):
        """ Return number of times pressed same key (1 a 4)
        for simple, double, triple or quadruple clics"""
        self._last.append([key, datetime.datetime.now()])
        self._last.pop(0)
        rk= [i[0] == self._last[-1][0] for i in self._last][::-1]+[False]
        rt = [self._last[-1][1]-i[1]<=self._t[j] for j,i in enumerate(self._last)][::-1]+[False]
        return min(rk.index(False), rt.index(False))
        
    def on_press(self, key):
        if self._last_press == key: # filter repeated on_press without on_release (in windows)
            return
        self._last_press = key
        self._log("on_press {}".format(key))
        if key in TkKeys.tk_mods.values():
            self._mods.add(str(key))
        self._repeated = self._multi_clic(key)
        if self._anykey>0 or key in self._keys:
            self._current.add(key)
            if self._anykey>0:
                self._current.add("any_key")
            self._call_4_combs(key)
            
    def on_release(self, key):
        self._last_press = 0
        if key in TkKeys.tk_mods.values():
            self._mods.discard(str(key))
        if self._anykey>0:
            self._current.discard("any_key")
        try:
            self._current.remove(key)
            self._log("on_release2 {}".format(key))
            self._call_4_combs(key)
        except KeyError:
            pass

    def on_move(self, x, y):
        if self._on_move:
            self._current.add("Motion")
            self._call_4_combs("Motion", x, y)
            self._current.discard("Motion")
            
    def on_click(self, x, y, button, pressed):
        #self._log('{0} {1} at {2}'.format(button, 'Pressed' if pressed else 'Released', (x, y)))
        if pressed:
            self._current.add(str(button))
            self._repeated = self._multi_clic(button)
        else:
            self._current.discard(str(button))
        self._on_move = pressed #detect motion only when button pressed
        self._call_4_combs(button, x, y)
            
    def on_scroll(self, x, y, dx, dy):
        #self._log('Mousewheel {0} at {1}'.format( 'down' if dy < 0 else 'up',(x, y)))
        self._current.add("Mousewheel")
        self._call_4_combs("Mousewheel", x, y, dx, dy)
        self._current.discard("Mousewheel")

def test():
    import tkinter, time

    def callback1(e):
        print('CALLBACK1 E:'+str(e) +"  ["+ threading.currentThread().getName() +"]")
        time.sleep(5)
        print("exiting callback1")

    def callback2(e):
        print('Callback2 fired:'+str(e))
        time.sleep(5)
        print("exiting callback2")  

    def callback3(e):
        print('CALLBACK3 E:'+str(e) +"  ["+ threading.currentThread().getName() +"]")
        if threading.currentThread()==threading.main_thread():
            global bg2,  logger
            bg2.gbind("<KeyPress>",logger.logger)
            # bg2gbind("<1>",mouselogger)
            bg2.gbind("<2>",logger.logger)
            bg2.gbind("<3>",logger.logger)
            bg2.gbind("<Mousewheel>",logger.logger)
    def callback4(e):
        print('CALLBACK4. Event:'+str(e))
        bg1.gunbind('<Triple-KeyRelease-f>', callback4)
        
    def exitall(e=None):
        print('exitall: exiting')
        bg1.stop()
        root.event_generate("<<QUIT>>")

    def quit(*args):
        root.destroy()

    logging.basicConfig(level=logging.DEBUG)
    bg1 = BindGlobal(logger=logging.getLogger(__name__))
    print("[ left-clic mouse while 'Menu' Key is pressed ]->callback1")
    bg1.gbind("<Menu-1>",callback1)
    print("[ double-clic over 'c' key while 'Right-Control' presed ]->callback2")
    bg1.gbind("<Double-Control_R-c>",callback2)
    print("[ Triple clic over 'Right Shift' key ]")
    bg1.gbind("<Triple-Shift_R>",lambda e: print("test:"+str(e)))
    print("[4-clic over 'f' key, but on release] -> callback3 + callback4")
    bg1.gbind("<Quadruple-KeyRelease-f>",callback3)
    bg1.gbind("<Quadruple-KeyRelease-f>",callback4, '+')
    bg1.gbind("<65027>",lambda e: print("ALT-GR in LINUX"+str(e)))
    print("[ global begin drag with mouse left button ] ")
    bg1.gbind("<Motion-Button1>",lambda e: print("DRAG:"+str(e)))
    print("[ Win + Left Alt, when release ] ")
    bg1.gbind("<Command-Alt_L-KeyRelease>",lambda e: print("WIN+Alt:"+str(e)))
    print("[ Triple clic over 'Esc' key to exit]")
    bg1.gbind("<Triple-Escape>",exitall)
    # print("[ press any key ]-> callback5")
    # bg1.gbind("<KeyPress>",callback5)
    bg1.start()

    root = tkinter.Tk()
    root.bind("<<QUIT>>", quit)   # tkinter bind to custom event
    root.mainloop()
    bg1.stop()

if __name__ == '__main__':
    test()

