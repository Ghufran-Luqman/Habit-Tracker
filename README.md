A website application built with FastAPI and SQLite designed to help you stay consistent with your day-to-day habits.
![image](https://github.com/user-attachments/assets/e7b4668f-0988-4d7a-a98d-81233b56f005)
It has features such as undoing your 10 recently deleted habits (not from pressing the reset button but from pressing the remove button). The recently deleted habits are stored in a list.
This undo button only appears if there are any recently deleted habits. Here, the habit 'Code' was removed.

![image](https://github.com/user-attachments/assets/97b483c5-a0dc-443b-9120-f562f04a60d8)

If the user enters 'Code' again, this is removed from the list and simply placed back.

To run, make sure your environment is set-up with everything in fastAPI (`pip install fastapi[all]`) and SQLite, then run `uvicorn main:app --reload`.
