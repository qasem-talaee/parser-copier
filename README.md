# Parser & Copier
A python parser and copier software that you can config it from `yaml` files, so you don't need change the code.

You can have any configuration file as much as you want.

## Parser
As you specify in the Configuration file, software reads log files and send its data.The software ensures that the duplicate data is not sent or that the data is not lost.

## Copier
As you specify in the Configuration file, the software copies the latest source files to the destination. The software ensures that there are always the latest source files in the destination and that if the file is edited at the origin, it will be changed to the destination.

## Installation
- In windows

```
pip install virtualenv
```

- In linux

```
sudo apt install python3-pip python3-venv unixodbc unixodbc-dev python3-tk
```

Then

- In Windows

```
python -m venv ./venv
```

```
venv\Script\activate
```

- In Linux

```
python3 -m venv ./venv
```

```
source ./venv/bin/activate
```

And install prerequisites

```
pip install -r req.txt
```

Finally run it

```
python3 main.py
```
## How To Compile it
After you have completed the installation instructions, Enter this command
```
auto-py-to-exe
```

And then specify main.py file to `Script Location` and add `lib` filder in `Additional Files`, Finally convert this.

If your machine is windows, `auto-py-to-exe` compile project to `exe` file,otherwise, if your machine is linux, `auto-py-to-exe` compile it for linux.

## How to create a config file for Parser ?
Create a `yaml` file with a name you want, then config these variables in it.finally copy this file to `config-log` directory.
<table>
    <thead>
        <tr>
            <th>Variable</th>
            <th>Description</th>
            <th>Options</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Separator</td>
            <td>separator of data in each rows in text files</td>
            <td><code>t</code> or <code>n</code> or somthing else</td>
        </tr>
        <tr>
            <td>Type</td>
            <td>type of file</td>
            <td><code>txt</code> or <code>csv</code> or <code>mdb</code></td>
        </tr>
        <tr>
            <td>File</td>
            <td>the file must read and parse its data</td>
            <td></td>
        </tr>
        <tr>
            <td>Send-Type</td>
            <td>How to send data?</td>
            <td><code>api</code> or <code>sql</code> (sql for sql server)</td>
        </tr>
        <tr>
            <td>SQL-SERVER</td>
            <td>If your <code>Send-Type</code> is sql, adjust it</td>
            <td></td>
        </tr>
        <tr>
            <td>SQL-DATABASE</td>
            <td>If your <code>Send-Type</code> is sql, adjust it</td>
            <td></td>
        </tr>
        <tr>
            <td>SQL-Table</td>
            <td>If your <code>Send-Type</code> is sql, adjust it</td>
            <td></td>
        </tr>
        <tr>
            <td>SQL-USERNAME</td>
            <td>If your <code>Send-Type</code> is sql, adjust it</td>
            <td></td>
        </tr>
        <tr>
            <td>SQL-PWD</td>
            <td>If your <code>Send-Type</code> is sql, adjust it</td>
            <td></td>
        </tr>
        <tr>
            <td>Table-Name-MDB</td>
            <td>If your <code>Type</code> is mdb, set mdb table name to it</td>
            <td></td>
        </tr>
        <tr>
            <td>Send-API</td>
            <td>If your <code>Send-Type</code> is api, set api address to it</td>
            <td></td>
        </tr>
        <tr>
            <td>Data</td>
            <td>number of column you need to read.start of 0</td>
            <td></td>
        </tr>
        <tr>
            <td>Names</td>
            <td>the data send with these names in api or column name of sql table</td>
            <td></td>
        </tr>
        <tr>
            <td>Check</td>
            <td>the number of columns with which the software checks that they do not send duplicate information</td>
            <td></td>
        </tr>
        <tr>
            <td>Date-Format</td>
            <td>what is the format of the check data?</td>
            <td></td>
        </tr>
        <tr>
            <td>Ignore-Row</td>
            <td>which rows should be ignored? (start from 0)</td>
            <td></td>
        </tr>
    </tbody>
  </table>

See an example of parser config file :

```yaml
Separator : t
Type : txt
File : G:\Qasem Talaee\project\parser\test\text.txt
Send-Type : sql
SQL-SERVER : server
SQL-DATABASE : databse
SQL-Table : data
Table-Name-MDB : data
Send-API : 172.0/logsheet.php
Data :
  - 2
  - 3
  - 4
  - 5
Names :
  - pi
  - fi
  - mi
  - si
Check :
  - 0
  - 1
Date-Format : '%Y-%m-%d %H:%M:%S'
Ignore-Row :
  - 0
```

See an example of the file to be read :

```text
Date	Time	pi	fi	mi	si
1401-04-01	22:15:02	1	2	3	4
1401-04-02	23:12:22	2	3	4	5
1401-04-03	17:35:17	6	7	8	9
```

## How to create a config file for Copier ?
Create a `yaml` file with a name you want, then config these variables in it.finally copy this file to `config-copy` directory.

with `-` you can create a list of configs in `Order`.
<table>
    <thead>
        <tr>
            <th>Variable</th>
            <th>Description</th>
            <th>Options</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Order</td>
            <td>It's header and must be exist</td>
            <td></td>
        </tr>
        <tr>
            <td>From</td>
            <td>The address of the source directory</td>
            <td></td>
        </tr>
        <tr>
            <td>To</td>
            <td>The address of the destination directory</td>
            <td></td>
        </tr>
        <tr>
            <td>Type</td>
            <td>The system determines the required files based on the file name. What do you want to be in the file name?</td>
            <td></td>
        </tr>
        <tr>
            <td>Count</td>
            <td>The number of files to be stored in the destination for each <code>Type</code></td>
            <td></td>
        </tr>
    </tbody>
  </table>

See an example of copier config file :

```yaml
Order :
  - 
    From : c:\source
    To : e:\destination
    Type :
      - game
      - log
    Count : 10
```