# Nyan

This is a WIP fork of [replit-play](https://github.com/replit/play) focused on achieving feature parity
with Scratch.


## Tods

- [ ] implement `@foreach_sprite(tag=None)` decorator which will be used for attaching a script to multiple
sprites at once. This will be particularly useful for forever loops that should be running independently
for each sprite
- [ ] maybe a camera should be implemented? should be useful for things like screen shake.
- [ ] add scratch effects such as fisheye, whirl, pixlate, etc
- [ ] add music support (start, stop, fade, volume, etc).
- [ ] add tone support. A good example is pygame zero
- [ ] add spaceship and flappy bird example
- [ ] add custom events
- [ ] determine if sprite or drawable is the right base term. i.e can shapes (circle, rect) and font be called a sprite