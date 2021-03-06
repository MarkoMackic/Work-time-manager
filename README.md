# Manage your work sessions easily and securely

## Intro:

I needed program to manage my work sessions for me, and calculate amount I earned, so I made my own. In commands section everything you can use will be describe. If you think there is a feature to add, open an issue describing the problem. Date, time and datetime formats are at beginning of program, so you can tweak them for your comfort. This program can be used by multiple users, and each user sessions are saved to file he created (it asks you at beginning of program for session file) and only he can access the file with his password. Currently this works with python 3 only.

## Commands:

* __start__

   &nbsp; &nbsp; &nbsp;Starts the session.

* __stop__
    
  &nbsp; &nbsp; &nbsp;
  Ends the session.
      
* __print_sessions__ {start_date} {end_date}

  
  &nbsp; &nbsp; &nbsp;
  Prints the sessions.
  
  &nbsp; &nbsp; &nbsp;
  start_date, end_date - Optional parameters, if both are supplied, then the date range sessions are printed, if there is only date1 then a single date sessions are printed. If none of these are supplied it will print all of your sessions.
  
* __add_session__ {start_date}-{start_time} {end_date}-{end_time} paid

   &nbsp; &nbsp; &nbsp;
   You can add a session into history by using this command. Paid is true/false string.
   
* __ttime__

    &nbsp; &nbsp; &nbsp;
   If you started the session, and you want to check the current working time, you can use this command.
   
* __remove_sessions__ {date}

    &nbsp; &nbsp; &nbsp;
    If you need to remove sessions from your working history, use this command and follow further instructions.
    
* __save__

    &nbsp; &nbsp; &nbsp;
    Saves all of your sessions to file. Make sure all sessions are finished before using this command.

* __load__

    &nbsp; &nbsp; &nbsp;
    Loads your session file from file to memory.
   
* __mark_paid__ {start_date} {end_date}

    &nbsp; &nbsp; &nbsp;
    start_date, end_date - Optional parameters, if both are supplied, then the date range sessions are marked paid, if there is only start_date then a single date sessions are marked paid. If none of these are supplied it will mark all your sessions as paid.
 
* __mark_unpaid__ {start_date} {end_date}

    &nbsp; &nbsp; &nbsp;
    start_date, end_date - Optional parameters, if both are supplied, then the date range sessions are marked unpaid, if there is only start_date then a single date sessions are marked unpaid. If none of these are supplied it will mark all your sessions as unpaid.
    
* __change_h_price__ {price}
    
    &nbsp; &nbsp; &nbsp;
    Change your hourly price. Price should be integer, but float with . is supported eg. 10.5
    
* __calc__ {start_date} {end_date}

    &nbsp; &nbsp; &nbsp;
    Calc counts only for sessions that are marked unpaid, it calculates how much hours you have unpaid, and the amount of money you earned.

    &nbsp; &nbsp; &nbsp;
    start_date, end_date - Optional parameters, if both are supplied, then the date range sessions are calculated, if there is only start_date then a single date sessions are calculated. If none of these are supplied it will calculate all your sessions.
