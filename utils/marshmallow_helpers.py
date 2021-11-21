import marshmallow
import flask_restful


class SuperSchema(marshmallow.Schema):

    def check_and_abort(self, data, unknown=marshmallow.EXCLUDE):
        try:
            return self.load(data, unknown=unknown)
        except marshmallow.ValidationError as err:
            flask_restful.abort(400, error="ERR_VALIDATION_FAILED", errors=err.messages)

    def load(self, data, *, many=None, partial=None, unknown=None):
        # this was added because of `marshmallow.fields.Nested` validation
        # as it is not calling `SuperSchema.check_and_abort` so `unknown` field is not set for it
        if not unknown:
            unknown = marshmallow.EXCLUDE
        return super(marshmallow.Schema, self).load(
            data, many=many, partial=partial, unknown=unknown
        )

    @marshmallow.pre_load
    def remove_null_values(self, data, **kwargs):
        return {
            key: value for key, value in data.items() if value is not None
        }
