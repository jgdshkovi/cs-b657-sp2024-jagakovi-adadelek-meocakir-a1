# Project Report

## Introduction
In this report, we present a comprehensive documentation of our approaches and outcomes for Assignment 1. The report is 
structured into 3 primary sections. Initially, we delve into image preprocessing, where we outline the procedures 
employed to prepare images for answer detection. Subsequently, we explore the answer detection phase where we explain 
the methodologies we used to identify answers within the preprocessed images. Finally, we discuss the process of answer 
injection/extraction.

Our approach is both efficient and robust. It processes individual forms in under 3 seconds, maintaining high accuracy 
with only two errors identified across the entire test dataset. This underscores the effectiveness and reliability of 
our approach in handling tasks with precision and speed.

## Preprocess
This animation showcases the key stages of our preprocessing algorithm. In this section, we will provide a frame by 
frame explanation of each major step of our approach. The step number is specified in the top left of the animation.
We use different colors for different steps of preprocessing for easy visualization.

![a-48](Animation/a-48.gif)

### Step 0-1
These steps include removing the header of the form and converting every pixel to either pure white or pure black. We 
achieve this by setting a threshold value, which allows us to categorize each pixel as either pure white or black based 
on its brightness.

### Step 2-4
These steps include to the column elimination phase, where we remove columns primarily composed of white pixels by 
coloring them blue. We have a tolerance of a few black pixels for every column so noise pixels can still be removed. 
At steps 3 and 4 we do additional passes where we remove very small lingering columns that most likely does not contain
any meaningful information (Notice small white column gaps in the image).

### Step 5
This step includes finding the columns that actually contain the answers. We do this by finding the top 4 widest removed
column from the previous steps. Our assumption is that the widest gaps in the form correspond to the spaces between each 
column of questions. We color these columns green to differentiate  from the rest of the removed columns. After this 
step every column that is not green most likely contain answers of the student.

### Step 6-11
At this stage we are left with 3 main columns that contain the student's answers. In these steps we attempt to detect
the question rows by replacing the whitespace rows by red. Similar to column detection, we have a few pixel tolerance so
if the marked square is slightly overflowing the borders of the box, we can still separate them. We process every 
question column separately so the rows can be seperated more precisely for every column. Similar to the column processing 
we do multiple passes for every row to remove any small spaces that most likely does not contain any meaningful 
information (Notice the small white rows close to the header).

### Step 12
We pass the preprocessed image to the grader.

## Question Detection

## Answer Inject/Extraction

## Conclusion

## Member Contributions
