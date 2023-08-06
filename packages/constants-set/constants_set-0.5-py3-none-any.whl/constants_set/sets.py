class ConstantsSet(set):
    def to_choices(self):
        return tuple((name, name) for name in sorted(self))

    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError(f"{name} not present in the ConstantsSet {self}")

    def __str__(self):
        return ", ".join(sorted(self))

    def to_array(self):
        return sorted(self)
