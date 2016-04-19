1. install mongodb
2. create a directory with non-root/sudo access e.g. 
  mkdir ~/mongodb/
3. start the mongodb daemon: 
  mongod --dbpath ~/mongodb/
4. Change the line (should be around 26) from this:
```python
client = MongoClient('mongodb://' + dbuser + ':' + dbpass + '@ds023458.mlab.com:23458/heroku_6f2n4wp9')
```
  to this:
```python
client = MongoClient('127.0.0.1:27017')
```
5. Start the server and hope for the best!
