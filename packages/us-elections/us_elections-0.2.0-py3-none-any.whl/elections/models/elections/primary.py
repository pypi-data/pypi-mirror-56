# Imports from other dependencies.
import us


class PrimaryElection(object):
    party_prefix = None
    repr_label = "PrimaryElection"

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k == "state":
                self.__dict__[k] = us.states.lookup(v)
            elif k == "election_notes":
                self.__dict__[k] = v
            elif self.party_prefix and k.startswith(self.party_prefix):
                modified_field_name = k[len(self.party_prefix) :]

                if not modified_field_name.startswith("runoff_"):
                    self.__dict__[modified_field_name] = v

    def __repr__(self):
        return "<{}: {}>".format(self.repr_label, self.__str__())

    def __str__(self):
        return "{} {:%b. %d, %Y}".format(self.state.name, self.election_date)


class DemocraticPrimaryElection(PrimaryElection):
    party_prefix = "dem_"
    repr_label = "DemocraticPrimaryElection"


class RepublicanPrimaryElection(PrimaryElection):
    party_prefix = "gop_"
    repr_label = "RepublicanPrimaryElection"
