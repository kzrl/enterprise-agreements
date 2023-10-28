#!/bin/bash
for pdf in pdf/*.pdf;
do pdftotext "$pdf";
done;

mv pdf/*.txt txt/
