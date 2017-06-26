import Tkinter as tk
import time
import rospy
from remote_operator import msg


REFRESH_RATE = 1.0

class GUI():
    def __init__(self, rd, ros_lock):
        self.rd = rd
        self.ros_lock = ros_lock
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.window_close_callback)
        self.root.geometry("500x500")
        self.label = tk.Label(text="window")
        self.label.pack()
        self.x_slider = tk.Scale(self.root, command=self.x_slider_callback, from_=1000, label="X axis", to=-1000)
        self.x_slider.pack()
        self.teleop_command = msg.TeleopCommand()
        self.teleop_command.joysticks.append(msg.JoystickMessage())
        self.teleop_command.joysticks[0].l_x_axis = self.teleop_command.joysticks[0].l_y_axis = self.teleop_command.joysticks[0].l_twist_axis = 0

        self.gui_state = tk.IntVar()
        self.gui_state.set(msg.StateCommand.DISABLED)

        states = [("Disabled", msg.StateCommand.DISABLED), ("Enabled Teleop", msg.StateCommand.ENABLED_TELEOP), ("Enabled Auto", msg.StateCommand.ENABLED_AUTO), ("Persistent Enable Auto", msg.StateCommand.PERSISTENT_ENABLE_AUTO), ("Persistent Enable Teleop", msg.StateCommand.PERSISTENT_ENABLE_TELEOP)]

        for txt, val in states:
            tk.Radiobutton(self.root, text=txt, padx=20, variable=self.gui_state, command=self.state_radiobutton_callback, value=val).pack()

        self.auto_refresh()
        self.root.mainloop()

    def window_close_callback(self):
        rospy.signal_shutdown("Window closed")

    def state_radiobutton_callback(self):
        self.rd.set_state(self.gui_state.get())

    def loop(self):
        now = time.strftime("%H:%M:%S")
        self.label.configure(text=now)

    def x_slider_callback(self, new_value):
        print "Called"
        self.teleop_command.joysticks[0].l_x_axis = float(new_value) / 1000
        self.rd.send_teleop_command(self.teleop_command)

    def auto_refresh(self):
        with self.ros_lock:
            if rospy.is_shutdown():
                self.root.destroy()
                return
        tinit = time.time()
        self.loop()
        tdif = time.time() - tinit
        sleep_time = int((1 / REFRESH_RATE) * 1000 - tdif)
        if sleep_time < 0:
            sleep_time = 0
        self.root.after(sleep_time, self.auto_refresh)