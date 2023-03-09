import os

script_dir = os.path.dirname(__file__)
subs = "subjects"
path = os.path.join(script_dir, subs)

file_names = os.listdir(path)
for file in file_names:
    subject = "/".join([subs, file])
    with open(subject, 'r') as csv:
        csv_text = csv.read()
    new_text = csv_text.replace("@@@", "~~~")
    with open(subject, 'w') as new:
        new.write(new_text)