# CouchDB Cleaning tool  
  
A simple python script to clean deleted documents, compact databases and views.  
  
## How to use  
  
start by installing the requirements:  
  
```bash
pip install -r requirements.txt
```
  
Now run the script:  
  
```bash
python purge_database.py --user=<YOUR USERNAME> --password=<YOUR PASSWORD> --host=<THE URL TO COUCHDB>
```  
  
Get help for available options:  
  
```bash  
python purge_database.py -h
```  
  

It defaults to calling the host using HTTP, if you want to use HTTPS you need to specify --protocol=HTTPS  
  
### Options  
  
`--user: The username to authenticate with the server`  
`--password: The password for the user`  
In case of admin party just skip those.  
  
`--host: The url of the datbase including port (default localhost:5984)`  
`--protocol: http or https (default http)`  
`--database: The database to clean (default all)`  
  
  
   Copyright (C) 2020 nisbus.com.
  
This file is part of CouchDB Cleaner.  
  
CouchDB Cleaner is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at
your option) any later version.  
  
CouchDB Cleaner is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.  
  
You should have received a copy of the GNU General Public License
along with CouchDB Cleaner.  If not, see <https://www.gnu.org/licenses/>.
