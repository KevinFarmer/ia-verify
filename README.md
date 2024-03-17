# verify_uploads.py

To verify your Internet Archive items uploaded by TubeUp

Enter your IA account email in the single quotes on line 1

Optionally, decide whether you want to check thumbnails, and toggle line 2 True/False appropriately

### Note
Any .webp thumbnails take time for IA to process into a format that they will display, and will get falsely flagged as missing while still processing


## Output

### upload_issues.txt
A text file containing any IA items missing data
Includes the identifier, the file formats currently in the item, and whether video/thumbnail/info.json is missing

### problem_ids.txt
A text file of the youtube URLs for the incomplete items, which can be re-run using tubeup -i


# verify_id_list.py

Takes in an input file of youtube IDs or URLs, and determines which either haven't been uploaded, or have but are missing data


## Output

### {input_file_name}_missing_ids_from_list.txt
A text file containing any IA items missing data
Includes the identifier, the file formats currently in the item, and whether video/thumbnail/info.json is missing

### {input_file_name}_problem_ids_from_list.txt
A text file of the youtube URLs for the incomplete items, which can be re-run using tubeup -i

> :warning: These items can only be fixed by the person who uploaded them originally
