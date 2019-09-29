# WikiParse
A program that makes parsing and gather info from some wiki pages.
In addition it will find the shortest path between two articles through references in each page. To do this we should have folder with wiki pages. 

My folder you can find here: https://drive.google.com/open?id=1qweLupOhLxDuLWSe3oXa2yAvDZPFPz6T

Our program will take the path to folder on your pc and two names of article (they should be in wiki folder) . It will find the shortest way between this pages through references in each page.

In each page it will calcualte: 
  - qauntity of images with width greater or equal 200;
  - quantity of header that the first letter is capital "E","T" or "C";
  - max length of references that don't have any tags between them;
  - quantity of lists that not insterted in other lists;
  
The result will return dictionary where the key is name of article and value is list with calculation
