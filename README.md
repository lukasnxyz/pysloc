### pysloc
An easy way to visualize a git repository's commit log.

![chart example]()

Full credit for the idea comes from [lesshero by kaihendry](https://github.com/kaihendry/lesshero),
go check it out!

#### Quick-start
```shell
python3 -m venv venv
source venv/bin/activate/
pip3 install -r requirements.txt
```
then run pysloc in a git repository or direct it to one
```shell
python3 pysloc.py .
# or
python3 pysloc.py -d "dir/of/git/repo"
```
If you want to "install" pysloc to your system, ...
