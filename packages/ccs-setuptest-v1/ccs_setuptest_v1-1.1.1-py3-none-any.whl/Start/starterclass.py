try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import webbrowser
import pytest
from Conf import test_configVars

cfg = test_configVars

from tkinter import Toplevel
import tkinter.messagebox as mssgbx


class VerticalScrolledFrame:
    """
    A vertically scrolled Frame that can be treated like any other Frame
    ie it needs a master and layout and it can be a master.
    :width:, :height:, :bg: are passed to the underlying Canvas
    :bg: and all other keyword arguments are passed to the inner Frame
    note that a widget layed out in this frame will have a self.master 3 layers deep,
    (outer Frame, Canvas, inner Frame) so
    if you subclass this there is no built in way for the children to access it.
    You need to provide the controller separately.
    """
    def __init__(self, master, **kwargs):
        width = kwargs.pop('width', None)
        height = kwargs.pop('height', None)
        bg = kwargs.pop('bg', kwargs.pop('background', None))
        self.outer = tk.Frame(master, **kwargs)

        self.vsb = tk.Scrollbar(self.outer, orient=tk.VERTICAL)
        self.vsb.pack(fill=tk.Y, side=tk.RIGHT)
        self.canvas = tk.Canvas(self.outer, highlightthickness=0, width=width, height=height, bg=bg)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas['yscrollcommand'] = self.vsb.set
        # mouse scroll does not seem to work with just "bind"; You have
        # to use "bind_all". Therefore to use multiple windows you have
        # to bind_all in the current widget
        self.canvas.bind("<Enter>", self._bind_mouse)
        self.canvas.bind("<Leave>", self._unbind_mouse)
        self.vsb['command'] = self.canvas.yview

        self.inner = tk.Frame(self.canvas, bg=bg)
        # pack the inner Frame into the Canvas with the topleft corner 4 pixels offset
        self.canvas.create_window(4, 4, window=self.inner, anchor='nw')
        self.inner.bind("<Configure>", self._on_frame_configure)

        self.outer_attr = set(dir(tk.Widget))

    def __getattr__(self, item):
        if item in self.outer_attr:
            # geometry attributes etc (eg pack, destroy, tkraise) are passed on to self.outer
            return getattr(self.outer, item)
        else:
            # all other attributes (_w, children, etc) are passed to self.inner
            return getattr(self.inner, item)

    def _on_frame_configure(self, event=None):
        x1, y1, x2, y2 = self.canvas.bbox("all")
        height = self.canvas.winfo_height()
        self.canvas.config(scrollregion = (0,0, x2, max(y2, height)))

    def _bind_mouse(self, event=None):
        self.canvas.bind_all("<4>", self._on_mousewheel)
        self.canvas.bind_all("<5>", self._on_mousewheel)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse(self, event=None):
        self.canvas.unbind_all("<4>")
        self.canvas.unbind_all("<5>")
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        """Linux uses event.num; Windows / Mac uses event.delta"""
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units" )
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units" )


class startclass:
    # Notification - new window for message on start via Toplevel:
    def __init__(self):
        self.fenster1 = tk.Tk()
        self.fenster1.title("Information about setting-up the values for installation & testing")

        self.infotxt = tk.Label(self.fenster1, text=""" NOTIFICATION:
        The values for the setup needed to be changed manually within the file:
        
        setuptest/Conf/test_configVars.py  
        
	BEFORE the installation.
        
	If you click the CONTINUE button below, all values declared within this test_configVars.py file will be shown to you.
        
        You can change these values by clicking the [SETUP] button - this button should open the file with your system's editor
        (notepad, gedit, TextEdit, nano ...). If this should fail, you need to open the file manually.
	Save the file somewhere, and replace the default one with it later in your new setuptest installation.
        Note: you need to uninstall the setuptest & redo the installation if the values shown to you do not match to your needs.
        Check the README.md for more information - its all well documented (uninstall info at the bottom).
        
        For entering the needed values, You will need:
         1. A (FREE) sendgrid account & 
         2. An E-Mail-Address with a PGP encryption.
        More details can be found in the comments of the test_configVars.py file.

        Please, ensure the correct values - then you can click the [INSTALL] button to use these values for:
         A) perform the final installation steps
        and
         B) creating a first example-project & run some automated testing walk-throughs 
        (for testing the application and to show you & your team some functionalities
        for getting acquainted to the app and for helping you with the first steps for your own project).
        
        Congratulations for using the CCS by the way - this is the next level of communication & collaboration
        in locally distributed project-teams.
        
        
        - CYCONET: across all borders.
        """,
        fg="orchid4", font="Verdana 10", justify="left", borderwidth=2, relief="groove").grid(column=0, row=0)

        # proceed on button click [CONTINUE]:
        self.fdBtn = tk.Button(master=self.fenster1, text="CONTINUE", width=15, bg="orange2",activebackground="dark orange", highlightbackground="red2", highlightcolor="green2", command=self.proceed)
                             #  command=lambda:[self.proceed(),self.fenster1.destroy()]) #
        self.fdBtn.grid(column=0, row=2, sticky=tk.W)
        # Bring tkinter fenster1 to the screen via mainloop:
        self.fenster1.mainloop()

    # NOTIFICATION END-------------------------------------------------
    def proceed(self):
       # self.fenster = tk.Tk()
        self.top = Toplevel()
        self.top.geometry('1100x600')
        self.top.title("Starter for CCS initial Installation & Testing")
        # start frame:
        self.frame = VerticalScrolledFrame(self.top,
                                               width=1000,
                                               borderwidth=2,
                                               relief=tk.SUNKEN,
                                               background="DarkSeaGreen1"
                                               )
        # frame.grid(column=0, row=0, sticky='nsew') # fixed size
        self.frame.pack(fill=tk.BOTH, expand=True)  # fill window

        #  self.infotxt.grid(column=0, row=0)

        # start open the config file via dialog:
        # start ok-label mit run button:
        # if the value is set to "not-set-yet", offer a button to make the settings:
        # if cfg.ccsIP == "nota-set-yet":
        # orange info & button:
        self.fdLabel = tk.Label(self.frame, text="Click [SETUP] to open test_configVars.py & change values:",
                           fg="DarkOrange3", bg="light goldenrod", font="Verdana 12", justify="center", borderwidth=2, relief="groove")
        self.fdLabel.grid(column=1, row=2, sticky=tk.W)
        self.fdBtn = tk.Button(master=self.frame, text="SETUP",  width=15, bg="orange2", activebackground="dark orange",
                               highlightbackground="red2", highlightcolor="green2", command=self.setup)
        self.fdBtn.grid(column=2, row=2, sticky=tk.W, padx=5, pady=5)

        # start labels for variables:
        # 11 variables (for 5 Projects.) +n projects => +n variables (for the project-numbers for the project-slots)
        # 1 IP or localhost:
        self.ipLabel = tk.Label(self.frame, text="Value for IP or localhost:", fg="purple4", background="DarkSeaGreen2")
        self.ipLabel.grid(column=1, row=3, sticky=tk.W)

        self.ipLabelv = tk.Label(self.frame, text=cfg.ccsIP, fg="purple4", background="DarkSeaGreen2")
        self.ipLabelv.grid(column=2, row=3, sticky=tk.W)

        # 2 sendgrid API Key:
        self.sgLabel = tk.Label(self.frame, text="Sendgrid API Key:", fg="maroon4", background="DarkSeaGreen2")
        self.sgLabel.grid(column=1, row=4, sticky=tk.W)
        self.sgLabelv = tk.Label(self.frame, text=cfg.sendgridAPIkey, fg="maroon4", background="DarkSeaGreen2")
        self.sgLabelv.grid(column=2, row=4, sticky=tk.W)

        # 3 project number1:
        self.p1Label = tk.Label(self.frame, text="Project NUMBER for slot 1:")
        self.p1Label.grid(column=1, row=5, sticky=tk.W)
        self.p1Labelv = tk.Label(self.frame, text=cfg.firstProjectNumber)
        self.p1Labelv.grid(column=2, row=5, sticky=tk.W)
        # 4 project number2:
        self.p2Label = tk.Label(self.frame, text="Project NUMBER for slot 2:")
        self.p2Label.grid(column=1, row=6, sticky=tk.W)
        self.p2Labelv = tk.Label(self.frame, text=cfg.secondProjectNumber)
        self.p2Labelv.grid(column=2, row=6, sticky=tk.W)
        # 5 project number3:
        self.p3Label = tk.Label(self.frame, text="Project NUMBER for slot 3:")
        self.p3Label.grid(column=1, row=7, sticky=tk.W)
        self.p3Labelv = tk.Label(self.frame, text=cfg.thirdProjectNumber)
        self.p3Labelv.grid(column=2, row=7, sticky=tk.W)
        # 6 project number4:
        self.p4Label = tk.Label(self.frame, text="Project NUMBER for slot 4")
        self.p4Label.grid(column=1, row=8, sticky=tk.W)
        self.p4Labelv = tk.Label(self.frame, text=cfg.fourthProjectNumber)
        self.p4Labelv.grid(column=2, row=8, sticky=tk.W)
        # 7 project number5:
        self.p5Label = tk.Label(self.frame, text="Project NUMBER for slot 5:")
        self.p5Label.grid(column=1, row=9, sticky=tk.W)
        self.p5Labelv = tk.Label(self.frame, text=cfg.fifthProjectNumber)
        self.p5Labelv.grid(column=2, row=9, sticky=tk.W)

        # 9 Super Admin's E-Mail / E-Mail of "User-Number-One":
        self.seLabel = tk.Label(self.frame, background="DarkGoldenrod1", text="Super Admin's E-Mail:")
        self.seLabel.grid(column=1, row=10, sticky=tk.W)
        self.seLabelv = tk.Label(self.frame, background="DarkGoldenrod1", text=cfg.usrNumberOneEmail)
        self.seLabelv.grid(column=2, row=10, sticky=tk.W)
        # 9 Super Admin / "User-Number-One":
        self.suLabel = tk.Label(self.frame, text="Super Admin's Name:")
        self.suLabel.grid(column=1, row=11, sticky=tk.W)
        self.suLabelv = tk.Label(self.frame, text=cfg.usrNumberOneName)
        self.suLabelv.grid(column=2, row=11, sticky=tk.W)
        # 10 Super Admin's Password:
        self.pwLabel = tk.Label(self.frame, text="Super Admin's Password:", fg="red4")
        self.pwLabel.grid(column=1, row=12, sticky=tk.W)
        self.pwLabelv = tk.Label(self.frame, text=cfg.usrNumberOnePW, fg="red4")
        self.pwLabelv.grid(column=2, row=12, sticky=tk.W)
        # 11 Super Admin's public PGP Key:
        self.pwLabel = tk.Label(self.frame, background="DarkGoldenrod1", text="Super Admin's public PGP-Key:")
        self.pwLabel.grid(column=1, row=13, sticky=tk.NW)
        self.pwLabelv = tk.Label(self.frame,  background="DarkGoldenrod2", text=cfg.usrNumberOnesPublicPGPkey, font="Verdana 9")
        self.pwLabelv.grid(column=2, row=13, sticky=tk.W)

    # start ok-label mit run button:
        self.okLabel = tk.Label(self.frame, text="Install with these values:", fg="OrangeRed4", bg="salmon1", font="Verdana 13",
                                justify="center", borderwidth=2, relief="groove")
        self.okLabel.grid(column=1, row=30, sticky=tk.E)
        # run button mit function call:
        self.okBtn = tk.Button(master=self.frame, text="INSTALL", width=15, bg="firebrick1", activebackground="tomato2",
                               highlightbackground="orange2", highlightcolor="orchid2", command=self.runsetup)
        self.okBtn.grid(column=2, row=30, sticky=tk.W, padx=5, pady=5)

# Erweiterung um die Tests mit
       # a) Infoblock "if click, then we perform"
       # b) mit den Runs:
       # 1. run All (execute pytest )Tests/
       # test_loginCreateProjectCreateWBS.py
       # test_loginMakePosts.py
       # test_loginPersProfileComplete.py

    # Bring tkinter to the screen via mainloop:
        self.top.mainloop()


    # SETUP function (if value is set to "not-set-yet":
    def setup(self):
        webbrowser.open("./Conf/test_configVars.py")
        exit()

    # test if user did enter IP or localhost:
    def testempty(self):
        if cfg.ccsIP == "not-set-yet":
            print("the value for the IP or localhost is not set")
            mssgbx.showinfo("ERROR - VALUES not set!", """Check the README.md, delete & reinstall the setuptest.""")
           # webbrowser.open("./Conf/test_configVars.py")
            exit()
    # run the pytest (defined by __main__.py) on button-click:
    def runsetup(self):
        self.testempty()
        pytest.main()
