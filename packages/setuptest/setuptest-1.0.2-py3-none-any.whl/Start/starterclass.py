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

        Please, ensure the correct values - then you can click the buttons for the Setup, Install and Tests in the given order (top - down):
         1. Make db-tables
         2. Create Super-Admin
         3. Create First Project
         4. Create Projects 2-5
         5. Create a WBS
         6. Make Posts
         7. Create UserProfile 
        
        Finally, after the execution of all 7 scripts you have made a rough testing of fundamental functionalities - and
        you do receive a populated example project.
        
        You can keep that project for testing-purposes for testing the application and to show you & your team some functionalities
        for getting acquainted to the app and for helping you with the first steps for your own project.
        
        
        
        Congratulations for using the CCS by the way - it is a unique solution in many ways..
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
        self.fdBtn = tk.Button(master=self.frame, text="SETUP",  width=15, bg="orange2", activebackground="chartreuse2",
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
       # self.okLabel = tk.Label(self.frame, text="Install with these values:", fg="OrangeRed4", bg="salmon1", font="Verdana 13",
        #                        justify="center", borderwidth=2, relief="groove")
       # self.okLabel.grid(column=1, row=30, sticky=tk.E)

        # run button mit function call:
        #self.okBtn = tk.Button(master=self.frame, text="INSTALL", width=15, bg="firebrick1", activebackground="tomato2",
        #                       highlightbackground="orange2", highlightcolor="orchid2", command=self.runsetup)
        #self.okBtn.grid(column=2, row=30, sticky=tk.W, padx=5, pady=5)
    # ----


        # start info-label with execution buttons of the selected setup-install-tests button:
        self.setupInfoLabel = tk.Label(self.frame, text="Click the buttons to install with these values:", fg="OrangeRed4", bg="gold",
                            font="Verdana 13",
                            justify="center", borderwidth=2, relief="groove")
        self.setupInfoLabel.grid(column=1, row=30, sticky=tk.E)
# start setup buttons:
        # run button setup database tables via function call makedb:
        self.dbBtn = tk.Button(master=self.frame, text="1. Make db-tables", width=15, bg="gold", activebackground="chartreuse2",
                           highlightbackground="light salmon", highlightcolor="orchid2", command=self.makedb)
        self.dbBtn.grid(column=2, row=31, sticky=tk.W, padx=5, pady=5)
        # ----

        # run button register SuperAdminables via function call regadmin:
        self.dbBtn = tk.Button(master=self.frame, text="2. Create Super-Admin", width=15, bg="gold",
                           activebackground="chartreuse2",
                           highlightbackground="light salmon", highlightcolor="orchid2", command=self.regadmin)
        self.dbBtn.grid(column=2, row=32, sticky=tk.W, padx=5, pady=5)
        # ----

        # run button setup 1st Project via function call makeproject1:
        self.dbBtn = tk.Button(master=self.frame, text="3. Create First Project", width=15, bg="gold",
                           activebackground="chartreuse2",
                           highlightbackground="light salmon", highlightcolor="orchid2", command=self.makeproject1)
        self.dbBtn.grid(column=2, row=33, sticky=tk.W, padx=5, pady=5)
        # ----

        # run button setup Project 2-5 via function call makeproject4:
        self.dbBtn = tk.Button(master=self.frame, text="4. Create Projects 2-5", width=15, bg="gold",
                           activebackground="chartreuse2",
                           highlightbackground="light salmon", highlightcolor="orchid2", command=self.makeproject4)
        self.dbBtn.grid(column=2, row=34, sticky=tk.W, padx=5, pady=5)
        # ----


# start test buttons:
    # run the pytest - make wbs - Tests/test_loginCreateProjectCreateWBS.py on button-click:
        self.dbBtn = tk.Button(master=self.frame, text="5. Create a WBS", width=15, bg="SteelBlue1",
                           activebackground="chartreuse2",
                           highlightbackground="light cyan", highlightcolor="gold", command=self.makewbs)
        self.dbBtn.grid(column=2, row=35, sticky=tk.W, padx=5, pady=5)
        # ----


    # run the pytest - make posts (iterative repetitive post and direct- answer for every wbs-level):
        self.dbBtn = tk.Button(master=self.frame, text="6. Make Posts", width=15, bg="SteelBlue1",
                           activebackground="chartreuse2",
                           highlightbackground="light cyan", highlightcolor="gold", command=self.makeposts)
        self.dbBtn.grid(column=2, row=36, sticky=tk.W, padx=5, pady=5)
        # ----

    # run the pytest - login and create a user-profile for the Super-Admin with personality-assessment and CFLX test:
        self.dbBtn = tk.Button(master=self.frame, text="7. Create UserProfile", width=15, bg="SteelBlue1",
                           activebackground="chartreuse2",
                           highlightbackground="light cyan", highlightcolor="gold", command=self.makeprofile)
        self.dbBtn.grid(column=2, row=37, sticky=tk.W, padx=5, pady=5)
        # ----


# run all 7 at once  - the complete setup install and test walk-through performed with one button click:

        self.allBtn = tk.Button(master=self.frame, text="RUN ALL 7", width=15, bg="firebrick1",
                           activebackground="chartreuse2",
                           highlightbackground="DarkOrange1", highlightcolor="gold", command=self.runsetup_all)
        self.allBtn.grid(column=2, row=38, sticky=tk.W, padx=5, pady=5)
    # ----


    # Bring tkinter to the screen via mainloop:
        self.top.mainloop()

## start: neu mit os.path:

    def setup(self):
        import os
        pfad = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../Conf')
        dateiname = "test_configVars.py"
        datei = os.path.join(pfad, dateiname)

        try:
         #   fobj = open(datei, "r")
            webbrowser.open(datei)
        except IOError:
            print
            'Could not open the ' + datei + ' !'
            print
            'Please check, the PATH.'
        else:
            print
            "OK, did work."
         #   fobj.close()

## unten: alt
    # SETUP function (if value is set to "not-set-yet":
    def setup_alt(self):
        webbrowser.open("../Conf/test_configVars.py")
        exit()

    # test if user did enter IP or localhost:
    def testempty(self):
        if cfg.ccsIP == "not-set-yet":
            print("the value for the IP or localhost is not set")
         #   mssgbx.showinfo("ERROR - VALUES not set!", """Check the README.md, delete & reinstall the setuptest.""")
            self.setup()
           # webbrowser.open("./Conf/test_configVars.py")
            exit()




# defs of RunSetups/ pytest scripts
    # run the pytest - make databases - RunSetups/test_ini_1_createTables.py on button-click:
    def makedb(self):
        self.testempty()
        print("database-table creation scripts triggered. Skips, if tables exist already.")
        pytest.main(['../RunSetups/test_ini_1_createTables.py'])

    # run the pytest - create a Super-Admin:
    def regadmin(self):
        self.testempty()
        print("Super Admin creation script triggered. Fails, if name already exists.")
        pytest.main(['../RunSetups/test_ini_2_registerSuperadmin.py'])

    # run the pytest - create a first project:
    def makeproject1(self):
        self.testempty()
        print("1st Project creation script triggered. Overwrites Parameters if slot 1 is already populated.")
        pytest.main(['../RunSetups/test_ini_3_1stProjectSetup.py'])

    # run the pytest - create a first project:
    def makeproject4(self):
        self.testempty()
        print("Project creation script for project 2 to 5 is triggered. Overwrites Parameters of project, if slot 2,3,4 or 5 is already populated.")
        pytest.main(['../RunSetups/test_ini_4_4ProjectsSetup.py'])

# defs of Tests/ pytest scripts
    # run the pytest - make wbs - Tests/test_loginCreateProjectCreateWBS.py on button-click:
    def makewbs(self):
        self.testempty()
        print("login and create a project-name and a wbs script was triggered. Throws errors and exits if project already exists.")
        pytest.main(['../Tests/test_loginCreateProjectCreateWBS.py'])

    # run the pytest - make posts (iterative repetitive post and direct- answer for every wbs-level):
    def makeposts(self):
        self.testempty()
        print("Super Admin logs in and starts making posts and direct answers -will throw errors if posts already exists.")
        pytest.main(['../Tests/test_loginMakePosts.py'])

    # run the pytest - login and create a user-profile for the Super-Admin with personality-assessment and CFLX test:
    def makeprofile(self):
        self.testempty()
        print("Super Admin login and create a user-profile for the Super-Admin with personality-assessment and CFLX test.")
        pytest.main(['../Tests/test_loginPersProfileComplete.py'])

    # run the pytest (defined by __main__.py) on button-click:
    def runsetup_all(self):
        self.testempty()
        print("The run all 7 setup & installation steps at once was triggered ...")
        pytest.main(['../RunSetups/test_ini_1_createTables.py'])
        pytest.main(['../RunSetups/test_ini_2_registerSuperadmin.py'])
        pytest.main(['../RunSetups/test_ini_3_1stProjectSetup.py'])
        pytest.main(['../RunSetups/test_ini_4_4ProjectsSetup.py'])
        pytest.main(['../Tests/test_loginCreateProjectCreateWBS.py'])
        pytest.main(['../Tests/test_loginMakePosts.py'])
        pytest.main(['../Tests/test_loginPersProfileComplete.py'])

