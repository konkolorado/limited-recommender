from rest_framework import serializers


class UserIDSlugRelatedField(serializers.SlugRelatedField):
    def display_value(self, instance):
        return f'{instance.user_id}'


class ISBNSlugRelatedField(serializers.SlugRelatedField):
    def display_value(self, instance):
        return f'{instance.isbn}'
