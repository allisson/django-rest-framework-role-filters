from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    serializer_name = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'admin_only_field',
            'body',
            'created_at',
            'id',
            'serializer_name',
            'title',
            'updated_at',
            'user',
        )
        read_only_fields = (
            'id',
            'user',
        )

    def __init__(self, *args, **kwargs):
        # From http://www.django-rest-framework.org/api-guide/serializers/#example
        fields = kwargs.pop('fields', None)

        super(PostSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def validate(self, data):
        data['user'] = self.context['request'].user
        return data

    def get_serializer_name(self, obj):
        return 'PostSerializer'


class PostSerializerForUser(PostSerializer):
    def get_serializer_name(self, obj):
        return 'PostSerializerForUser'
