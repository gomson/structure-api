from rest_framework import serializers

from .models import DjangoBaseNode, DjangoDependencyRelation


class DjangoBaseNodeSlugSerializer(serializers.Serializer):
    """
    Just reports the `uuid` of target node as well as (scope:path).
    """
    id = serializers.UUIDField(source='uuid', required=True)
    path = serializers.CharField(max_length=1000)
    scope = serializers.CharField(max_length=1000)


# Different serializer depending on direction being used for relationship
class DjangoUsedforsRelationSerializer(serializers.Serializer):
    usedfor = DjangoBaseNodeSlugSerializer(required=True)
    explain_usedfor = serializers.CharField(max_length=1000)
    level = serializers.CharField(max_length=1000)


class DjangoPrerequisitesRelationSerializer(serializers.Serializer):
    prerequisite = DjangoBaseNodeSlugSerializer(required=True)
    explain_prerequisite  = serializers.CharField(max_length=1000)
    level = serializers.CharField(max_length=1000)


class DjangoBaseNodeSerializer(serializers.Serializer):
    """
    Used to recusiverly serialize Nodes to JSON.
      - hops=0: only data of current node is returned (fk for others)
      - hops=1: return also data of nodes linked to
    """
    id          = serializers.UUIDField(source='uuid', required=True)
    path        = serializers.CharField(max_length=1000)
    scope       = serializers.CharField(max_length=1000)
    version     = serializers.CharField(max_length=1000)
    created_at  = serializers.DateTimeField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)
    comment     = serializers.CharField(allow_blank=True, allow_null=True)

    # relationships (useing reverse direction of ForeignKey from Relation model)
    # needed since `prerequisites` resolves to `DjangoBaseNodeSerializer`s
    prerequisites = DjangoPrerequisitesRelationSerializer(source='usedfors_rels', many=True, read_only=True)
    usedfors = DjangoUsedforsRelationSerializer(source='prerequisites_rels', many=True, read_only=True)

    class Meta:
        read_only_fields = ('id', 'created_at', 'modified_at',)
        
    def update(self, instance, validated_data):
        instance.path = validated_data.get('path', instance.path)
        instance.scope = validated_data.get('scope', instance.scope)
        instance.version = validated_data.get('version', instance.version)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance



class CreateDjangoBaseNodeSerializer(serializers.Serializer):
    """
    Used to process POST requests that create new `DjangoBaseNode`s.
    """
    path        = serializers.CharField(max_length=1000)
    scope       = serializers.CharField(max_length=1000)
    version     = serializers.CharField(max_length=1000)
    comment     = serializers.CharField(allow_blank=True, allow_null=True)
    
    class Meta:
        fields = ('path', 'scope', 'version', 'comment',)
        read_only_fields = ('id')

    def create(self, validated_data):
        node = DjangoBaseNode(**validated_data)
        node.save()
        return node



# # custom field example
# class PolymorphicTaggedObjectRelatedField(serializers.RelatedField):
#     """
#     A custom field to use for the `tagged_object` generic relationship.
#     """
#     def to_representation(self, value):
#         """
#         Serialize tagged objects to a simple textual representation.
#         """
#         if isinstance(value, Bookmark):
#             return 'Bookmark: ' + value.url
#         elif isinstance(value, Note):
#             return 'Note: ' + value.text
#         raise Exception('Unexpected type of tagged object')
# if isinstance(value, Bookmark):
#     serializer = BookmarkSerializer(value)
# elif isinstance(value, Note):
#     serializer = NoteSerializer(value)
# else:
#     raise Exception('Unexpected type of tagged object')
# 
# return serializer.data