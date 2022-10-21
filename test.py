from pathvalidate import sanitize_filename

fname = "fi:l*e /p\"a?t>h|"
sanitize_filename(fname)
print(f"{fname}\n")