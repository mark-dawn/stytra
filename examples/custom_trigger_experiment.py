# Here we see how to implement a simple new type of trigger that check when the
# number of files in a directory changes for triggering a simple protocol
# showing a Flash.

from pathlib import Path

from stytra import Stytra, Protocol
from stytra.stimulation.stimuli.visual import Pause, FullFieldVisualStimulus
from stytra.triggering import Trigger


# The simplest way to implement a new trigger is inheriting from the Trigger
# class and reimplement the check_trigger method with the desired condition. In
# our case, we'll ask to check for the number of files in a folder. The
# experiment will start only when a file is added or removed.


class NewFileTrigger(Trigger):

    def __init__(self, pathname):
        self.path = Path(pathname)
        self.files_n = len(list(self.path.glob("*")))
        super().__init__()

    def check_trigger(self):
        # When number of files changes, check_trigger will return True:
        n = len(list(self.path.glob("*")))
        if n != self.files_n:
            self.files_n = n
            return True
        else:
            return False


class FlashProtocol(Protocol):
    name = "flash protocol"

    def __init__(self):
        super().__init__()
        self.add_params(period_sec=5., flash_duration=2.)

    def get_stim_sequence(self):
        stimuli = [
            Pause(duration=self.params["period_sec"] - self.params["flash_duration"]),
            FullFieldVisualStimulus(
                duration=self.params["flash_duration"], color=(255, 255, 255)
            ),
        ]
        return stimuli


if __name__ == "__main__":
    # Select a directory:
    path = "."

    # Instantiate the trigger:
    trigger = NewFileTrigger(path)

    # Call stytra assigning the triggering. Note that stytra will wait for
    # the trigger only if the "wait for trigger" checkbox is ticked!
    st = Stytra(protocols=[FlashProtocol], trigger=trigger)
