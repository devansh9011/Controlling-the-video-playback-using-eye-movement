import gi
import vlc
import cv2
import numpy as np
import time
from threading import Thread

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# from gi.repository import GdkX11
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')


class ApplicationWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Python-Vlc Media Player")
        self.player_paused = False
        self.is_player_active = False
        self.connect("destroy", Gtk.main_quit)

        # Creating media playback buttons
        self.playback_button = Gtk.Button()
        self.stop_button = Gtk.Button()

        # initialising the images
        self.play_image = Gtk.Image.new_from_icon_name("gtk-media-play", Gtk.IconSize.MENU)
        self.pause_image = Gtk.Image.new_from_icon_name("gtk-media-pause", Gtk.IconSize.MENU)
        self.stop_image = Gtk.Image.new_from_icon_name("gtk-media-stop", Gtk.IconSize.MENU)

        # setting the default image for the buttons
        self.playback_button.set_image(self.play_image)
        self.stop_button.set_image(self.stop_image)

    def show(self):
        self.show_all()

    def setup_objects_and_events(self):

        self.playback_button.connect("clicked", self.toggle_player_playback)

        self.stop_button.connect("clicked", self.stop_player)

        self.draw_area = Gtk.DrawingArea()

        self.draw_area.set_size_request(800, 400)

        self.draw_area.connect("realize", self._realized)

        # virtual horizontal box which contains the both media playback buttons
        self.hbox = Gtk.Box(spacing=6)
        self.hbox.pack_start(self.playback_button, True, True, 0)
        self.hbox.pack_start(self.stop_button, True, True, 0)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.vbox)
        self.vbox.pack_start(self.draw_area, True, True, 0)
        self.vbox.pack_start(self.hbox, False, False, 0)

    def stop_player(self, widget, data=None):
        self.player.stop()
        self.is_player_active = False
        self.playback_button.set_image(self.play_image)

    def toggle_player_playback(self, widget, data=None):

        # if player is not active and is not paused
        if self.is_player_active == False and self.player_paused == False:
            self.player.play()
            self.playback_button.set_image(self.pause_image)
            self.is_player_active = True

        elif self.is_player_active and self.player_paused:
            self.player.play()
            self.playback_button.set_image(self.pause_image)
            self.player_paused = False

        elif self.is_player_active and self.player_paused == False:
            self.player.pause()
            self.playback_button.set_image(self.play_image)
            self.player_paused = True
        else:
            pass

    def pause_player(self, widget, data=None):
        if self.is_player_active:
            self.player.pause()
            self.playback_button.set_image(self.play_image)
            self.player_paused = True

    def resume_player(self, widget, data=None):
        if self.is_player_active:
            self.player.play()
            self.playback_button.set_image(self.pause_image)
            self.player_paused = False

    def _realized(self, widget, data=None):
        self.vlcInstance = vlc.Instance("--no-xlib")
        self.player = self.vlcInstance.media_player_new()
        win_id = widget.get_window().get_xid()
        self.player.set_xwindow(win_id)
        self.player.set_mrl(MRL)
        self.player.play()
        self.playback_button.set_image(self.pause_image)
        self.is_player_active = True


class webcam:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def detect_face(self):
        ret, frame = self.cap.read()
        frame = cv2.add(frame, np.array([30.0]))  # adding brightness to the frame
        face_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # converting the coloured image into black and white
        detected = False
        face_rectangle = face_cascade.detectMultiScale(face_img, scaleFactor=1.4, minNeighbors=5)  # detecting for face
        for (x, y, w, h) in face_rectangle:
            cv2.rectangle(face_img, (x, y), (x + w, y + h), (255, 255, 255),
                          5)  # drawing rectangle over the detected face
            detected = True
            face = face_img[y:y + h, x:x + w]  # cropping the face rectangle
            eyes_rectangle = eye_cascade.detectMultiScale(face)  # detection for eyes in the face
            for (xx, yy, ww, hh) in eyes_rectangle:
                cv2.rectangle(face_img, (xx + x, y + yy), (x + xx + ww, y + yy + hh), (255, 0, 0),
                              2)  # drawing rectangle over the detected eyes

        cv2.imshow('face detect', face_img)
        return detected

    def __del__(self):
        self.cap.release()


def foo():
    global seconds, window
    window.show()
    Gtk.main()
    while True:
        flag = wb.detect_face()
        if not flag:
            if not window.player_paused:
                window.pause_player()
            else:
                if time.time() - seconds >= 20:
                    window.player.stop()
                    window.vlcInstance.release()
        else:
            if window.player_paused:
                window.resume_player()
            seconds = time.time()

        window.player.stop()
        window.vlcInstance.release()


MRL = '/home/devil/Downloads/video.mp4'
window = ApplicationWindow()
window.setup_objects_and_events()

seconds = time.time()
wb = webcam()
foo();
# Thread(target=foo, args=()).start()

# window.show()
# Gtk.main()
# window.player.stop()
# window.vlcInstance.release()

