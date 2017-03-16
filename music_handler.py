import os, pygame

music_folder = os.path.join("res", "music")

def music_file(filename):
    """Return the relative path to a music file.
    This method is for convenience only.
    """
    return os.path.join(music_folder, filename)

tracks = {
    "levels": [
        music_file("ozzed__shingle_tingle.ogg"),
        music_file("ozzed__shell_shock_shake.ogg"),
        music_file("ozzed__human_factory_reset.ogg")
    ],
    "bracket":       music_file("kulor__oceanfloor.ogg"),
    "continue":      music_file("chiptune__under_my_bed.ogg"),
    "game_over":     music_file("gameover.wav"),
    "congrats":      music_file("fishyash__coasting_into_the_sunset.ogg")
}

def play_track(name):
    """Play a track from the list."""
    pygame.mixer.music.load(tracks[name])
    _play()

def play_level_track(level):
    """Play a level's track.
    anything < 0: random"""
    if level < 0:
        import random
        rand = random.randrange(0, len(tracks["levels"]))
        pygame.mixer.music.load(tracks["levels"][rand])
    else:
        pygame.mixer.music.load(tracks["levels"][level])
    _play()

def _play():
    pygame.mixer.music.set_volume(.7)
    pygame.mixer.music.play()

def fadeout():
        pygame.mixer.music.fadeout(250)
