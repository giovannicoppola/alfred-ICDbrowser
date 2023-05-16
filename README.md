# alfred-ICDbrowser
A browser for ICD-10 codes


<a href="https://github.com/giovannicoppola/alfred-ICDbrowser/releases/latest/">
<img alt="Downloads"
src="https://img.shields.io/github/downloads/giovannicoppola/alfred-ICDbrowser/total?color=purple&label=Downloads"><br/>
</a>

![](images/alfred-ICDbrowser.gif)

<!-- MarkdownTOC autolink="true" bracket="round" depth="3" autoanchor="true" -->

- [Motivation](#motivation)
- [Setting up](#setting-up)
- [Basic Usage](#usage)
- [Known Issues](#known-issues)
- [Acknowledgments](#acknowledgments)
- [Changelog](#changelog)
- [Feedback](#feedback)

<!-- /MarkdownTOC -->


<h1 id="motivation">Motivation ✅</h1>

- To search or browse ICD10 codes
- to review and learn about the ICD-code hierarchy



<h1 id="setting-up">Setting up ⚙️</h1>

### Needed
- Alfred 5 with Powerpack license


<h1 id="usage">Basic Usage 📖</h1>

## Browsing 📇
- launch with keyword (default: `icd-b`) or custom hotkey. 
- a search term (optional, multiple strings supported) will filter the entries at the current level. 
- Browse across categories: 
	- `Enter`: forward
	- `Cmd-Enter`: back
- `Shift-enter` will show the corresponding entry in large font and copy it to the clipboard
- `Ctrl-enter` will show the corresponding entry within the ICD hierarchy (current item will be marked with ✴️)
	

## Searching 🔍
- adding `--a` to the search string (multiple strings supported) will search across the entire ICD-10 database.
- `Ctrl-enter` will show the corresponding entry within the ICD hierarchy (current item will be marked with ✴️)
- `Shift-enter` will show the corresponding entry in large font and copy it to the clipboard

## Showing entry within the ICD hierarchy 🌲
- `Ctrl-enter` will show the corresponding entry within the ICD hierarchy (current item will be marked with ✴️)
- `Shift-enter` will show the hierarchy in large font and copy it to the clipboard

## rebuilding database (optional) 🛠️
- `alfred-ICDbrowser` comes with the database derived from the ICD XML tabular file released on April 1 2023 and available on the CDC website [here](https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Publications/ICD10CM/April-1-2023-Update/)
- the script `icd-fun.py` can be used to rebuild/update the database. run with `python3 icd-fun.py "path-to-XML-file.xml"`

<h1 id="known-issues">Limitations & known issues ⚠️</h1>

- None for now, but I have not done extensive testing, let me know if you see anything!



<h1 id="acknowledgments">Acknowledgments 😀</h1>

- Icons from [Flaticon](https://www.flaticon.com/): 
	- number 1: https://www.flaticon.com/free-icon/number-1_9770783?term=1&page=1&position=35&origin=search&related_id=9770783
	- number 2: https://www.flaticon.com/free-icon/two_10125947?term=2&page=1&position=33&origin=search&related_id=10125947
	- number 3: https://www.flaticon.com/free-icon/number-3_9494620?term=3&page=1&position=17&origin=search&related_id=9494620
	- number 4: https://www.flaticon.com/free-icon/number-4_10358556?term=4&page=1&position=7&origin=search&related_id=10358556
	- number 5: https://www.flaticon.com/free-icon/number-5_8068238?term=5&page=1&position=6&origin=search&related_id=8068238
	
	
<h1 id="changelog">Changelog 🧰</h1>

- 05-11-2023: version 0.1


<h1 id="feedback">Feedback 🧐</h1>

Feedback welcome! If you notice a bug, or have ideas for new features, please feel free to get in touch either here, or on the [Alfred](https://www.alfredforum.com) forum. 

