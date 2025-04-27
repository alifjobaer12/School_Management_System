
class SlideAnimation:
    def __init__(self, anime_y, frame_main, login_window):
        # global anime_y, frame_main, login_window
        self.frame = frame_main
        self.window = login_window
        self.anime_y = anime_y
        # self.speed = speed
        # self.delay = delay

    def slide_down(self, callback=None):
        self.anime_y += 3
        if self.anime_y <= 200:
            self.frame.place(x=320, y=self.anime_y, anchor="center")
            self.window.after(2, lambda: self.slide_down(callback))
        else:
            if callback:
                callback()
    
    # def slide_up(self, callback=None):
    #     self.anime_y -= 3
    #     if self.anime_y >= -203:
    #         self.frame.place(x=320, y=self.anime_y, anchor="center")
    #         self.window.after(2, lambda: self.slide_up(callback))
    #     else:
    #         if callback:
    #             callback()
