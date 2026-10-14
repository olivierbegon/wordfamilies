# Word Families

Tap-and-play word family lessons (-am, -ap) for a beginning reader. Works offline on iPad once added to the Home Screen.

Live at https://olivierbegon.github.io/wordfamilies/

## Add or change a lesson
1. Edit the `FAMILIES` list in `build.py` (words, pictures, story).
2. Run `python3 build.py`. It writes `<family>.html`, the menu (`index.html`) and the offline file list in `sw.js`.
3. Commit and push.

`lesson.template.html` is the shared page layout for every family.
