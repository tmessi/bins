mplayer/mencoder notes
======================

```bash
mplayer dvd://1 -chapter 2 -vf cropdetect # display values for crop of black bars
```

```bash
mencode dvd://1 -ofps 24000/1001 -oac copy -ovc lavc -lavcopts vcodec=mpeg4:vbitrate=2400:v4mv:mbd=2:trell:cmp=3:subcmp=3:autoaspect:vpass=1 -vf pullup,softskip,crop=720:352:0:62,hqdn3d=2:1:2 -o movie.avi
```

Options details
---------------

+ `-ofps`: FPS of output, `24000/1001` is most North American DVDs.
+ `-oac copy`: Copy audio from DVD, keeps best audio quality.
+ `-ovc lavc`: Use lavc for video encoding, default mplayer decoder.


Options for video encoding follow `-lavopts`.


+ `vcodec=mpeg4`: Codec to use.
+ `vbitrate=2400`: Variable bit rate. `2400` is a good default value for high quality.
+ `v4mv:mbd=2:trell`: Increase quality at expense of encoding time.
+ `cmp=3:subcmp=3`: Comparison function that yields higher quality than defatuls. Can experiment (see man page for possible values).
+ `autoaspect`: Automatically adjust aspect
+ `vpass`: The pass on the video. Run the same command with `vpass=2` after first pass. A third pass may increase quality again, but minimally. Never need more than four passes. (Dimishing returns).


Filter options follow `-vf`.

+ `pullup,softskip`: Used due to North American Region DVD, may need to use other filter options for TV.
+ `crop=`: Remove black bars, determine with `cropdetect` (see above).
+ `hqdn3d=2:1:2`: More quaility.


Links
-----

+ http://www.mplayerhq.hu/DOCS/HTML/en/encoding-guide.html
+ http://www.mplayerhq.hu/DOCS/HTML/en/menc-feat-telecine.html
+ http://www.mplayerhq.hu/DOCS/HTML/en/menc-feat-enc-libavcodec.html
