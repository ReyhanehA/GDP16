from django.forms import ModelForm as DjangoModelForm
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields import NOT_PROVIDED


class ModelForm(DjangoModelForm):
    """
    Allows a model form to validate properly with default attributes missing.

    Django model forms expect all attributes for a given model to be present
    in a request. Since a typical request comes from an HTML form and the HTML
    for that form is typically generated by the form object (which sets all
    of the HTML form values to the defaults of the model), this is usually not
    an issue. However, with RESTful requests, we cannot assume that all
    attributes will be present in the request.

    This class allows the form to validate even if some (optional) attributes
    are not present in the original request. It does so by adding the default
    values (from the model) to the data from the request for each missing
    attribute. It must add these elements to the data object, as opposed to
    just passing it to the form's __init__ method as the 'initial' parameter
    since 'initial' is only used to render the HTML form and not for the
    validation of the data.

    UPDATE:
    This mixin has been updated to also populate form with values from an
    instance, if one has been provided.
    Note: this has not yet been tested, and likely does not work, on
    many-to-many relationships.
    """

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)

        # Make sure the data is editable and that we are not altering the
        # original object
        data = {}
        for k, v in self.data.items():
            data[k] = v
        self.data = data

        for field in self.instance.__class__._meta.fields:
            if field.name not in self.data.keys() or self.data.get(field.name) == None:
                inst_val = None
                if self.instance.id:
                    try:
                        inst_val = getattr(self.instance, field.name)
                        #Get the ID if this is a model object and
                        #we're dealing with a foreign key
                        #relationship.
                        inst_val = getattr(inst_val, 'id')
                    except (AttributeError, ObjectDoesNotExist):
                        pass
                    self.data[field.name] = inst_val
                elif field.default != NOT_PROVIDED:
                    self.data[field.name] = field.default
