# Doomsday Algorithm

The Doomsday Algorithm is a method to deteriminate the day of the week for any given date. It's designed in a way that makes it easy to calculate in your head. This project created a python programm to train this algorithm. The program creates a random date, shows you the result, stops the time for each calcultion, and documents the results for later analysis.

## How does the algorithm work?

In the gregorian calender some dates have alwys the same date of the week in a year (dates in day.month.):

- 3.1./4.1. (regular/leap year)
- 28.2./29.2. (regular/leap year; often refered as 'last of February' or '0.3.')
- 7.3.
- 4.4.
- 9.5.
- 6.6.
- 11.7.
- 8.8.
- 5.9.
- 10.10.
- 7.11.
- 12.12.

> "As mentioned above, the last day of February defines the doomsday. For January, January 3 is a doomsday during common years and January 4 a doomsday during leap years, which can be remembered as "the 3rd during 3 years in 4, and the 4th in the 4th year". For March, one can remember the pseudo-date "March 0", which refers to the day before March 1, i.e. the last day of February.
> For the months April through December, the even numbered months are covered by the double dates 4/4, 6/6, 8/8, 10/10, and 12/12, all of which fall on the doomsday. The odd numbered months can be remembered with the mnemonic "I work from 9 to 5 at the 7-11", i.e., 9/5, 7/11, and also 5/9 and 11/7, are all doomsdays (this is true for both the Day/Month and Month/Day conventions)." Wikipedia

___
**Example:** Weekday of 20th August 2017  
Doomsday of 2017 was Tuesday.  
Doomsday of August is the 8th -> 8/8 is a Tuesday  
20-8 = 12  
12 mod 7 = 5 -> five days shift  
20th August 2017 was a Sunday.  
___

If the day for any of the doomsdays is known, all other doomsday for this year are known as well and can be used to calulate the day for any other date of the year. 
To calculate the doomsday for a year, an anchor day for the century can be used. 

|Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|
|-|-|-|-|-|-|-|
|2100||2000|1900||1800||

The anchor days are repeated in a 400 year cycle (as the entire gregorian calender).

Now you can calculate the difference between the year and century anchor year in years. Multiply by five, divide by fourh, and round down. Divide by seven and the remainer is the shift of days.

___
**Example:** doomsday of 1925:  
Century: 1900  
1925 - 1900 = 25  
25*5/4 = 125/4 = 31.25 -> down rounded 31  
31 mod 7 = 3  
Doomsday of 1900 was Wednesday. Three days shift makes the Doomsday of 1925 an Saturday.
___

An additional important fact is, that years which are divisible by 100, but not by 400 are not leap years, even though they are divisible by 4. E.g. 2100 won't be a leap year, but 2400 will.

### Additional Examples

___
#### 24.01.2224

Doomsday of 2200: Friday  
2224 - 2200 = 24  
24*5/4 = 120/4 = 30  
30 mod 7 = 2 -> two days shift  

--> Doomsday of 2224 is Sunday.  

2224 is a leap year, hence the 4th January is a Doomsday.  
24 - 4 = 20  
20 mod 7 = 6 -> six days shift  

--> The 24th January 2224 is a Saturday.  

___
#### 21.12.1726

Doomsday of 1700: Monday  
1726 - 1700 = 26  
26*5/4 = 130/4 = 32.5 -> down rounded 32  
32 mod 7 = 3 -> three days shift.  

--> Doomsday of 1726 was Thursday.  

12.12. is a Doomsday.  
21 - 12 = 9  
9 mod 7 = 2 -> two days shift  

-> The 12th December 1726 was a Saturday.  
___

## What the programm does

The rogramm provides a GUI for easy training. It creates a random date, and indicates, if the selection was correct with a simple green-red color code.
It also creates a file (if not existing) where it stores the session number, number of guess, the correct answer, the guess, and the time (duration).

![GUI](GUI.png)