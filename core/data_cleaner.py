class DataCleaner:

    def __init__(self, default_cleaners=None):
        self.default_data_cleaners = default_cleaners
        self.data_cleaner = None
        self.set_default_cleaners(default_cleaners)

    def get(self, _class):
        """
        returns data_cleaner for provided class
        :param _class:
        :return:
        """
        return self.data_cleaner.get(_class)

    def update_cleaner(self, _class, fields):
        """
        changes cleaner for provided class
        :param _class: class for what to change cleaner
        :param fields: fields to be cleaned when returning JSON
        :return:
        """
        self.data_cleaner[_class] = fields

    def extend_cleaner(self, _class, fields):
        self.data_cleaner[_class].extend(fields)

    def extend_default_cleaner(self, _class, fields):
        """
        extends default cleaner for class with fields provided
        :param _class:
        :param fields:
        :return:
        """
        if self.default_data_cleaners.get(_class):
            self.data_cleaner[_class] = self.default_data_cleaners[_class].copy()
            self.data_cleaner[_class].extend(fields)
        else:
            self.data_cleaner[_class] = fields

    def clear_for_class(self, _class):
        """
        removes cleaner for provided class
        :param _class:
        :return:
        """
        if self.data_cleaner.get(_class):
            del self.data_cleaner[_class]

    def reset_for_class(self, _class):
        """
        set default cleaner for provided class
        :param _class:
        :return:
        """
        if self.default_data_cleaners.get(_class):
            self.data_cleaner[_class] = self.default_data_cleaners[_class].copy()

    def set_default_cleaners(self, default_cleaners=None):
        """
        set default cleaners for all class provided in `default_cleaners`
        :param default_cleaners:
        :return:
        """
        self.default_data_cleaners = default_cleaners or dict()
        self.reset()

    def reset(self):
        """
        resets cleaners to default
        :return:
        """
        self.data_cleaner = dict()
        for key in self.default_data_cleaners:
            self.data_cleaner[key] = self.default_data_cleaners[key].copy()
