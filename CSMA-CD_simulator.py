from itertools import combinations
import sys

class Source:
    num_collisions = 0
    source_id = ''
    curr_frame = 0
    frames_left = 0
    progress = ""
    possibilities = []
    sent = False
    def __init__(self, id, frames):
        self.source_id = id
        self.frames_left = frames

def simulate(num_sources, total_frames):
    sources = []
    id = 'a'
    total = num_sources * total_frames
    sent = 0
    slot = "slot\t| "
    current_slot = 0
    for i in range(num_sources):
        sources.append(Source(id, total_frames))
        id = chr(ord(id) + 1)

    #check how many total packets are sent
    while sent < total:
        print("Progress so far:")       # prints the current progress for each source
        for source in sources:
            print(source.source_id + "\t", source.progress, sep='|')
            if len(source.possibilities) == 0:
                source.possibilities = [i+current_slot for i in range(2**source.num_collisions)]
            source.possibilities = [num for num in source.possibilities if num >= current_slot]
        print(slot)
        print("---------------------------------------------")
        print("Current state:")         # prints the current state for each source
        print("Source | Current frame | Num Collisions | Possible slots")
        for source in sources:
            if source.frames_left == 0:
                print(source.source_id, "Done", sep="\t|\t")
            else:
                print(source.source_id, source.source_id + str(source.curr_frame), source.num_collisions, ",".join(str(x) for x in source.possibilities), sep="\t|\t")

        print("---------------------------------------------")

        frame = []
        must_send = ''      #determines whether a source must send a packet and adds that to the combination of all other sources
        for source in sources:
            if source.frames_left == 0:
                continue
            elif current_slot in source.possibilities and len(source.possibilities) > 1:
                frame.append(source.source_id + str(source.curr_frame))
            elif current_slot in source.possibilities:
                must_send += source.source_id + str(source.curr_frame) + ","

        must_send = must_send.rstrip(',')

        c = [comb for i in range(len(frame)) for comb in combinations(frame, i + 1)]    #calculates the possibilities for slot
        new = [','.join(w) for w in c]
        possibilities = [(s + "," + must_send).rstrip(',') for s in new]
        if must_send != '':
            possibilities.append(must_send)
        print("possibilities for slot " + str(current_slot))
        for i,s in enumerate(possibilities):
            print(str(i) + ") " + s)

        user = input('enter a number for the choice you make --> ')     #gets user input. checks again if not valid number
        while not user.isnumeric() or int(user.strip("\n")) >= len(possibilities) or int(user.strip("\n")) < 0:
            user = input('enter a valid number listed in the possibilities --> ')
        choices = possibilities[int(user.strip("\n"))].split(",")

        # extracts user choice and respectively updates state and progress
        if len(choices) == 1:
            choice = choices[0]
            id = choice[0]
            num = int(choice[1])
            id = ord(id) - 97
            source = sources[id]
            source.num_collisions = 0
            source.curr_frame += 1
            source.frames_left -= 1
            source.progress += choice + "\t"
            source.possibilities.clear()
            source.sent = True
            sent += 1
        else:
            for choice in choices:
                id = choice[0]
                num = int(choice[1])
                id = ord(id) - 97
                source = sources[id]
                source.num_collisions += 1
                source.possibilities = [i + current_slot + 1 for i in range(2 ** source.num_collisions)]
                source.progress += choice + "\t"
                source.sent = True

        for source in sources:
            if source.sent:
                source.sent = False
            else:
                source.progress += "  \t"

        slot += str(current_slot) + " \t"
        current_slot += 1


    print("Progress so far:")       #prints out progress and state once more after all packets have sent
    for source in sources:
        print(source.source_id + "\t", source.progress, sep=' | ')
        if len(source.possibilities) == 0:
            source.possibilities = [i + current_slot for i in range(2 ** source.num_collisions)]
    print(slot)
    print("---------------------------------------------")
    print("Current state:")
    print("Source | Current frame | Num Collisions | Possible slots")
    for source in sources:
        if source.frames_left == 0:
            print(source.source_id, "Done", sep="\t|\t")
        else:
            print(source.source_id, source.source_id + str(source.curr_frame), source.num_collisions,
                  ",".join(str(x) for x in source.possibilities), sep="\t|\t")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Not enough arguments given. Try again!")
        exit(0)
    num_sources = int(sys.argv[1])
    num_frames = int(sys.argv[2])
    simulate(num_sources, num_frames)
