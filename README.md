### Notes to self...

To run ([see here](https://stackoverflow.com/questions/45854169/how-can-i-use-an-es6-import-in-node)):
```
node -r esm debug_martinez_110.js
```

To debug within VSCode
(requires using built-in terminal, taken from [here](https://medium.com/@nsisodiya/the-ultimate-vs-code-debug-setup-for-node-js-a03cdbc594ba)):
```
node -r esm --inspect-brk --inspect=0.0.0.0:9229 ./debug_martinez_110.js
```
