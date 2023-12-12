@namespace
class SpriteKind:
    Boy = SpriteKind.create()
    Ghost = SpriteKind.create()
# Event handler for when the player sprite overlaps with a specific tile.
# Calls the changeLevel function with levelNumber 2.

def on_overlap_tile(sprite2, location):
    changeLevel(2)
scene.on_overlap_tile(SpriteKind.player,
    assets.tile("""
        tilemap9
    """),
    on_overlap_tile)

# Creates a projectile sprite and plays a sound effect based on the ShotDirection.

def on_a_pressed():
    global projectile
    if ShotDirection == 1:
        projectile = sprites.create_projectile_from_sprite(assets.image("""
            proyectile1
        """), girl, 100, 0)
        music.play(music.create_sound_effect(WaveShape.SINE,
                400,
                600,
                255,
                0,
                100,
                SoundExpressionEffect.VIBRATO,
                InterpolationCurve.CURVE),
            music.PlaybackMode.UNTIL_DONE)
    else:
        projectile = sprites.create_projectile_from_sprite(assets.image("""
            proyectile0
        """), girl, -100, 0)
        music.play(music.create_sound_effect(WaveShape.SINE,
                400,
                600,
                255,
                0,
                100,
                SoundExpressionEffect.VIBRATO,
                InterpolationCurve.CURVE),
            music.PlaybackMode.UNTIL_DONE)
controller.A.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)

# Creates animations for the girl sprite.
def createAnimations():
    characterAnimations.loop_frames(girl,
        assets.animation("""
            girlRight
        """),
        500,
        characterAnimations.rule(Predicate.MOVING_RIGHT))
    characterAnimations.loop_frames(girl,
        assets.animation("""
            girlLeft
        """),
        500,
        characterAnimations.rule(Predicate.MOVING_LEFT))
# Game over if girl steps on final Boss

def on_on_overlap(sprite32, otherSprite32):
    global bossHealth
    sprites.destroy(projectile, effects.spray, 100)
    bossHealth += -1
    if bossHealth == 0:
        sprites.destroy_all_sprites_of_kind(SpriteKind.enemy)
        game.game_over(True)
sprites.on_overlap(SpriteKind.projectile, SpriteKind.enemy, on_on_overlap)

# Makes the ghost sprites follow the girl sprite.
def ghostsFollow():
    for value in collectedBoys:
        spriteutils.place_angle_from(value, 0, -30, girl)
        spriteutils.place_angle_from(value, 0, -30, value)
        value.follow(girl, 5)
# Event handler for when the left button is pressed.
# Sets the ShotDirection to 2.

def on_left_pressed():
    global ShotDirection
    ShotDirection = 2
controller.left.on_event(ControllerButtonEvent.PRESSED, on_left_pressed)

# Changes the level based on the levelNumber parameter.
# Destroys all enemy sprites of kind SpriteKind.enemy.
# If levelNumber is 2, sets the current tilemap, places the girl sprite on a random tile,
# creates a boss sprite, places it on a random tile, and sets the bossHealth to 5.
# Sets the background color to 13.
def changeLevel(levelNumber: number):
    global boss, bossHealth
    sprites.destroy_all_sprites_of_kind(SpriteKind.enemy)
    if levelNumber == 2:
        tiles.set_current_tilemap(tilemap("""
            level0
        """))
        tiles.place_on_random_tile(girl, assets.tile("""
            myTile19
        """))
        boss = sprites.create(assets.image("""
            finalBoss
        """), SpriteKind.enemy)
        tiles.place_on_random_tile(boss, assets.tile("""
            myTile20
        """))
        bossHealth = 5
    scene.set_background_color(13)
# Event handler for when the projectile sprite overlaps with a Boy sprite.
# Destroys the projectile and the otherSprite.
# Creates a Ghost sprite and increases the score by 1.

def on_on_overlap2(sprite, otherSprite):
    sprites.destroy(projectile, effects.spray, 100)
    sprites.destroy(otherSprite, effects.spray, 100)
    collectedBoys.append(sprites.create(assets.image("""
        cuteGhost
    """), SpriteKind.Ghost))
    info.change_score_by(1)
sprites.on_overlap(SpriteKind.projectile, SpriteKind.Boy, on_on_overlap2)

def on_on_overlap3(sprite3, otherSprite3):
    sprites.destroy_all_sprites_of_kind(SpriteKind.enemy)
    info.set_life(0)
    music.play(music.melody_playable(music.wawawawaa),
        music.PlaybackMode.UNTIL_DONE)
sprites.on_overlap(SpriteKind.player, SpriteKind.enemy, on_on_overlap3)

def on_right_pressed():
    global ShotDirection
    ShotDirection = 1
controller.right.on_event(ControllerButtonEvent.PRESSED, on_right_pressed)

# Shows welcome message and how to play before game starts
def showMenu():
    scene.set_background_color(11)
    game.set_dialog_text_color(10)
    game.set_dialog_frame(assets.image("""
        toki
    """))
    game.show_long_text("Welcome to Tokimeki! Will you find your biggest crush?",
        DialogLayout.FULL)
    game.show_long_text("How to play: Press A to shoot and charm all the boys before running out of time",
        DialogLayout.FULL)
# Defines settings for the game
def tokimekiSettings():
    game.splash("Press A to start")
    info.start_countdown(59)
    info.set_life(3)
    info.set_score(0)
boyToAdd: Sprite = None
boss: Sprite = None
bossHealth = 0
projectile: Sprite = None
ShotDirection = 0
collectedBoys: List[Sprite] = []
girl: Sprite = None
showMenu()
tiles.set_current_tilemap(tilemap("""
    level2
"""))
tokimekiSettings()
changeLevel(1)
girl = sprites.create(assets.image("""
    mainCharacter
"""), SpriteKind.player)
tiles.place_on_random_tile(girl, assets.tile("""
    spawn
"""))
_let = sprites.create(assets.image("""
    cuteGhost
"""), SpriteKind.player)
scene.camera_follow_sprite(girl)
controller.move_sprite(girl, 100, 100)
createAnimations()
collectedBoys = []
ShotDirection = 1
# Updates ghosts that follow the girl

def on_update_interval():
    ghostsFollow()
game.on_update_interval(500, on_update_interval)

# Makes boys appear

def on_update_interval2():
    global boyToAdd
    aliveBoys: List[Sprite] = []
    boyToAdd = sprites.create(assets.image("""
        boyCharacter
    """), SpriteKind.Boy)
    boyToAdd.set_position(randint(0, scene.screen_width()), 109)
    aliveBoys.append(boyToAdd)
game.on_update_interval(3000, on_update_interval2)
