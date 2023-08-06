import json
import random
import abc

class SchemaResolverBaseClass(abc.ABC):

    @abc.abstractmethod
    def get_schema(self, reference):
        """Given a reference, returns a wrapped schema object.
        """
        pass


class GeneratorFromSchema(object):

    def __init__(self, resolver=None):
        self.resolver = resolver
        self.includeMode = 'all'

    def GetExampleOr(self, schema, default):
        if 'example' in schema:
            return schema['example']
        elif 'examples' in schema:
            return schema['examples'][0]
        elif 'enum' in schema:
            return schema['enum'][0]
        else:
            return default

    def GetNumber(self, schema):
        return self.GetExampleOr(schema, schema['type'] == 'integer' and 1 or 3.14)

    def GetObject(self, schema, base=None):
        base = base or {}
        for propName, propSchema in schema['properties'].items():
            if (self.includeMode == 'required') and (('required' not in schema) or (propName not in schema['required'])):
                continue
            thing = self.GetThing(propSchema)
            base[propName] = thing
        default = None
        if 'default' in schema:
            default = schema['default']
        elif 'defaults' in schema and isinstance(schema['defaults'], list):
            default = schema['defaults'][0]
        if default is not None:
            base.update(default)
        return base

    def GetArray(self, schema):
        base = []
        defaultMin = self.includeMode == 'all' and 1 or 0
        minItems = 'minItems' in schema and schema['minItems'] or defaultMin
        for _ in range(0, minItems):
            base.append(self.GetThing(schema['items']))
        return base

    def GetThing(self, schema, base=None):
        base = base or {}
        if '$ref' in schema:
            schema = self.resolver.get_schema(reference=schema['$ref'])
        if 'allOf' in schema:
            obj = base
            for opt in schema['allOf']:
                obj = self.GetThing(opt, base=obj)
            return obj
        elif 'anyOf' in schema:
            obj = base
            if self.includeMode == 'required':
                return obj
            for opt in schema['anyOf']:
                obj = self.GetThing(opt, base=obj)
            return obj
        elif 'oneOf' in schema:
            thing = self.GetThing(random.choice(schema['oneOf']))
            return thing
        elif 'type' not in schema:
            raise NotImplementedError(schema)
        elif schema['type'] in ['integer', 'number']:
            return self.GetNumber(schema)
        elif schema['type'] == 'string':
            return self.GetExampleOr(schema, 'string')
        elif schema['type'] == 'null':
            return None
        elif schema['type'] == 'boolean':
            return self.GetExampleOr(schema, True)
        elif schema['type'] == 'object':
            return self.GetObject(schema, base)
        elif schema['type'] == 'array':
            return self.GetArray(schema)
        else:
            raise NotImplementedError

    def GenerateSome(self, schema, run, includeMode) -> set:
        self.includeMode = (includeMode in ['all', 'required']) and includeMode or 'all'
        examples = set()
        for _ in range(0, run):
            thing = self.GetThing(schema)
            examples.add(json.dumps(thing, sort_keys=True))
        return examples

    def GenerateFull(self, schema, run=100) -> set:
        schemaJsonText = json.dumps(schema)
        run = max(2, schemaJsonText.count('oneOf')) * 4
        return self.GenerateSome(schema, run, 'all')

    def GenerateLimited(self, schema, run=2) -> set:
        schemaJsonText = json.dumps(schema)
        run = max(1, schemaJsonText.count('oneOf')) * 2
        return self.GenerateSome(schema, run, 'required')
    
    def Generate(self, schema) -> list:
        full = self.GenerateFull(schema)
        full.update(self.GenerateLimited(schema))
        return [json.loads(s) for s in full]

