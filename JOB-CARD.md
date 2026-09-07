# Job card

What it does:
Takes some text, finds the tasks mentioned in it, and gives each task a simple title and a completion status. It can return more than one task.

Input:
A field called "text", containing between 1 and 2000 characters.

Output:
An object with a "tasks" list. Each task has:
- "title": a short, clear string describing the task.
- "done": true if the text clearly says it was completed, otherwise false.

If there are no tasks, return an empty tasks list.

It must never:
- Invent tasks that are not mentioned in the input.
- Break a task into extra steps that the user did not mention.
- Change the meaning when simplifying the title.
- Mark a task as completed without clear evidence.
- Return extra fields or text outside the JSON response.

When unsure it should:
Set "done" to false if completion is unclear.
Leave something out if it is unclear whether it is a task.
An explicitly stated goal, like "I need to get fitter", counts as a task.
A situation by itself, like "The kitchen is a mess", does not.