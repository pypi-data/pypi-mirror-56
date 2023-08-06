from typing import List, Union, Optional
from datalogue.errors import DtlError, _property_not_found
from datalogue.models.transformations.commons import Transformation
from datalogue.utils import _parse_list
from abc import ABC, abstractmethod
from uuid import UUID


class ClassificationMethod(ABC):
    type_field = "type"

    def __init__(self, transformation_type: str):
        self.type = transformation_type
        super().__init__()

    def _base_payload(self) -> dict:
        return dict([(Transformation.type_field, self.type)])

    @abstractmethod
    def _as_payload(self) -> dict:
        """
        Represents the Classification method as a json payload

        :return:
        """
        pass

    @staticmethod
    @abstractmethod
    def _from_payload(json: dict) -> 'ClassificationMethod':
        """
        Represents the Classification method as a json payload

        :return:
        """


class RegexMap(object):
    def __init__(self, regex_ids: List[Union[UUID, str]], class_id: Union[UUID, str]):
        """
        Build a mapping between an ontological class and one or more regexes. The mapping will be used by a
            RegexOnFieldNameMethod or RegexOnValueMethod to apply classifications.

        :param class_id: the id of the ontological class that a regex match should maps to
        :param regex_ids: a list of regex ids whose matches map to the ontological class

        """
        self.regex_ids = regex_ids
        self.class_id = class_id

    def __repr__(self):
        pairs = ""
        for id in self.regex_ids:
            pairs += '\n  regex_id(' + str(id) + ') --> class_id(' + str(self.class_id) + ')'

        return ('RegexMap('
                f'{pairs})')

    def __eq__(self, other: 'RegexMap'):
        if isinstance(self, other.__class__):
            return self._as_payload() == other._as_payload()
        return False

    def _as_payload(self) -> dict:
        return {
            "regexes": list(map(lambda i: str(i), self.regex_ids)),
            "class": str(self.class_id)
        }

    @staticmethod
    def _from_payload(json: dict) -> Union[DtlError, 'RegexMap']:
        regexes = json.get("regexes")
        if regexes is None:
            return _property_not_found("regexes", json)

        class_id = json.get("class")
        if regexes is None:
            return _property_not_found("class", json)

        return RegexMap(regexes, class_id)


class MLMethod(ClassificationMethod):
    type_str = "MLMethod"

    def __init__(self, model_id: Union[UUID, str], threshold: Optional[float] = None):
        """
        Builds a local Machine learning classification method

        note: please deploy the model before using this method

        :param model_id: id of the machine learning model to be used
        :param threshold: optionally set a score threshold between 0 and 1, under which classification
            by this method fails
        """
        ClassificationMethod.__init__(self, MLMethod.type_str)
        self.model_id = model_id
        self.threshold = threshold

        if threshold is not None and threshold < 0:
            raise DtlError("Invalid threshold. Confidence scores are positive numbers. Please set "
                           "a threshold within that range.")

    def __repr__(self):
        return ('MLMethod(\n '
                f'model_id: {self.model_id}, '
                f'threshold: {self.threshold}\n)')

    def __eq__(self, other: 'MLMethod'):
        if isinstance(self, other.__class__):
            return self._as_payload() == other._as_payload()
        return False

    def _as_payload(self) -> dict:
        base = self._base_payload()
        base["model"] = str(self.model_id)
        base["threshold"] = self.threshold
        return base

    @staticmethod
    def _from_payload(json: dict) -> Union[DtlError, 'MLMethod']:
        model = json.get("model")
        if model is None:
            return _property_not_found("model", json)

        threshold = json.get("threshold")

        return MLMethod(model, threshold)


class RegexOnFieldNameMethod(ClassificationMethod):
    type_str = "RegexOnFieldNameMethod"

    def __init__(self, regex_name_maps: List[RegexMap]):
        """
        Build a classification method based on regexes applied to field names.
        This classification method will apply classes when a match is found between a data point’s field name
            and a supplied regex.

        note: the classification score supplied by a regex match is 1.0

        :param regex_name_maps: a list of the mappings between regexes and the classes they map to
        """
        ClassificationMethod.__init__(self, RegexOnFieldNameMethod.type_str)
        self.regex_name_maps = regex_name_maps

    def __repr__(self):
        pairs = repr(self.regex_name_maps)

        return ('\nRegexOnFieldNameMethod('
                f'{pairs}'
                f'\n  - Regexes above used to target data \033[1mfield names\033[0m for classification\n)')

    def __eq__(self, other: 'RegexOnFieldNameMethod'):
        if isinstance(self, other.__class__):
            return self._as_payload() == other._as_payload()
        return False

    def _as_payload(self) -> dict:
        base = self._base_payload()
        base["regexNameMaps"] = list(map(lambda m: m._as_payload(), self.regex_name_maps))
        return base

    @staticmethod
    def _from_payload(json: dict) -> Union[DtlError, 'RegexOnFieldNameMethod']:
        regex_name_maps = json.get("regexNameMaps")
        if regex_name_maps is None:
            return _property_not_found("regexNameMaps", json)
        else:
            regex_name_maps = _parse_list(RegexMap._from_payload)(regex_name_maps)
            if isinstance(regex_name_maps, DtlError):
                return regex_name_maps

        return RegexOnFieldNameMethod(regex_name_maps)


class RegexOnValueMethod(ClassificationMethod):
    type_str = "RegexOnValueMethod"

    def __init__(self, regex_value_maps: List[RegexMap]):
        """
        Build a classification method based on regexes applied to data values.
        This classification method will apply classes when a match is found between a data point’s value and a
         supplied regex.

        note: the classification score supplied by a regex match is 1.0

        :param regex_value_maps: a list of the mappings between regexes and the classes they map to
        """
        ClassificationMethod.__init__(self, RegexOnValueMethod.type_str)
        self.regex_value_maps = regex_value_maps

    def __repr__(self):
        pairs = repr(self.regex_value_maps)

        return ('\nRegexOnValueMethod('
                f'{pairs}'
                f'\n  - Regexes above used to target data \033[1mvalues\033[0m for classification\n)')

    def __eq__(self, other: 'RegexOnValueMethod'):
        if isinstance(self, other.__class__):
            return self._as_payload() == other._as_payload()
        return False

    def _as_payload(self) -> dict:
        base = self._base_payload()
        base["regexValueMaps"] = list(map(lambda m: m._as_payload(), self.regex_value_maps))
        return base

    @staticmethod
    def _from_payload(json: dict) -> Union[DtlError, 'RegexOnValueMethod']:
        regex_name_maps = json.get("regexValueMaps")
        if regex_name_maps is None:
            return _property_not_found("regexValueMaps", json)
        else:
            regex_name_maps = _parse_list(RegexMap._from_payload)(regex_name_maps)
            if isinstance(regex_name_maps, DtlError):
                return regex_name_maps

        return RegexOnValueMethod(regex_name_maps)


class Classifier(object):

    def __init__(self, classification_methods: List[ClassificationMethod], default_class_id: Optional[Union[UUID, str]] = None):
        """
        Build a local Classifier

        :param classification_methods: ordered list of Classification Methods
        :param default_class_id: allows the user to specify the class to be defaulted to, if all classification methods
            fail. Default value is `Unknown`. (currently part of replace_class, see below)
        """
        self.classification_methods = classification_methods
        self.default_class_id = default_class_id

    def __repr__(self):
        return ('Classifier('
               f'default_class: {self.default_class_id} '
               f'classification_methods: \n{self.classification_methods})')

    def __eq__(self, other: 'Classifier'):
        if isinstance(self, other.__class__):
            return self._as_payload() == other._as_payload()
        return False

    def _as_payload(self) -> dict:
        base = {
            "classificationMethods":  list(map(lambda m: m._as_payload(), self.classification_methods)),
            "defaultClass": self.default_class_id
        }
        return base

    @staticmethod
    def _from_payload(json: dict) -> Union[DtlError, 'Classifier']:
        classification_methods = json.get("classificationMethods")
        if classification_methods is None:
            return _property_not_found("classificationMethods", json)
        else:
            classification_methods = _parse_list(_classification_method_from_payload)(classification_methods)
            if isinstance(classification_methods, DtlError):
                return classification_methods

        default_class = json.get("default_class")

        return Classifier(classification_methods, default_class)


class Classify(Transformation):
    """
    Apply classes to all data streaming through a pipeline. Classification is based on the Classifier supplied.
    """
    type_str = "Classify"

    def __init__(self, classifier: Classifier, fields_to_target: Optional[List[List[str]]] = None,
                 add_class_fields=False, add_score_fields=False):
        """
        Unless specified with parameters below, this transformation does not alter the data schema; classes are
        represented in the backend only.

        :param classifier: the Classifier object to use for classification
        :param fields_to_target: specifies which fields to target for classification; remainder are not classified by
         this transformation
        :param add_class_fields: if True, adds a field containing class name for every classified field
        :param add_score_fields: if True, adds a field containing class score for every classified field
        """

        Transformation.__init__(self, Classify.type_str)
        self.classifier = classifier
        self.fields_to_target = fields_to_target
        self.add_class_fields = add_class_fields
        self.add_score_fields = add_score_fields

    def __eq__(self, other: 'Classify'):
        if isinstance(self, other.__class__):
            return self._as_payload() == other._as_payload()
        return False

    def __repr__(self):
        return('Classify('
               f'classifier: {self.classifier}, '
               f'fields_to_target: {self.fields_to_target}, '
               f'add_class_fields: {self.add_class_fields}, '
               f'add_score_fields: {self.add_score_fields})')

    def _as_payload(self) -> dict:
        base = self._base_payload()
        base["classifier"] = self.classifier._as_payload()
        base["fieldsToTarget"] = self.fields_to_target
        base["addClassFields"] = self.add_class_fields
        base["addScoreFields"] = self.add_score_fields
        return base

    @staticmethod
    def _from_payload(json: dict) -> Union[DtlError, 'Classify']:
        classifier = json.get("classifier")
        if classifier is None:
            return _property_not_found("classifier", json)
        else:
            classifier = Classifier._from_payload(classifier)
            if isinstance(classifier, DtlError):
                return classifier

        fields_to_target = json.get("fieldsToTarget")

        add_class_fields = json.get("addClassFields")
        if add_class_fields is None:
            add_class_fields = False

        add_score_fields = json.get("addScoreFields")
        if add_score_fields is None:
            add_score_fields = False

        return Classify(classifier, fields_to_target, add_class_fields, add_score_fields)


_ml_methods = dict([
    (MLMethod.type_str, MLMethod._from_payload),
    (RegexOnFieldNameMethod.type_str, RegexOnFieldNameMethod._from_payload),
    (RegexOnValueMethod.type_str, RegexOnValueMethod._from_payload)
])


def _classification_method_from_payload(json: dict) -> Union[DtlError, ClassificationMethod]:
    type_field = json.get(ClassificationMethod.type_field)
    if type_field is None:
        return DtlError("The json object doesn't have a '%s' property" % ClassificationMethod.type_field)

    parsing_function = _ml_methods.get(type_field)
    if parsing_function is None:
        return DtlError("Looks like '%s' Classification method is not handled by the SDK" % type_field)

    return parsing_function(json)
