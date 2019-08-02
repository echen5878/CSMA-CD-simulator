You can run on the terminal
	
	python CSMA-CD_simulator.py 2 2

The first argument specifies the number of sources. The second specifies how many packets each source has to send out.

It immediately prints out the progress and state, in which nothing has occurred.

It calculates the possibilities and then waits for the user to choose one of the possibilities.

It executes the choice and updates progress and model, waiting for user to choose one of the possibilities from the newly calculated possibilities.

When a source is done, it will indicate it on the current state and will not be included in the calculations.

This continues in a loop until all packets have been sent.

The final print will show the progress along with the final state with all sources indicating Done when all its packets have been sent.