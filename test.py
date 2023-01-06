
with open("C:\\ft_userdata\\docker-compose.yml", "r") as f:
    # Read the contents of the file into a list
    lines = f.readlines()

# Replace the 28th element in the list with "29 row"
lines[27] = '      --strategy NewStrategy\n'

# Write the modified list to the file
with open("C:\\ft_userdata\\docker-compose.yml", "w") as f:
    f.writelines(lines)
