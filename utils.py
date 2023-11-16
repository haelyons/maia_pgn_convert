from os import listdir, path
import re
import math

def get_files_in_directory(dir, ext):
    all_files = listdir(dir)
    matches = [];
    for filename in all_files:
        root, end = path.splitext(filename)
        if end == ext:
            matches.append(filename)
    return matches

def convert_lichess_to_chessbase(file_path):
    with open(file_path, encoding="utf8") as f:
        file = f.read()
    # Replace emt with clk
    file = file.replace("%clk", "%emt")
    # Remove UTC date/time fields
    file = re.sub("\[UTC.*\\n?", "", file)
    return file

def convert_chessbase_to_lichess(file_path):
    with open(file_path, encoding="utf8") as f:
        file = f.read()
    # Change all "%emt" to "%clk"
    file = file.replace("%emt", "%clk")
    # Split by double line break
    file_parts = file.split("\n\n")
    # Every other line is the move data. Strip line breaks from those.
    i = 1
    while i < len(file_parts):
        try:
            # Get initial clock time
            clock_time = re.search("%clk (.*?)]", file_parts[i])
            time_control = clock_to_seconds(clock_time.group(1))
            # Insert time control
            file_parts[i-1] = f'{file_parts[i-1]}\n[TimeControl "{time_control}"]'
        except:
            # No clock, not a big deal
            pass
            
        # Remove line breaks
        file_parts[i] = file_parts[i].replace("\n", "")
        # Make sure clock isn't messed up
        file_parts[i] = re.sub("( :|: )", "", file_parts[i])
        i += 2

    return "\n\n".join(file_parts)

def convert_chesscom_to_lichess(file_path):
    with open(file_path, encoding="utf8") as f:
        file = f.read()

    # Global field deletions: Date, Round, CurrentPosition, Timezone, StartTime, EndTime, EndDate, Link
    file = re.sub("\[Date.*\\n?", "", file)
    file = re.sub("\[Round.*\\n?", "", file)
    file = re.sub("\[CurrentPosition.*\\n?", "", file)
    file = re.sub("\[Timezone.*\\n?", "", file)
    file = re.sub("\[StartTime.*\\n?", "", file)
    file = re.sub("\[EndTime.*\\n?", "", file)
    file = re.sub("\[EndDate.*\\n?", "", file)
    file = re.sub("\[Link.*\\n?", "", file) 

    # Chess.com uses double line-breaks, Lichess DB has single
    file_parts = file.split("\n\n")
    print("Converting: ", len(file_parts), " chess games...")

    # Replace ECOUrl with "Opening" field extracted from ECOUrl
    i = 0
    max_games = len(file_parts)
    max_games = 1000
    while i < 1000:
        try:
            eco_pattern = r'\[ECOUrl "(.*?)"'
            opening = re.search(eco_pattern, file_parts[i])
            url = opening.group(1)
            split = url.split("/")[-2:]
            split = re.sub("-", " ", split[1])
            print("Game:", i, " Opening:", split)
            opening_string = "[Opening " + "\"" + split + "\"" + "]\n" 
            file_parts[i] = re.sub("\[ECOUrl.*\\n?", opening_string, file_parts[i]) 
            file_parts[i] = re.sub("\[Event.*\\n?", "[Event \"Rated Classical Game\"]\n", file_parts[i])
            # Remove extra whitespaces between move numbers, replace double tabs between lines with a newline
            file_parts[i] = re.sub("  ", " ", file_parts[i])
            file_parts[i] = re.sub("        ", "\n", file_parts[i])
        except:
            # Doesn't have an opening (in case of immediate draw), okay to pass
            pass

        # Replace double linebreaks with single linebreaks
        file_parts[i] = file_parts[i].replace("\n\n", "\n")
        i += 1

    # Concatenate file parts
    return "\n".join(file_parts)

def clock_to_seconds(clock_time):
    hours, minutes, seconds = clock_time.split(":")
    total_seconds = int(hours) * 60 * 60 + int(minutes) * 60 + int(seconds)
    # Do some rounding (10 minutes)
    rounded_seconds = math.ceil(total_seconds / 600) * 600
    return f"{rounded_seconds}+0"