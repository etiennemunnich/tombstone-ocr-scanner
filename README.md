# tombstone-ocr-scanner
Tombstone scanner - the idea is to help my dad find family names from photos of tombstones as part of a geneology/family tree project.

Present features:
 - Use AWS Rekognition to process/OCR files and dump output to JSON files locally on your PC/instance/server
 
Planned features:
 - allow for upload to S3 / present files from local PC to AWS Rekognition
 - dump resultant JSON output to S3 folder
 - check if JSON output already exist for files processed
 
Additionally I'd like to have a post OCR processing web app that allows a user to view the image, detected text output and then allow the user to relate fields and create a corrected file (to allow for the correction of misspelled detected words).

I'm sure there are loads of other ideas and processes we could use - open to ideas and contributions!
