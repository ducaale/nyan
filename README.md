# nyan

This is a WIP fork of [replit-play](https://github.com/replit/play) focused on achieving feature parity
with Scratch.


## Todos

- [x] implement `@nyan.foreach_sprite()` decorator which will be used for attaching a script to multiple
sprites at once. This will be particularly useful for forever loops that should be running independently
for each sprite
- [ ] maybe a camera should be implemented? should be useful for things like screen shake.
- [ ] add scratch effects such as fisheye, whirl, pixlate, etc
- [x] add music support (play, stop, pause, volume, etc).
- [x] add flappy bird example
- [x] add custom events
- [x] add nyan_packager
- [x] add option to pass icon in nyan_packager
- [ ] determine if sprite or drawable is the right base term. i.e can shapes (circle, rect) and font be called a sprite?
- [x] add @sprite.when_clicked
- [ ] copy replit-play docs
- [ ] `@nyan.gamestate()` decorator for running script in a particular state
- [ ] global object for storing data https://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute
- [x] add scratch like timer that can be resetted
- [ ] add support for changing backdrop