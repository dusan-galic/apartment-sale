from sqlalchemy import TypeDecorator, String


class StringChoiceType(TypeDecorator):
    """
    :param choices:
    :param kw:
    """
    impl = String

    def __init__(self, choices, **kw):
        self.choices = dict(choices)
        super(self.__class__, self).__init__(**kw)

    def process_bind_param(self, value, dialect):
        """
        :param value:
        :param dialect:
        :return:
        """
        items = [k for k, v in self.choices.items() if v == value]
        return items.pop() if items else None

    def process_result_value(self, value, dialect):
        """
        :param value:
        :param dialect:
        :return:
        """
        return self.choices[value] if value in self.choices else None

    @property
    def python_type(self):
        """
        :return:
        """
        return str

    def process_literal_param(self, value, dialect):
        """
        :param value:
        :param dialect:
        :return:
        """
        return str(value) if value else None
