# MonitorDisabler
MonitorDisabler utilites for disable all monitors except primary. Secondary start return all monitors in usual mode.

  - Disable all monitors except primary
  - Enable all monitors


### Tech

MonitorDisabler uses a number of open source projects to work properly:

* [Python 3+]

And of course MonitorDisabler it self is open source with a [public repository][dill]
 on GitHub.

### Installation

MonitorDisabler python 3+ to run.

Build new version of MonitorDisabler.

```bash
$ pip install pyinstaller
$ pyinstaller --onefile <monitorDisablerDirectory>/monitor_disabler.py
```
or run file builder from project home directory

```bash
./builder
```

After that monitor_disabler appear in <monitorDisablerDirectory>/dist/

###Prepeare for using:
Take file `monitor_disabler` from main directory or `<monitorDisablerDirectory>/dist/`  and copy to `/bin` directory
```bash
cp monitor_disabler /bin/
``` 
After that set executing privileges
```bash
chmod 777 /bin/monitor_disabler
```



   [dill]: <https://github.com/Amilitar/monitorDisabler>
