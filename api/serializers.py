from rest_framework.serializers import HyperlinkedIdentityField, CharField, IntegerField, Serializer, ModelSerializer
from notes.models import Note


class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'

class ThinNoteSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='notes-detail')
    class Meta:
        model = Note
        fields = ('id', 'title', 'url')


# class NoteSerializer(Serializer):
#     id = IntegerField(read_only=True)
#     title = CharField(max_length=255, required=True)
#     text = CharField(allow_blank=True, required=True)
#
#     def create(self, validated_data):
#         return Note(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.text = validated_data.get('text', instance.text)
#         instance.save()
#         return instance







