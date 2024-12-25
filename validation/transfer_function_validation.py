from marshmallow import Schema, fields, validate, validates_schema, ValidationError, INCLUDE

class TransferFunctionPlotInput(Schema):
    num = fields.List(fields.Float, required=True)  # Numerator coefficients of the transfer function
    den = fields.List(fields.Float, required=True)  # Denominator coefficients of the transfer function
    t_max = fields.Float(required=True, validate=validate.Range(min=0))  # t_max (float value)

    class Meta:
        unknown = INCLUDE  # This will allow unknown fields in the payload

    @validates_schema
    def validate_ranges(self, data, **kwargs):
        # Validate that numerator and denominator have at least one element each
        if "num" in data and len(data["num"]) == 0:
            raise ValidationError("Numerator list (num) cannot be empty.")
        if "den" in data and len(data["den"]) == 0:
            raise ValidationError("Denominator list (den) cannot be empty.")

        # Ensure that the degree of the denominator is at least as large as the numerator
        if "num" in data and "den" in data:
            if len(data["num"]) > len(data["den"]):
                raise ValidationError("The degree of the denominator must be greater than or equal to the numerator.")


class TransferFunctionPlotInputWithAxis(TransferFunctionPlotInput):
    x_axis = fields.List(fields.Float, required=True, validate=validate.Length(equal=2))  # Range for x-axis
    y_axis = fields.List(fields.Float, required=True, validate=validate.Length(equal=2))  # Range for y-axis

    @validates_schema
    def validate_axis(self, data, **kwargs):
        # Validate that x_axis defines a valid range
        if "x_axis" in data and data["x_axis"][0] >= data["x_axis"][1]:
            raise ValidationError("x_axis must define a valid range: [min, max] with min < max.")
        # Validate that y_axis defines a valid range
        if "y_axis" in data and data["y_axis"][0] >= data["y_axis"][1]:
            raise ValidationError("y_axis must define a valid range: [min, max] with min < max.")


class TransferFunctionInput(Schema):
    num = fields.List(fields.Float, required=True)  # Numerator coefficients of the transfer function
    den = fields.List(fields.Float, required=True)  # Denominator coefficients of the transfer function

    class Meta:
        unknown = INCLUDE  # This will allow unknown fields in the payload
