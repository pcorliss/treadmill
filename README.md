# Treadmill Bluetooth Script

This script interacts via bluetooth with my TR1000 LifeSpan treadmill with retro console.

Big thanks to [@brandonarbini](https://github.com/brandonarbini) for their original work reverse engineering the initialization and command codes. [Ruby Project](https://github.com/brandonarbini/treadmill)
Also thanks to [@lostmsu](https://github.com/lostmsu) for their detective work and C# project. 
And all the helpful comments in GitHub that worked as helpful breadcrumbs along the way.
* [brandonarbini/treadmill](https://github.com/brandonarbini/treadmill) - Ruby
* [lostmsu/Xrcise](https://github.com/lostmsu/Xrcise) - C#
* https://github.com/brandonarbini/treadmill/issues/1
* [lostmsu Gist](https://gist.github.com/lostmsu/1b0d4a33e5ca2418c2b52797eb720ec7)

## Running

Tested with Python `3.12.3`.

```
pip install -r requirements.txt
python3 treadmill.py
```
