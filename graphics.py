
#function that increases the resolution in windows
def set_dpi_awarness():
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwarness(1)
    except:
        pass

# class that contains the suitable colours for UI
class Colour():
    def __init__(self):
        self.combinations=[{ "colour_primary": "#1e698d",
                        "colour_secondary": "#789fbb",
                        "colour_light_background": "#c2d5db",
                        "colour_light_text": "#eee",
                        "colour_dark_text": "#131925"
                        },
                      {
                            "colour_primary": "#031163",
                            "colour_secondary": "#1978a5",
                            "colour_light_background": "#1978a5",
                            "colour_light_text": "#eee",
                            "colour_dark_text": "#b9925e",
                      },
                      {
                          "colour_primary": "#336b87",
                          "colour_secondary": "#90afc5",
                          "colour_light_background": "#336b87",
                          "colour_light_text": "#eee",
                          "colour_dark_text": "#2a3132"
                      },
                      {
                          "colour_primary": "#1e3d59",
                          "colour_secondary": "#1E2761",
                          "colour_light_background": "#f5f0e1",
                          "colour_light_text": "#eee",
                          "colour_dark_text": "#1e3d59",
                      },
                      {
                          "colour_primary": "#1e2761",
                          "colour_secondary": "#408ec6",
                          "colour_light_background": "#fff",
                          "colour_light_text": "#eee",
                          "colour_dark_text": "#8a307f",
                      },
                     {
                               "colour_primary": "#1e3d59",
                               "colour_secondary": "#1E2761",
                               "colour_light_background": "#1e3d59",
                               "colour_light_text": "#eee",
                               "colour_dark_text": "#f5f0e1",
                     },
                     {
                               "colour_primary": "#343148",
                               "colour_secondary": "#1E2761",
                               "colour_light_background": "#343148",
                               "colour_light_text": "#A2A2A1",
                               "colour_dark_text": "#D7C49E",
                     },
                    {
                               "colour_primary": "#2A2B2D",
                               "colour_secondary": "#1E2761",
                               "colour_light_background": "#2A2B2D",
                               "colour_light_text": "#ec96a4",
                               "colour_dark_text": "#D7C49E",
                    },
                    {
                               "colour_primary": "#1f3044",
                               "colour_secondary": "#646c79",
                               "colour_light_background": "#1f3044",
                               "colour_light_text": "#A2A2A1",
                               "colour_dark_text": "#eee",
                    },
                    {
                               "colour_primary": "#425664",
                               "colour_secondary": "#3C6478",
                               "colour_light_background": "#425664",
                               "colour_light_text": "#dadedf",
                               "colour_dark_text": "#F2F3F4",
                    },
                    {
                               "colour_primary": "#1e3d59",
                               "colour_secondary": "#1e3d59",
                               "colour_light_background": "#1e3d59",
                               "colour_light_text": "#C1C7C9",
                               "colour_dark_text": "#f5f0e1",
                    },
                    ]