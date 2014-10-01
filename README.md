Python-Agchive
==============

Compress/Extract files or recursive folders with several formats, automatically detected in path.

Introduction
-----------------------
The Agchive.py is a Python class which compress or decompress files or recursive folders with the selected algorithm.

How it's work
-----------------------
For compression : 
```
compression = Agchive()  
compression.compress( srcFileOrFolder, dstArchive, removeSrc = False)  
```

1. srcFileOrFolder --> String absolute path of file or folder you want to compress
2. dstArchive --> String absolute path of your archive **with the extention**
3. removeSrc --> (Optional) If you want to remove the source

For decompression : 
```
extracting = Agchive()
extracting.extract(srcArchive, srcFileOrFolder, removeSrc = False)
```

1. srcFileOrFolder --> String absolute path of archive **with the extention**
2. dstArchive --> String absolute path of your folder or file decompress
3. removeSrc --> (Optional) If you want to remove the source

Example
-----------------------

To compress à folder in folder.zip archive without remove the source  

```
compression = Agchive()
compression.compress( "c:/myFolder", "c:/myArchive.zip")
```


To decompress à document.rar to documentFolder and remove the source

```
extracting = Agchive()
extracting.extract("c:/document.rar", "c:/documentFolder", True)
```

Supported format and action for now
-----------------------
Zip : Compress, Decompress  
7z  : Compress, Decompress  
rar : Decompress  
