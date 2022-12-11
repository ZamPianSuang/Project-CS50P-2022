
# Myanmar Unicode Justification Smoother for Word
### Video Demo: <www.youtube.com>
**Description:**
### This project is Myanmar Unicode Justification Smoother for Microsoft Word
#### It has originally 4 files (but I added a few example files for demonstration purpose),
- project.py - which is main project file
- README.md - this file
- requirements.txt - includes pip-installable libraries that my project requires
- test_project.py - test codes for my project
#### The main problem to solve in this project is when we write Myanmar (Burmese) language in Microsoft Word, Word assumes words between 2 spaces as a single word (which is usually very long). So we cannot get a perfect justify (Ctrl+J) as English language. This project solves that problem by prompting to select Microsoft Word files in that project directy to modify. Once selected a Word file, it will automatically add Zero-Width-Space (U+200B) between around 90% of every Burmese word of the whole document without touching it's styles. The Zero-Width-Space (U+200B) is a hidden character in Unicode that works exactly like normal space but it has no width. By adding Zero-Width-Space, almost every word of Burmese langugage is treated exactly like English words in English language. We cannot get 100% of the words modified due to some conflicts but it is enough to get a good justify in Microsoft Word. Finally, the project generate a modified Word file which can be justified (Ctrl+J) perfectly as English languages.
**Note**
#### This project is unable to extract images yet.