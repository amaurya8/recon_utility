**High Volume Data Recon Utility** 

This project is useful for comparing / reconciling high volume structured data sets between 2 systems could be files or databases
and any cross combination of files and databases. 

**Description**

This project is useful for comparing / reconciling high volume structured data sets between 2 systems could be files or databases
and any cross combination of files and databases. This is driven through a configuration which takes
user input( flags ), source / target details and compare types ( key basis and index ) along with other 
flag based recon features. Post reconciliation it generates quick review, eye-catching diffs 
between source and target systems, pls see one quick glimpse of diff reports.

![img.png](img.png)
![img_1.png](img_1.png)

Features:

1. File to File comparison ( csv, xlsx, text, json, xml, fix-width etc)
2. Database to Database ( Oracle, MSSQL, MySQL, ADX, DB2, Cosmos DB etc. )
3. File to Database, Database to File cross combination 
4. Key based compared ( Primary key and Composite primary key) 
5. Index based - row by row compare 
6. Flag based tolerance for numeric fields 
7. Flag based space tolerance for text / string fields
8. Detailed diff reports ( html, xlsx )
9. Parallel diff visualization for unmatched attributes / fields 
10. Row and Column level detailed diff statistics 
11. etc ... 


**Dependencies**

Platform: Windows 10 / Unix/ Linux
Python: 3.10 or above
IDE: Pycharm and equivalent IDE
Required Modules: Refer requirements.txt

**Installing**

Clone the below repo
Install required python modules and build the project
Run the demo scenario to make sure setup is complete 

**Executing program**

Configure Driver_Config.xlsx/csv per source and target details by following reference scenario
Run Recon Engine module through pycharm or command line ( python -m recon_engine.py)

**Authors**
Ibcore QA team

**Version History**
0.2
Various bug fixes and optimizations
See commit change or See release history
0.1

Acknowledgments
Inspiration, code snippets, etc. ( NA )

