namespace SpriteKind {
    export const Boy = SpriteKind.create()
    export const Ghost = SpriteKind.create()
}

//  Event handler for when the player sprite overlaps with a specific tile.
//  Calls the changeLevel function with levelNumber 2.
scene.onOverlapTile(SpriteKind.Player, assets.tile`
        tilemap9
    `, function on_overlap_tile(sprite2: Sprite, location: tiles.Location) {
    changeLevel(2)
})
//  Creates a projectile sprite and plays a sound effect based on the ShotDirection.
controller.A.onEvent(ControllerButtonEvent.Pressed, function on_a_pressed() {
    
    if (ShotDirection == 1) {
        projectile = sprites.createProjectileFromSprite(assets.image`
            proyectile1
        `, girl, 100, 0)
        music.play(music.createSoundEffect(WaveShape.Sine, 400, 600, 255, 0, 100, SoundExpressionEffect.Vibrato, InterpolationCurve.Curve), music.PlaybackMode.UntilDone)
    } else {
        projectile = sprites.createProjectileFromSprite(assets.image`
            proyectile0
        `, girl, -100, 0)
        music.play(music.createSoundEffect(WaveShape.Sine, 400, 600, 255, 0, 100, SoundExpressionEffect.Vibrato, InterpolationCurve.Curve), music.PlaybackMode.UntilDone)
    }
    
})
//  Creates animations for the girl sprite.
function createAnimations() {
    characterAnimations.loopFrames(girl, assets.animation`
            girlRight
        `, 500, characterAnimations.rule(Predicate.MovingRight))
    characterAnimations.loopFrames(girl, assets.animation`
            girlLeft
        `, 500, characterAnimations.rule(Predicate.MovingLeft))
}

//  Game over if girl steps on final Boss
sprites.onOverlap(SpriteKind.Projectile, SpriteKind.Enemy, function on_on_overlap(sprite32: Sprite, otherSprite32: Sprite) {
    
    sprites.destroy(projectile, effects.spray, 100)
    bossHealth += -1
    if (bossHealth == 0) {
        sprites.destroyAllSpritesOfKind(SpriteKind.Enemy)
        game.gameOver(true)
    }
    
})
//  Makes the ghost sprites follow the girl sprite.
function ghostsFollow() {
    for (let value of collectedBoys) {
        spriteutils.placeAngleFrom(value, 0, -30, girl)
        spriteutils.placeAngleFrom(value, 0, -30, value)
        value.follow(girl, 5)
    }
}

//  Event handler for when the left button is pressed.
//  Sets the ShotDirection to 2.
controller.left.onEvent(ControllerButtonEvent.Pressed, function on_left_pressed() {
    
    ShotDirection = 2
})
//  Changes the level based on the levelNumber parameter.
//  Destroys all enemy sprites of kind SpriteKind.enemy.
//  If levelNumber is 2, sets the current tilemap, places the girl sprite on a random tile,
//  creates a boss sprite, places it on a random tile, and sets the bossHealth to 5.
//  Sets the background color to 13.
function changeLevel(levelNumber: number) {
    
    sprites.destroyAllSpritesOfKind(SpriteKind.Enemy)
    if (levelNumber == 2) {
        tiles.setCurrentTilemap(tilemap`
            level0
        `)
        tiles.placeOnRandomTile(girl, assets.tile`
            myTile19
        `)
        boss = sprites.create(assets.image`
            finalBoss
        `, SpriteKind.Enemy)
        tiles.placeOnRandomTile(boss, assets.tile`
            myTile20
        `)
        bossHealth = 5
    }
    
    scene.setBackgroundColor(13)
}

//  Event handler for when the projectile sprite overlaps with a Boy sprite.
//  Destroys the projectile and the otherSprite.
//  Creates a Ghost sprite and increases the score by 1.
sprites.onOverlap(SpriteKind.Projectile, SpriteKind.Boy, function on_on_overlap2(sprite: Sprite, otherSprite: Sprite) {
    sprites.destroy(projectile, effects.spray, 100)
    sprites.destroy(otherSprite, effects.spray, 100)
    collectedBoys.push(sprites.create(assets.image`
        cuteGhost
    `, SpriteKind.Ghost))
    info.changeScoreBy(1)
})
sprites.onOverlap(SpriteKind.Player, SpriteKind.Enemy, function on_on_overlap3(sprite3: Sprite, otherSprite3: Sprite) {
    sprites.destroyAllSpritesOfKind(SpriteKind.Enemy)
    info.setLife(0)
    music.play(music.melodyPlayable(music.wawawawaa), music.PlaybackMode.UntilDone)
})
controller.right.onEvent(ControllerButtonEvent.Pressed, function on_right_pressed() {
    
    ShotDirection = 1
})
//  Shows welcome message and how to play before game starts
function showMenu() {
    scene.setBackgroundColor(11)
    game.setDialogTextColor(10)
    game.setDialogFrame(assets.image`
        toki
    `)
    game.showLongText("Welcome to Tokimeki! Will you find your biggest crush?", DialogLayout.Full)
    game.showLongText("How to play: Press A to shoot and charm all the boys before running out of time", DialogLayout.Full)
}

//  Defines settings for the game
function tokimekiSettings() {
    game.splash("Press A to start")
    info.startCountdown(59)
    info.setLife(3)
    info.setScore(0)
}

let boyToAdd : Sprite = null
let boss : Sprite = null
let bossHealth = 0
let projectile : Sprite = null
let ShotDirection = 0
let collectedBoys : Sprite[] = []
let girl : Sprite = null
showMenu()
tiles.setCurrentTilemap(tilemap`
    level2
`)
tokimekiSettings()
changeLevel(1)
girl = sprites.create(assets.image`
    mainCharacter
`, SpriteKind.Player)
tiles.placeOnRandomTile(girl, assets.tile`
    spawn
`)
let _let = sprites.create(assets.image`
    cuteGhost
`, SpriteKind.Player)
scene.cameraFollowSprite(girl)
controller.moveSprite(girl, 100, 100)
createAnimations()
collectedBoys = []
ShotDirection = 1
//  Updates ghosts that follow the girl
game.onUpdateInterval(500, function on_update_interval() {
    ghostsFollow()
})
//  Makes boys appear
game.onUpdateInterval(3000, function on_update_interval2() {
    
    let aliveBoys : Sprite[] = []
    boyToAdd = sprites.create(assets.image`
        boyCharacter
    `, SpriteKind.Boy)
    boyToAdd.setPosition(randint(0, scene.screenWidth()), 109)
    aliveBoys.push(boyToAdd)
})
