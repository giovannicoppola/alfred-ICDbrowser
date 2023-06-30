# alfred-ICD 🔟 browser
An [Alfred](https://www.alfredapp.com/) browser for ICD-10 codes


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

- To search or browse ICD-10 codes without opening a browser/website
- to review and learn about the ICD-code hierarchy



<h1 id="setting-up">Setting up ⚙️</h1>

### Needed
- [Alfred 5](https://www.alfredapp.com/) with Powerpack license
- `pandas` library (can be installed with `pip3 install pandas`


<h1 id="usage">Basic Usage 📖</h1>

## Browsing 📇
- launch with keyword (default: `icd-b`) or custom hotkey. 
- a search term (optional, multiple strings supported) will filter the entries at the current level. 
- Browse across categories: 
	- `Enter`: forward
	- `Cmd-Enter`: back
- `Shift-enter` will show the corresponding entry in large font and copy it to the clipboard
- `option-enter` will show the complete current list in large font and copy it to the clipboard
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
- the script `icd-fun.py` can be used to rebuild/update the database. Run with `python3 icd-fun.py "path-to-XML-file.xml"`

<h1 id="known-issues">Limitations & known issues ⚠️</h1>

- None for now, but I have not done extensive testing, let me know if you see anything!



<h1 id="acknowledgments">Acknowledgments 😀</h1>

- Icons from [Flaticon](https://www.flaticon.com/)
	
	
<h1 id="changelog">Changelog 🧰</h1>

- 2023-06-14: version 0.2 (added option to copy entire output
- 2023-05-11: version 0.1


<h1 id="feedback">Feedback 🧐</h1>

Feedback welcome! If you notice a bug, or have ideas for new features, please feel free to get in touch either here, or on the [Alfred](https://www.alfredforum.com) forum. 

