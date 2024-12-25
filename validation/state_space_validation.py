from marshmallow import Schema, fields, validate, validates_schema, ValidationError, INCLUDE


class StateSpacePlotInput(Schema):
    A = fields.List(fields.List(fields.Float), required=True)  # Matrix A (list of lists of floats)
    B = fields.List(fields.List(fields.Float), required=True)  # Matrix B (list of lists of floats)
    C = fields.List(fields.List(fields.Float), required=True)  # Matrix C (list of lists of floats)
    D = fields.List(fields.List(fields.Float), required=True)  # Matrix D (list of lists of floats)
    t_max = fields.Float(required=True, validate=validate.Range(min=0))  # t_max (float value)

    class Meta:
        unknown = INCLUDE  # This will allow unknown fields in the payload



class StateSpacePlotInputWithAxis(StateSpacePlotInput):
    # Adding x_axis and y_axis fields
    x_axis = fields.List(fields.Float, required=True, validate=validate.Length(equal=2))  # Range for x-axis
    y_axis = fields.List(fields.Float, required=True, validate=validate.Length(equal=2))  # Range for y-axis

    @validates_schema
    def validate_ranges(self, data, **kwargs):
        # Validate that x_axis defines a valid range
        if "x_axis" in data and data["x_axis"][0] >= data["x_axis"][1]:
            raise ValidationError("x_axis must define a valid range: [min, max] with min < max.")
        # Validate that y_axis defines a valid range
        if "y_axis" in data and data["y_axis"][0] >= data["y_axis"][1]:
            raise ValidationError("y_axis must define a valid range: [min, max] with min < max.")

class StateSpaceInput(Schema):
    A = fields.List(fields.List(fields.Float), required=True)  # Matrix A (list of lists of floats)
    B = fields.List(fields.List(fields.Float), required=True)  # Matrix B (list of lists of floats)
    C = fields.List(fields.List(fields.Float), required=True)  # Matrix C (list of lists of floats)
    D = fields.List(fields.List(fields.Float), required=True)  # Matrix D (

    class Meta:
        unknown = INCLUDE  # This will allow unknown fields in the payload